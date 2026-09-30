import pandas as pd
import numpy as np

# Location of the original Excel dataset
input_file = "data/raw/ApexPlanet_DataAnalytics_Dataset.xlsx"

# Read the Excel file
df = pd.read_excel(input_file)

print("Dataset loaded successfully!")

# Display basic information about the dataset
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nFirst 5 rows:")
print(df.head())

# Examine the dataset structure and summary statistics
print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset information:")
df.info()

print("\nStatistical summary:")
print(df.describe())

# Check unique values
print("\nUnique values:")
print(df.nunique())

# Check Missing Values
print("\nMissing values:")
print(df.isnull().sum())

# Check for duplicate rows
print("\nDuplicate rows:")
print(df.duplicated().sum())

# Check for duplicate Order IDs
print("\nDuplicate Order IDs:")
print(df["Order_ID"].duplicated().sum())

# Check data types of each column
print("\nData types:")
print(df.dtypes)

# Convert "Order_Date" to datetime format
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

print("\nOrder Date data type:")
print(df["Order_Date"].dtype)

#Clean missing Age values by filling them with the median age
age_median = df["Age"].median()
print("Median Age:", age_median)

df["Age"] = df["Age"].fillna(age_median)

print("Missing Age after cleaning:")
print(df["Age"].isnull().sum())

# Clean missing City values by filling them with "Unknown"
df["City"] = df["City"].fillna("Unknown")

print("Missing City after cleaning:")
print(df["City"].isnull().sum())

#Standardize text
text_columns = [
    "Gender",
    "City",
    "Product",
    "Category"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Extract Year, Month, Month Name, and Quarter from "Order_Date"
df["Order_Year"] = df["Order_Date"].dt.year

df["Order_Month"] = df["Order_Date"].dt.month

df["Order_Month_Name"] = df["Order_Date"].dt.strftime("%B")

df["Order_Quarter"] = df["Order_Date"].dt.quarter

# Add a new column "Transaction_ID" with unique identifiers
df.insert(
    0,
    "Transaction_ID",
    ["TXN" + str(i).zfill(6) for i in range(1, len(df) + 1)]
)

# Validate the "Total_Sales" column by comparing it with the calculated sales
calculated_sales = df["Quantity"] * df["Unit_Price"]

sales_mismatch = ~np.isclose(
    df["Total_Sales"],
    calculated_sales,
    rtol=1e-5,
    atol=0.02
)

print("Sales calculation mismatches:",
      sales_mismatch.sum())

# Detect outliers in the "Total_Sales" column using the IQR method
def detect_outliers(data, column):

    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = (
        (data[column] < lower_limit) |
        (data[column] > upper_limit)
    )

    return outliers, lower_limit, upper_limit

sales_outliers, lower, upper = detect_outliers(
    df,
    "Total_Sales"
)

print("Number of Total Sales outliers:",
      sales_outliers.sum())

print("Lower limit:", lower)
print("Upper limit:", upper)

df["Sales_Outlier"] = sales_outliers

# Save the cleaned dataset to a CSV file
output_file = "data/cleaned/cleaned_sales_dataset.csv"

df.to_csv(output_file, index=False)

print("\nCleaned dataset saved successfully!")
print("Location:", output_file)