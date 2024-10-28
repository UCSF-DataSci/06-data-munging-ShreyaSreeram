import pandas as pd
import logging


logging.basicConfig(filename='data_cleaning.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(filepath):
    """Loads the data from a CSV file."""
    try:
        data = pd.read_csv(filepath)
        logging.info("Data loaded successfully.")
        return data
    except FileNotFoundError:
        logging.error(f"The file {filepath} was not found.")
        raise
    except Exception as e:
        logging.error(f"An error occurred while loading the data: {e}")
        raise

def remove_duplicates(data):
    """Removes duplicate rows from the dataset."""
    initial_count = len(data)
    data = data.drop_duplicates()
    duplicates_removed = initial_count - len(data)
    logging.info(f"Duplicate rows identified at indices: {duplicates_removed}")
    logging.info(f"Removed {duplicates_removed} duplicate rows.")
    return data

def handle_missing_values(data):
    """Imputes missing values for 'age', 'year', 'population' and remove rows with missing categorical data."""
    # Log the initial state of missing values
    missing_before = data[data.isnull().any(axis=1)]
    initial_count = len(data)
    
    # Impute missing values for 'age' with the median
    data['age'] = data['age'].fillna(data['age'].median())
    
    # If 'year' contains NaN after coercion, fill with a placeholder or remove
    if 'year' in data.columns:
        data['year'] = pd.to_numeric(data['year'], errors='coerce')
        if data['year'].isnull().any():
            # Fill year with a placeholder value (e.g., -1) or a reasonable value
            data['year'] = data['year'].fillna(-1).astype(int)
    
    # If 'population' contains NaN, fill with 0 or a specified placeholder
    if 'population' in data.columns:
        data['population'] = pd.to_numeric(data['population'], errors='coerce')
        data['population'] = data['population'].fillna(0).astype(int)
    
    # Remove rows where 'income_groups' or 'gender' is missing
    data.dropna(subset=['income_groups', 'gender'], inplace=True)
    
    # Log the final state after handling missing values
    missing_removed = initial_count - len(data)
    logging.info(f"Rows with missing values before cleaning: {len(missing_before)}")
    logging.info(f"Rows with missing values after cleaning: {missing_removed}")
    return data

def correct_outliers(data):
    """Corrects outliers in the population column using IQR."""
    Q1 = data['population'].quantile(0.25)
    Q3 = data['population'].quantile(0.75)
    IQR = Q3 - Q1
    condition = (data['population'] < Q1 - 1.5 * IQR) | (data['population'] > Q3 + 1.5 * IQR)
    outliers_before = data[condition]
    data = data[~condition]
    logging.info(f"Outlier rows identified at indices: {len(outliers_before)}")
    logging.info(f"Total outliers removed: {len(outliers_before)}")
    return data

def fix_data_types(data):
    """Converts data types to appropriate formats and handle errors."""
    print("Initial data types:\n", data.dtypes)

    try:
        # Ensure 'year' and 'population' are treated as numeric, coercing errors to NaN
        data['year'] = pd.to_numeric(data['year'], errors='coerce')
        if data['year'].isnull().any():
            print("Warning: NaN introduced by coercion in 'year'")
        data['year'] = data['year'].dropna().astype(int)

        data['population'] = pd.to_numeric(data['population'], errors='coerce')
        if data['population'].isnull().any():
            print("Warning: NaN introduced by coercion in 'population'")
        data['population'] = data['population'].fillna(0).astype(int)

        # Ensure 'gender' is converted to categorical
        data['gender'] = data['gender'].astype('category')
        print("'gender' column converted to categorical.")

    except Exception as e:
        print(f"Failed to convert data types: {e}")
        raise

    print("Updated data types:\n", data.dtypes)
    return data

def filter_future_dates(data):
    """Removes entries with future dates."""
    current_year = pd.to_datetime('today').year
    future_dates = data[data['year'] > current_year]
    initial_count = len(data)
    data = data[data['year'] <= current_year]
    dates_removed = initial_count - len(data)
    logging.info(f"Future date rows identified at indices: {len(future_dates)}")
    logging.info(f"Total future date rows removed: {dates_removed}")
    return data

def save_cleaned_data(data, output_path):
    """Saves the cleaned data to a CSV file."""
    try:
        data.to_csv(output_path, index=False)
        logging.info(f"Cleaned data saved to {output_path}.")
    except Exception as e:
        logging.error(f"Failed to save cleaned data: {e}")
        raise

def main():
    input_path = 'messy_population_data.csv'
    output_path = 'cleaned_population_data.csv'


    data = load_data(input_path)

    data = remove_duplicates(data)
    data = handle_missing_values(data)
    data = correct_outliers(data)
    data = fix_data_types(data)
    data = filter_future_dates(data)

    save_cleaned_data(data, output_path)

if __name__ == '__main__':
    main()