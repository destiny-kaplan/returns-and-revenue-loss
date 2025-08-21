
# Importing libraries
import pandas as pd
import numpy as np

# Import CSV File
df = pd.read_csv("C:\\Users\\Admin\\Documents\\Portfolio Case Studies\\Data Cleaning and Transformation\\online_sales_dataset.csv")

# Checking the data types
print("Data Types:")
print(df.dtypes)
print("\n")

# Checking the number of unique values for each column
print("Number of Unique Values:")
print(df.nunique())

# Checking Category and Description for mismatched data
desc_category_check_all = (
    df.groupby('Description')['Category']
    .nunique()
    .reset_index(name='CategoryCount')
    .sort_values('CategoryCount', ascending=False)
)

# Checking descriptions appearing in more than one category
misaligned_desc_all = desc_category_check_all[desc_category_check_all['CategoryCount'] > 1]

print("\n--- Descriptions appearing in multiple categories ---")
print(misaligned_desc_all)

# Getting the Top 2 descriptions per category
top2_per_category_all = (
    df.groupby(['Category', 'Description'])
    .size()
    .reset_index(name='Count')
    .sort_values(['Category', 'Count'], ascending=[True, False])
    .groupby('Category')
    .head(2)
    .reset_index(drop=True)
)

print("\n--- Top 2 Descriptions per Category (ALL ORDERS) ---")
print(top2_per_category_all)

# Checking SKU/StockCode for mismatched Descriptions
duplicate_descriptions = df[df.duplicated('Description', keep=False)].sort_values('Description')
duplicate_stockcodes = df[df.duplicated('StockCode', keep=False)].sort_values('StockCode')

print("\n--- Duplicate Descriptions ---")
print(duplicate_descriptions[['Description', 'Category']].drop_duplicates())

print("\n--- Duplicate StockCodes ---")
print(duplicate_stockcodes[['StockCode', 'Description', 'Category']].drop_duplicates())

# Correcting bad data to ensure that StockCode, Description, and Category are aligned
update_map = {
    "Backpack":         ("SKU_1000", "Backpack", "Accessories"),
    "Wall Clock":       ("SKU_1001", "Wall Clock", "Accessories"),
    "White Mug":        ("SKU_1002", "White Mug", "Accessories"),
    "T-shirt":          ("SKU_2000", "T-shirt", "Apparel"),
    "Headphones":       ("SKU_3000", "Headphones", "Electronics"),
    "USB Cable":        ("SKU_3001", "USB Cable", "Electronics"),
    "Wireless Mouse":   ("SKU_3002", "Wireless Mouse", "Electronics"),
    "Desk Lamp":        ("SKU_4000", "Desk Lamp", "Furniture"),
    "Office Chair":     ("SKU_4001", "Office Chair", "Furniture"),
    "Blue Pen":         ("SKU_5000", "Blue Pen", "Stationery"),
    "Notebook":         ("SKU_5001", "Notebook", "Stationery")
}

# Updating SKU, Description, and Category
def update_row(row):
    desc = row['Description']
    if desc in update_map:
        row['StockCode'], row['Description'], row['Category'] = update_map[desc]
    return row

df = df.apply(update_row, axis=1)

# Removing "SKU_" from StockCode for ease of analysis
df["StockCode"] = df["StockCode"].astype(str).str.replace("SKU_", "", regex=False)

# Separate InvoiceDate into two columns - one for Date and one for Time
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Year"] = df["InvoiceDate"].dt.year  # Extract Year for analysis

# Remove any rows where Year is 2025
df = df[df["Year"] != 2025]

# Correct Date/Time format
invoice_time = df["InvoiceDate"].dt.strftime("%H:%M")  # HH:MM 24-hour format
df["InvoiceDate"] = df["InvoiceDate"].dt.date  # Keep only date
df.insert(df.columns.get_loc("InvoiceDate") + 1, "InvoiceTime", invoice_time)

# Rounding Discount column to two decimal places
df["Discount"] = df["Discount"].apply(lambda x: np.floor(x * 100) / 100)

# Saving updated data to new file
df.to_csv("updated_data_file.csv", index=False)
print("\n File saved as updated_data_file.csv")