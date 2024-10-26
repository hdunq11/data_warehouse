import pandas as pd
from src import settings
from src.db import db

customer_db = db["customers"]

def import_customer():
    try:
        if customer_db.count_documents({}) != 0:
            customer_db.drop()
    except:
        pass

    df = pd.read_excel(settings.input_path, sheet_name='customer')

    # Extract unique customers
    customers = df[['customerid', 'DOB', 'gender', 'address', 'Website', 'job', 'industry']].drop_duplicates()

    # Convert to dictionary
    customers_dict = customers.to_dict(orient='records')

    print(customers_dict[:5])
    print(len(customers_dict))

    for customer in customers_dict:
        try:
            customer_db.insert_one(customer)
        except:
            pass