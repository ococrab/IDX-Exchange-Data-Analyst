import glob
import pandas as pd

# Look inside the 'csv' subfolder for the files
listing_files = sorted(glob.glob("csv/CRMLSListing*.csv"))
print(f"Found {len(listing_files)} listing files.")

if listing_files:
  df_listings = pd.concat(
      [pd.read_csv(f) for f in listing_files], ignore_index=True
  )
  df_listings.to_csv("CRMLSListing_Combined.csv", index=False)
  print("Saved CRMLSListing_Combined.csv successfully!")

sold_files = sorted(glob.glob("csv/CRMLSSold*.csv"))
print(f"Found {len(sold_files)} sold files.")

if sold_files:
  df_sold = pd.concat([pd.read_csv(f) for f in sold_files], ignore_index=True)
  df_sold.to_csv("CRMLSSold_Combined.csv", index=False)
  print("Saved CRMLSSold_Combined.csv successfully!")