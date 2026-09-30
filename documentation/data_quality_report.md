# Data Quality Assessment Report

## Dataset Overview

The dataset contains 1,000 sales transactions
and 12 original variables.

## Missing Values

The initial assessment identified:

- Age: 20 missing values
- City: 13 missing values

## Duplicate Records

No exact duplicate rows were identified.

Duplicate Order_ID values were identified.
These records were retained because they contained
different transaction information.

## Data Type Issues

Order_Date was initially stored as an object/text
field and was converted to datetime.

## Data Cleaning

- Missing Age values were replaced using median imputation.
- Missing City values were replaced with "Unknown".
- Text fields were standardized.
- Order_Date was converted to datetime.

## Outlier Detection

Potential outliers in Total_Sales were identified
using the IQR method.

The outliers were flagged rather than deleted.

## Feature Engineering

The following columns were created:

- Transaction_ID
- Order_Year
- Order_Month
- Order_Month_Name
- Order_Quarter
- Sales_Outlier

## Validation

Total Sales was checked against:

Quantity × Unit Price

The calculation was found to be consistent.

## Conclusion

The cleaned dataset is ready for further analysis.