import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
import os
import glob

# Fetch sector data for tickers using yfinance
def fetch_sector_data(tickers):
    sector_data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            sector = info.get('sector', 'Unknown')
            sector_data[ticker] = sector
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            sector_data[ticker] = 'Unknown'
    return sector_data

# Load CSV files, clean data, and merge with sector data
def load_and_clean_data(path, excluded_files):
    all_files = glob.glob(path + "*.csv")
    all_files = [f for f in all_files if os.path.basename(f) not in excluded_files]
    df_list = []
    tickers = []
    
    for file in all_files:
        try:
            ticker = os.path.splitext(os.path.basename(file))[0].split('_')[0]
            df = pd.read_csv(file)
            df['Ticker'] = ticker
            tickers.append(ticker)
            df_list.append(df)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
    
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        combined_df_cleaned = combined_df.dropna()  # Drop rows with missing values
        
        # Fetch sector data and merge it with the DataFrame
        sector_data = fetch_sector_data(tickers)
        combined_df_cleaned['Sector'] = combined_df_cleaned['Ticker'].map(sector_data)
        
        return combined_df_cleaned
    else:
        return None

# Calculate correlation matrix with duplicates removed
def calculate_correlations(combined_df):
    correlation_df = combined_df.pivot(index='Date', columns='Ticker', values='Adj Close')
    correlation_matrix = correlation_df.corr()
    
    # Extract the upper triangle of the correlation matrix (excluding the diagonal)
    upper_triangle_mask = np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
    upper_triangle = correlation_matrix.where(upper_triangle_mask)
    
    # Flatten the matrix and sort by correlation value
    corr_pairs = upper_triangle.unstack().sort_values(kind="quicksort", ascending=False)
    corr_pairs = corr_pairs.dropna()  # Drop any NaN values resulting from filtering

    return corr_pairs

# Filter data by sector/industry
def filter_by_sector(data, sectors):
    return data[data['Sector'].isin(sectors)]

# Time-series correlation calculation
def time_series_correlation(combined_df, tickers, window):
    correlation_df = combined_df.pivot(index='Date', columns='Ticker', values='Adj Close')
    rolling_corr = correlation_df[tickers].rolling(window=window).corr().dropna()
    return rolling_corr

# Calculate the spread between pairs
def calculate_spread(ticker1, ticker2, combined_df):
    pivot_df = combined_df.pivot(index='Date', columns='Ticker', values='Adj Close')
    spread = pivot_df[ticker1] - pivot_df[ticker2]
    return spread

# Streamlit app interface
def main():
    st.title("Enhanced Ticker Correlation Explorer")

    # User input: Path to data files and exclusions
    path = st.text_input("Enter the path to your CSV files:", 'C:/Users/Nick/Desktop/Boost Buddy/css fp/AlgoTrading/')
    excluded_files = ['IRX.csv', 'BRK.B.csv']
    
    # Load and clean data
    st.write("Loading and cleaning data...")
    combined_df = load_and_clean_data(path, excluded_files)
    
    if combined_df is not None:
        st.success("Data loaded successfully!")
        
        # Filter by sector/industry
        st.write("Filter by Sector/Industry:")
        sectors = st.multiselect('Select sectors to include:', combined_df['Sector'].unique())
        if sectors:
            combined_df = filter_by_sector(combined_df, sectors)
        
        # Calculate correlations
        st.write("Calculating correlations...")
        corr_pairs = calculate_correlations(combined_df)
        
        # User input: Correlation threshold
        threshold = st.slider("Select correlation threshold:", min_value=0.0, max_value=1.0, value=0.8, step=0.05)
        
        # Filter correlations based on the threshold
        st.write(f"Displaying correlations greater than {threshold} or less than {-threshold}...")
        filtered_corr = corr_pairs[(corr_pairs >= threshold) | (corr_pairs <= -threshold)]
        
        # Display the filtered correlations
        st.dataframe(filtered_corr.head(50))  # Show the top 50 correlations
        
        # Option to download the correlation data
        st.write("Download correlation data:")
        csv = filtered_corr.to_csv(index=True)
        st.download_button("Download CSV", csv, "filtered_correlations.csv", "text/csv")
        
        # Time-series correlation analysis
        st.write("Time-Series Correlation Analysis:")
        tickers = st.multiselect('Select tickers for time-series correlation:', combined_df['Ticker'].unique())
        window = st.slider("Select rolling window size (in days):", min_value=10, max_value=365, value=30, step=5)
        if len(tickers) == 2:
            rolling_corr = time_series_correlation(combined_df, tickers, window)
            st.line_chart(rolling_corr)
        
        # Spread analysis
        st.write("Spread Analysis:")
        ticker1 = st.selectbox('Select Ticker 1:', combined_df['Ticker'].unique())
        ticker2 = st.selectbox('Select Ticker 2:', combined_df['Ticker'].unique())
        if ticker1 and ticker2:
            spread = calculate_spread(ticker1, ticker2, combined_df)
            st.line_chart(spread)
        
        # Correlation heatmap with data validation
        st.write("Correlation Heatmap:")
        heatmap_data = combined_df.pivot(index='Date', columns='Ticker', values='Adj Close').corr()
        if not heatmap_data.empty:
            sns.heatmap(heatmap_data, annot=False, cmap='coolwarm', linewidths=0.5)
            st.pyplot(plt)
        else:
            st.warning("No valid data to display in the heatmap.")

    else:
        st.error("Failed to load data. Please check the path or file exclusions.")

if __name__ == "__main__":
    main()
















    
