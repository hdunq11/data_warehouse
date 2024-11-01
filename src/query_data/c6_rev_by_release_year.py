from platform import release

import pandas as pd
from src.db import db
import src.settings as settings

film_db = db["films"]
transaction_db = db["transaction"]

def c6_rev_by_release_year():

    transaction = list(transaction_db.find())

    # Truy vấn transaction
    for item in transaction:
        film = film_db.find_one({'show_id': item['film_id']})
        item['film'] = film

    release_year_revenue = {}
    for item in transaction:
        year = item['film']["release_year"]
        if year in release_year_revenue:
            release_year_revenue[year]["quantity"] += 1
            release_year_revenue[year]["total"] += item['total']
        else:
            release_year_revenue[year] = {"quantity": 1, "total": item['total']}


    # Chuẩn bị dữ liệu cho CSV
    rows = []
    for index, data in release_year_revenue.items():
        rows.append({
            "Release_year": index,
            "Quantity": data["quantity"],
            "Total_Revenue": data["total"]
        })

    # Chuyển đổi sang DataFrame và lưu thành CSV
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'release_year_revenue.csv', index=False)


# Call the function to execute the script
c6_rev_by_release_year()