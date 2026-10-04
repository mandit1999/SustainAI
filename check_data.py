import pandas as pd

# Load dataset
df = pd.read_csv("data/facility_data.csv")

print("=" * 50)
print("SUSTAINAI DATA QUALITY CHECK")
print("=" * 50)

# Number of rows and columns
print("\n1. Dataset Shape")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Column names
print("\n2. Columns")
for column in df.columns:
    print("-", column)

# Missing values
print("\n3. Missing Values")
print(df.isnull().sum())

# Duplicate rows
print("\n4. Duplicate Rows")
print(df.duplicated().sum())

# Facilities
print("\n5. Facilities")
print(df["facility_name"].unique())

# Cities
print("\n6. Cities")
print(df["city"].unique())

# Facility types
print("\n7. Facility Types")
print(df["facility_type"].unique())

# Date range
print("\n8. Date Range")
print("Start:", df["date"].min())
print("End:", df["date"].max())

# Basic statistics
print("\n9. Numerical Statistics")
print(df.describe())

print("\n" + "=" * 50)
print("DATA CHECK COMPLETED")
print("=" * 50)