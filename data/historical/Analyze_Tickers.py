import pandas as pd
import glob

# Path to where your CSV files are stored
path = 'C:/Users/Nick/Desktop/Boost Buddy/css fp/AlgoTrading/'

# List of problematic tickers/files to exclude
excluded_files = ['IRX.csv', 'BRK.B.csv']  # Add any other problematic files to this list

# Load all CSV files in the specified directory
all_files = glob.glob(path + "*.csv")

# Exclude problematic files from the list of all files
all_files = [f for f in all_files if f.split('/')[-1] not in excluded_files]

# Check if any files are found after exclusion
if not all_files:
    print("No CSV files found after excluding problematic files. Please check the path or exclusions.")
else:
    df_list = []
    
    # Process each file
    for file in all_files:
        try:
            # Attempt to read the CSV file into a DataFrame
            df = pd.read_csv(file)
            ticker = file.split('/')[-1].split('_')[0]  # Extract ticker from filename
            df['Ticker'] = ticker  # Add a new column for the ticker symbol
            df_list.append(df)  # Add the DataFrame to the list
            print(f"Successfully loaded data for {ticker}")
        
        except Exception as e:
            # Handle and log any errors during the file loading process
            print(f"Error processing file {file}: {e}")
    
    # Combine all successfully loaded DataFrames
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        print("Data loaded successfully.")
        
        # **Check for Missing Values**
        print("Checking for missing values...")
        print(combined_df.isnull().sum())

        # **Option 1: Drop rows with missing values**
        combined_df_cleaned = combined_df.dropna()

        # OR

        # **Option 2: Fill missing values (forward fill or backward fill)**
        # combined_df_cleaned = combined_df.fillna(method='ffill')  # Forward fill
        # combined_df_cleaned = combined_df.fillna(method='bfill')  # Backward fill

        # **Verify the cleaning**
        print("Checking for missing values after cleaning...")
        print(combined_df_cleaned.isnull().sum())

        # **Prepare Data for Correlation Analysis**
        correlation_df = combined_df_cleaned.pivot(index='Date', columns='Ticker', values='Adj Close')
        correlation_matrix = correlation_df.corr()

        # **Identify Strong Correlations**
        # Flatten the correlation matrix and sort by absolute correlation value
        corr_pairs = correlation_matrix.unstack().sort_values(kind="quicksort", ascending=False)

        # Filter out self-correlations (which will always be 1)
        corr_pairs = corr_pairs[corr_pairs < 1]

        # Display the top 10 strongest correlations
        print("Top 10 strongest positive correlations:")
        print(corr_pairs.head(10))

        # Display the top 10 strongest negative correlations
        print("Top 10 strongest negative correlations:")
        print(corr_pairs.tail(10))

    else:
        print("No data was loaded into the DataFrame list.")

