import pandas as pd

"""
Loads raw CSV files and performs basic validation checks:
- required columns
- null values in required fields
- uniqueness of primary keys
- uniqueness of composite keys for order_items
"""

# ----------------------------
# Loading function
# ----------------------------

def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file and remove fully empty rows and columns."""
    df = pd.read_csv(path, sep=';')
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    return df

# ----------------------------
# Validation functions
# ----------------------------

def validate_columns(df, expected_columns, table_name):
    """Check whether a table contains all required columns."""
    for column in expected_columns:
        if column not in df.columns:
            print(f"{table_name}: missing column '{column}'")
            return False

    print(f"{table_name}: columns are valid")
    return True

def validate_no_nulls(df, required_columns, table_name):
    """Check whether required columns contain null values."""
    for column in required_columns:
        if df[column].isnull().any():
            print(f"{table_name}: column '{column}' contains null values")
            return False

    print(f"{table_name}: required columns have no null values")
    return True

def validate_unique(df, key_column, table_name):
    """Check whether a key column contains unique values."""
    if df[key_column].nunique() != len(df):
        print(f"{table_name}: column '{key_column}' is not unique")
        return False
    print(f"{table_name}: column '{key_column}' is unique")
    return True

def validate_composite_unique(df, key_columns, table_name):
    """Check whether a combination of columns is unique."""
    if df.duplicated(subset=key_columns).any():
        print(f"{table_name}: combination {key_columns} is not unique")
        return False

    print(f"{table_name}: combination {key_columns} is unique")
    return True

def validate_ids_format():
    """TODO: implement"""
    pass

def validate_positive():
    """TODO: implement"""
    pass

def validate_price_cost_relation():
    """TODO: implement"""
    pass


# -----------------------------------
# Table-specific validation functions
# -----------------------------------

def validate_categories(df):
    columns_valid = validate_columns(df, ["category_id","category_name"], "categories")
    nulls_valid = validate_no_nulls(df, ["category_id","category_name"], "categories")
    unique_valid = validate_unique(df, "category_id","categories")
    return columns_valid and nulls_valid and unique_valid

def validate_stores(df):
    columns_valid = validate_columns(df,["store_id","store_name","city"], "stores")
    nulls_valid = validate_no_nulls(df,["store_id","store_name", "city"], "stores")
    unique_valid = validate_unique(df,"store_id","stores")
    return columns_valid and nulls_valid and unique_valid

def validate_products(df):
    columns_valid = validate_columns(df,["product_id","product_name","category_id","price","cost","stock"], "products")
    nulls_valid = validate_no_nulls(df,["product_id","product_name","category_id","price","cost","stock"], "products")
    unique_valid = validate_unique(df,"product_id", "products")
    return columns_valid and nulls_valid and unique_valid

def validate_orders(df):
    columns_valid = validate_columns(df,["order_id","store_id","order_date"], "orders")
    nulls_valid = validate_no_nulls(df,["order_id","store_id","order_date"], "orders")
    unique_valid = validate_unique(df,"order_id","orders")
    return columns_valid and nulls_valid and unique_valid

def validate_order_items(df):
    columns_valid = validate_columns(df,["order_item_id","order_id","product_id","line_number","quantity"],"order_items")
    nulls_valid = validate_no_nulls(df,["order_item_id","order_id","product_id","line_number","quantity"],"order_items")
    unique_valid = validate_unique(df,"order_item_id","order_items")
    composite_valid = validate_composite_unique(df,["order_id","line_number"], "order_items")
    return columns_valid and nulls_valid and unique_valid and composite_valid


# ----------------------------
# Load and validate raw tables
# ----------------------------

# Load raw tables
categories = load_csv('../data/raw/categories.csv')
stores = load_csv('../data/raw/stores.csv')
products = load_csv('../data/raw/products.csv')
orders = load_csv('../data/raw/orders.csv')
order_items = load_csv('../data/raw/order_items.csv')

# Validate raw tables
categories_valid = validate_categories(categories)
stores_valid = validate_stores(stores)
products_valid = validate_products(products)
orders_valid = validate_orders(orders)
order_items_valid = validate_order_items(order_items)

# ----------------------------
# Validation summary
# ----------------------------

print("\nValidation summary:")
print(f"categories: {categories_valid}")
print(f"stores: {stores_valid}")
print(f"products: {products_valid}")
print(f"orders: {orders_valid}")
print(f"order_items: {order_items_valid}")