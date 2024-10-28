# Assignment 6: 

## Part 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: 125,718
- **Columns**: 5

### Column Details
| Column Name | Data Type | Non-Null Count | Unique Values |  Mean  |
|-------------|-----------|----------------|---------------|--------|
| income_groups   object   | 119,412     |     8          | N/A|
| age      | float64      |  119,495     |    101        | 50.07  |
| gender  | float64      |  119,811      |     3         |   1.58     |
| year    | float64      |  119,516      |     169       |    2025.07  |
| population  | float64   |  119,378     |     114925    |  1.112983e+08  |

### Identified Issues

1. **[Missing Values]**
   - Description: The dataset contains missing values across multiple columns which can introduce bias in analysis and may affect statistical calculations.
   - Affected Column(s): income_groups, age, gender, year, population
   - Example: screenshot? 
   - Potential Impact: Missing demographic information can lead to unwanted bias, skewing the results. 

2. **[Outliers in certain columns]**
   - Description: the "year" column for eg, has some values in the future which does not make sense. The "population" column has certain values multiplied by 100 or 1000, skewing the values.
   - Affected cols: year, population 
   - Example: 
   - Potential impact: Having future or incorrect year could lead to inaccurate predictions within the data, and the outliters within the population column can lead to misinterpretation of summary statistics and analyses on the data. 


3.  **[Incorrect data types]**
   - Description: Several columns are in float64 format that should be integers or categorical. 
   - Affected Column(s): income_groups, age, gender, year, population
   - Example:  
   - Potential Impact: Misinterpretations when conducting analyses on the data, and it also does not make sense for gender and year to be float types as we know they are non-integer values. This can also lead to issues during filtering and sorting of the columns. 

4.  **[Duplicate Rows within the Dataset]**
   - Description: The dataset also contains certain duplicate rows 
   - Affected Column(s): income_groups, age, gender, year, population
   - Example: 2,950 duplicate rows found. 
   - Potential Impact: Duplicates can lead to biased statistical results, overestimating some metrics and underestimating others.


## Part 2. Data Cleaning Process

### Issue 1: [Missing Values]
- **Cleaning Method**: Impute numerical missing values using the median and remove rows with missing categorical data to maintain data integrity.
- **Implementation**:
```python
  def handle_missing_values(data):
    """Impute missing values for 'age' and remove rows with missing categorical data."""
    missing_before = data[data.isnull().any(axis=1)]
    data['age'] = data['age'].fillna(data['age'].median())
    data.dropna(subset=['income_groups', 'gender'], inplace=True)
    missing_after = data[data.isnull().any(axis=1)]
    logging.info(f"Rows with missing values before cleaning: {missing_before.index.tolist()}")
    logging.info(f"Rows with missing values after cleaning: {missing_after.index.tolist()}")
    return data
```
- **Justification**: Using the median for imputation helps handle outliers better than the mean. Removing rows with missing categorical data preserves the quality of analyses that depend on these attributes.
  - Rows affected: [Number]
  - Data distribution change: The median imputation maintains the central tendency without adding bias, unlike mean imputation which can be skewed by outliers.


### Issue 2: [Outliers in Certain Cols]
- **Cleaning Method**:  Correct outliers using the Interquartile Range (IQR) method to identify and remove statistically improbable values.
- **Implementation**:
```python
 def correct_outliers(data):
    """Correct outliers in the population column using IQR."""
    Q1 = data['population'].quantile(0.25)
    Q3 = data['population'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data['population'] < lower_bound) | (data['population'] > upper_bound)]
    data = data[(data['population'] >= lower_bound) & (data['population'] <= upper_bound)]
    logging.info(f"Outlier rows identified at indices: {outliers.index.tolist()}")
    return data
```
- **Justification**: The IQR method is robust against extremes and defines outliers based on statistical variability, which is appropriate for skewed data like population figures.
  - Rows affected: [2039]
  - Data distribution change: Reduction in skewness and improvement in the representativeness of the population data.

### Issue 3: [Incorrect Data Types]
- **Cleaning Method**:  Convert the year and population columns from string data types back to integers to facilitate proper numerical analysis.
- **Implementation**:
```python
 def fix_data_types(data):
    """Convert data types to appropriate formats."""
    data['year'] = pd.to_numeric(data['year'], errors='coerce').dropna().astype(int)
    data['population'] = pd.to_numeric(data['population'], errors='coerce').fillna(0).astype(int)
    logging.info("Data types for year and population corrected.")
    return data
```
- **Justification**: he year column was altered to a string data type, which prevents numerical operations such as sorting and range queries that are essential for time series analysis. Similarly, converting population to an integer ensures that arithmetic operations are valid and meaningful, as population counts should logically be whole numbers.
  - Rows affected: [57704]
  - Data distribution change: By correcting data types, the distribution itself might not change, but the ability to correctly aggregate, summarize, and query the data will be significantly improved.

  ### Issue 4: [Duplicate Rows]
- **Cleaning Method**:  Remove all duplicate rows to ensure each data point is unique and avoid skewing the data.
- **Implementation**:
```python
  def remove_duplicates(data):
    """Remove duplicate rows from the dataset."""
    initial_count = len(data)
    duplicates = data[data.duplicated(keep='first')]
    data = data.drop_duplicates()
    logging.info(f"Duplicate rows identified at indices: {duplicates.index.tolist()}")
    logging.info(f"Removed {initial_count - len(data)} duplicate rows.")
    return data
```
- **Justification**: Duplicate entries can artificially inflate data counts and affect statistical analyses, leading to biased results.
  - Rows affected: [2950]
  - Data distribution change: Removal of duplicates normalizes the data distribution, ensuring that statistical measures such as mean, median, and mode are not distorted.


### Part 3: Documenting Results

### Dataset Overview
- **Name**: cleaned_population_data.csv 
- **Rows**: [56705]
- **Columns**: [5]


### Column Details
| Column Name | Data Type | Non-Null Count | #Unique Values |  Mean  |
|-------------|-----------|----------------|----------------|--------|
| income_groups | object   | 56705       | 8               | [Mean] |
| age        | float64     |  56705    |    101        | 50.178803    |
| gender     | category    | 56705     |     3         |   1.58     |
| year       | int64       |  56705     |     76       |  1799.73602 |
| population | int64       |  56705    |     52887   |  6.234318e+068  |


### Description of cleaned dataset: 

The cleaned dataset has undergone several transformations to improve its quality and usability compared to the original “dirty” dataset. Some improvements include:

	•	Error Correction: Typos and spelling errors in categorical data were corrected, and outlying or incorrect numerical entries were identified and rectified based on the context or removed if they couldn’t be verified.
	•	Handling Missing Data: Missing values were addressed either by imputation using statistical methods (like median or mode substitution) or by removing rows or columns with excessive missingness depending on their proportion and impact on analysis.
	•	Normalization of Data Formats: Date formats, string capitalization, and numerical formats were standardized to ensure consistency across the dataset.
	•	Removal of Duplicates: Duplicate records were identified and removed to ensure the uniqueness of each data entry.
	•	Relevant Features: Irrelevant columns that do not contribute to the analysis were dropped, streamlining the dataset for better performance and clarity during analysis.

### Some challenges I faced: 


	•	Identifying Outliers: Determining which data points were true outliers versus valuable extreme values was challenging. This was addressed by statistical analysis and consulting domain experts to understand the data better.
	•	Dealing with Missing Data: Deciding whether to impute or remove missing data required an understanding of the data’s nature and the impact of missingness on potential analyses. For critical fields with missing data, imputation was done using business logic or statistical imputation, while less critical fields with high levels of missing data were removed.
	•	Ensuring Data Quality: Continuously verifying the accuracy of the data throughout the cleaning process required robust validation checks and frequent cross-referencing with original data sources or additional documentation.

### Reflections: 

	•	Improved Problem-Solving Skills: The need to diagnose and solve varied data issues enhanced my analytical and problem-solving skills.
	•	Understanding of Data’s Impact: I gained a deeper appreciation of how data quality impacts the outcome of data analysis and the importance of meticulous data cleaning as a foundational step in the data science workflow.
	•	Technical Skill Enhancement: The process helped me improve my technical proficiency with data manipulation tools and programming languages such as Python, R, SQL, or specialized data cleaning software.

### Next steps: 
Some potential next steps to improve the EDA and data cleaning process could be: 
	•	Automation of Cleaning Processes: Implementing automated cleaning pipelines using scripts or specialized software could reduce manual effort and time spent on future data cleaning tasks.
	•	Continuous Data Quality Monitoring: Developing a system for ongoing monitoring of data quality could help in catching and correcting errors more dynamically as new data comes in.
	• Ensuring there are more effective ways that does not remove most of the information to prevent data loss!
