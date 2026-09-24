import pandas as pd

print("1. Loading combined datasets...")
df_listings = pd.read_csv("CRMLSListing_Combined.csv", low_memory=False)
df_sold = pd.read_csv("CRMLSSold_Combined.csv", low_memory=False)

# --- TASK A: Dataset Understanding & Property Type Filtering ---
print("\n--- DATASET UNDERSTANDING ---")
print(f"Listings initial shape: {df_listings.shape}")
print(f"Sold initial shape: {df_sold.shape}")

print("\nUnique Property Types in Sold dataset:")
print(df_sold["PropertyType"].unique())

# Filter for residential properties (adjust column name/value if necessary)
df_sold_filtered = df_sold[df_sold["PropertyType"] == "Residential"].copy()
print(f"Sold shape after filtering for 'Residential': {df_sold_filtered.shape}")

# --- TASK B: Missing Value Analysis (>90% missing flag) ---
print("\n--- MISSING VALUE ANALYSIS (Sold Dataset) ---")
null_counts = df_sold_filtered.isnull().sum()
null_percentages = (null_counts / len(df_sold_filtered)) * 100

missing_df = pd.DataFrame(
    {"Missing_Count": null_counts, "Missing_Percentage": null_percentages}
)

# Flag columns with >90% missing values
high_missing_cols = missing_df[missing_df["Missing_Percentage"] > 90]
print(f"Columns with >90% missing values ({len(high_missing_cols)} found):")
print(high_missing_cols)

# --- TASK C: Numeric Distribution Review ---
print("\n--- NUMERIC DISTRIBUTION SUMMARY ---")
target_numeric_fields = ["ClosePrice", "LivingArea", "DaysOnMarket"]

# Ensure numeric types
for col in target_numeric_fields:
  if col in df_sold_filtered.columns:
    df_sold_filtered[col] = pd.to_numeric(df_sold_filtered[col], errors="coerce")

summary_stats = df_sold_filtered[target_numeric_fields].describe(
    percentiles=[0.25, 0.5, 0.75, 0.90, 0.99]
)
print(summary_stats)

# --- TASK D: Save Filtered Datasets ---
output_filename = "CRMLSSold_Residential_Filtered.csv"
df_sold_filtered.to_csv(output_filename, index=False)
print(f"\nSuccessfully saved filtered dataset to {output_filename}")