import pandas as pd

def clean_outliers(data, outliers_csv='outliers.csv'):
    """
    Cleans a dataset by detecting and removing rows containing outliers based on the Interquartile Range (IQR) method.
    
    Outliers are values that lie outside the range defined by:
        [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]
    where Q1 is the first quartile (25th percentile) and Q3 is the third quartile (75th percentile).

    Parameters:
    -----------
    data : pandas.DataFrame
        The input dataset to clean. It is expected to have numerical columns for which the IQR method can be applied.
    
    outliers_csv : str, optional, default 'outliers.csv'
        The filename where the rows containing outliers will be saved. The outliers are stored in a CSV file 
        before being removed from the dataset.

    Returns:
    --------
    pandas.DataFrame
        A new DataFrame that contains the cleaned dataset with outliers removed.

    Process:
    --------
    1. The function calculates the interquartile range (IQR) for each numeric column in the dataset.
    2. Rows with values outside the range [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR] are identified as outliers.
    3. These outlier rows are printed with their corresponding outlier values and removed from the dataset.
    4. The outlier rows are saved in a CSV file specified by `outliers_csv`.
    5. The cleaned dataset is returned without the rows containing outliers.

    Example:
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    >>>     'A': [1, 2, 3, 1000],
    >>>     'B': [4, 5, 6, -999]
    >>> })
    >>> clean_df = clean_outliers(df, outliers_csv='outliers.csv')
    Outlier in row 3 for column 'A': 1000
    Outlier in row 3 for column 'B': -999
    
    >>> clean_df
       A  B
    0  1  4
    1  2  5
    2  3  6
    """
    
    # Copy the original dataset
    cleaned_data = data.copy()
    
    # Create a list to store rows with outliers
    outlier_rows = []

    # Loop over each column in the dataset
    for column in cleaned_data.columns:
        if pd.api.types.is_numeric_dtype(cleaned_data[column]):
            # Calculate Q1 (25th percentile) and Q3 (75th percentile)
            Q1 = cleaned_data[column].quantile(0.25)
            Q3 = cleaned_data[column].quantile(0.75)
            
            # Calculate Interquartile Range (IQR)
            IQR = Q3 - Q1
            
            # Define the bounds for outliers
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Find outliers
            outliers = cleaned_data[(cleaned_data[column] < lower_bound) | (cleaned_data[column] > upper_bound)]
            
            # Print the rows and corresponding outlier values
            for index, row in outliers.iterrows():
                print(f"Outlier in row {index} for column '{column}': {row[column]}")
                outlier_rows.append(row)
            
            # Drop outliers from the cleaned dataset
            cleaned_data = cleaned_data[~((cleaned_data[column] < lower_bound) | (cleaned_data[column] > upper_bound))]
    
    # Create a DataFrame for the outliers and save to CSV
    outliers_df = pd.DataFrame(outlier_rows)
    outliers_df.to_csv(outliers_csv, index=False)
    
    return cleaned_data
