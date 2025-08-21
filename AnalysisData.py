# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Importing CSV File
df = pd.read_csv("C:\\Users\\Admin\\Documents\\Portfolio Case Studies\\Data Cleaning and Transformation\\updated_data_file.csv")

# Create LossOfRevenue column for returns only
df['LossOfRevenue'] = (df['UnitPrice'] + df['ShippingCost']) * df['Quantity']

# Count of ReturnStatus column
return_status_counts = df['ReturnStatus'].value_counts()

# Summary of Returned orders by CustomerID, Description, Category, SalesChannel, and OrderPriority
returned_df = df[df['ReturnStatus'] == 'Returned']

count_by_description = returned_df['Description'].value_counts()
count_by_customer = returned_df['CustomerID'].value_counts()
count_by_category = returned_df['Category'].value_counts()
count_by_saleschannel = returned_df['SalesChannel'].value_counts()
count_by_orderpriority = returned_df['OrderPriority'].value_counts()

# Loss of revenue per Category and Description
loss_by_category = (
    returned_df.groupby('Category')['LossOfRevenue']
    .sum()
    .reset_index()
    .sort_values('LossOfRevenue', ascending=False)
)

loss_by_description = (
    returned_df.groupby('Description')['LossOfRevenue']
    .sum()
    .reset_index()
    .sort_values('LossOfRevenue', ascending=False)
)

# Estimated Loss of Revenue on Returns by Year
loss_by_year = (
    returned_df.groupby('Year')['LossOfRevenue']
    .sum()
    .reset_index()
    .sort_values('LossOfRevenue', ascending=False)
)

# Count of Returns per Year per Category
returns_year_category = (
    returned_df.groupby(['Year', 'Category'])
    .size()
    .reset_index(name='Count')
    .sort_values('Count', ascending=False)
)

# Pivot table for plotting visualizations
pivot_returns = returns_year_category.pivot(index='Year', columns='Category', values='Count').fillna(0)

# Most Returned Description per Category
most_returned_per_category = (
    returned_df
    .groupby(['Category', 'Description'])
    .size()
    .reset_index(name='Count')
    .sort_values(['Category', 'Count'], ascending=[True, False])
    .groupby('Category')
    .head(1)
    .reset_index(drop=True)
)

# Visualizations

# Trend of Returns by Category
plt.figure(figsize=(10, 6))
for category in pivot_returns.columns:
    plt.plot(pivot_returns.index, pivot_returns[category], marker='o', label=category)

plt.title("Trend of Returns by Category")
plt.xlabel("Year")
plt.ylabel("Number of Returns")
plt.legend(title="Category")
plt.grid(True)

# Force x-axis to show only integer years
plt.xticks(ticks=range(int(pivot_returns.index.min()), int(pivot_returns.index.max()) + 1))

plt.tight_layout()
plt.savefig("trend_of_returns_by_category.png", dpi=300, bbox_inches="tight")
plt.show()

# Loss of Revenue by Category (Bar Chart)
plt.figure(figsize=(8, 5))
sns.barplot(
    data=loss_by_category,
    x='LossOfRevenue',
    y='Category',
    hue='Category',
    palette='Reds_r',
    legend=False
)

plt.title("Loss of Revenue by Category")
plt.xlabel("Loss of Revenue (in Millions)")
plt.ylabel("Category")

# Format x-axis in millions with $ sign
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x*1e-6:,.1f}M"))

plt.tight_layout()
plt.savefig("loss_of_revenue_by_category.png", dpi=300, bbox_inches="tight")
plt.show()

# Top Returned Descriptions (Bar Chart)
plt.figure(figsize=(8, 5))
count_by_description.head(10).plot(kind='barh', color='steelblue')
plt.title("Top 10 Returned Descriptions")
plt.xlabel("Number of Returns")
plt.ylabel("Description")
plt.tight_layout()
plt.savefig("top_10_returned_descriptions.png", dpi=300, bbox_inches="tight")
plt.show()

# Loss of Revenue by Year (Bar Chart)
plt.figure(figsize=(8, 5))
sns.barplot(
    data=loss_by_year,
    x='Year',
    y='LossOfRevenue',
    hue='Year',
    palette='viridis',
    legend=False
)
plt.title("Loss of Revenue by Year")
plt.xlabel("Year")
plt.ylabel("Loss of Revenue")

# Format y-axis in millions with $ sign
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x*1e-6:,.1f}M"))

plt.tight_layout()
plt.savefig("loss_of_revenue_by_year.png", dpi=300, bbox_inches="tight")
plt.show()

# Returns per Year per Category (Stacked Bar Chart)
pivot_returns.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title("Returns per Year per Category (Stacked)")
plt.xlabel("Year")
plt.ylabel("Number of Returns")
plt.tight_layout()
plt.savefig("returns_per_year_per_category_stacked.png", dpi=300, bbox_inches="tight")
plt.show()

# Return Status Breakdown (Pie Chart)
plt.figure(figsize=(6, 6))
return_status_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightgreen'])
plt.title("Return Status Breakdown")
plt.ylabel("")
plt.tight_layout()
plt.savefig("return_status_breakdown.png", dpi=300, bbox_inches="tight")
plt.show()

# Formatting for Currency
def format_currency(x):
    if isinstance(x, (int, float)):
        return f"${x:,.2f}"
    return x

# Display results in console
print("\n--- Total Count of ReturnStatus ---")
print(return_status_counts)

print("\n--- Count of Returned Orders by Description ---")
print(count_by_description)

print("\n--- Count of Returned Orders by CustomerID ---")
print(count_by_customer)

print("\n--- Count of Returned Orders by Category ---")
print(count_by_category)

print("\n--- Count of Returned Orders by SalesChannel ---")
print(count_by_saleschannel)

print("\n--- Count of Returned Orders by OrderPriority ---")
print(count_by_orderpriority)

print("\n--- Estimated Loss of Revenue by Category ---")
print(loss_by_category)

print("\n--- Estimated Loss of Revenue by Description ---")
print(loss_by_description)

print("\n--- Estimated Loss of Revenue on Returns by Year ---")
print(loss_by_year)

print("\n--- Count of Returns per Year per Category ---")
print(returns_year_category)

print("\n--- Most Returned Description per Category ---")
print(most_returned_per_category)
