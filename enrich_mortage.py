import pandas as pd

print("1. Fetching Mortgage Rate data from FRED...")
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=["observation_date"])
mortgage.columns = ["date", "rate_30yr_fixed"]

print("2. Resampling weekly rates to monthly averages...")
mortgage["year_month"] = mortgage["date"].dt.to_period("M")
mortgage_monthly = (
    mortgage.groupby("year_month")["rate_30yr_fixed"].mean().reset_index()
)

print("3. Loading combined MLS datasets...")
sold = pd.read_csv("CRMLSSold_Combined.csv", low_memory=False)
listings = pd.read_csv("CRMLSListing_Combined.csv", low_memory=False)

print("4. Creating year_month join keys on MLS datasets...")
sold["year_month"] = pd.to_datetime(sold["CloseDate"]).dt.to_period("M")
listings["year_month"] = pd.to_datetime(
    listings["ListingContractDate"]
).dt.to_period("M")

print("5. Merging mortgage rates onto datasets...")
sold_with_rates = sold.merge(mortgage_monthly, on="year_month", how="left")
listings_with_rates = listings.merge(
    mortgage_monthly, on="year_month", how="left"
)

print("6. Validating the merge (checking for null rates)...")
sold_nulls = sold_with_rates["rate_30yr_fixed"].isnull().sum()
listings_nulls = listings_with_rates["rate_30yr_fixed"].isnull().sum()

print(f"Unmatched rows in Sold dataset: {sold_nulls}")
print(f"Unmatched rows in Listings dataset: {listings_nulls}")

# Preview result
print("\nPreview of Sold with Rates:")
print(
    sold_with_rates[
        ["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]
    ].head()
)

print("7. Saving enriched datasets to new CSVs...")
sold_with_rates.to_csv("CRMLSSold_Enriched.csv", index=False)
listings_with_rates.to_csv("CRMLSListing_Enriched.csv", index=False)
print("Successfully saved CRMLSSold_Enriched.csv and CRMLSListing_Enriched.csv!")