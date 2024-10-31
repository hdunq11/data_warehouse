import pandas as pd
from src.db import db
import src.settings as settings
from datetime import datetime

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]

def c5_ticket_sales_by_day():
    # Cấu trúc lưu số lượng vé theo ngày trong tuần
    sales_by_day = {day: 0 for day in range(7)}

    # Tải dữ liệu
    sales_by_time = list(sales_by_time_db.find())
    time_data = {time['time_id']: time for time in time_db.find()}

    # Tính tổng số lượng vé theo ngày trong tuần
    for sale in sales_by_time:
        time_dimension = time_data.get(sale['time_dim_id'])
        if time_dimension:
            year = time_dimension.get('year')
            month = time_dimension.get('month')
            day = time_dimension.get('day')
            try:
                weekday = datetime(year, month, day).weekday()
            except ValueError:
                print(f"Warning: Invalid date {year}-{month}-{day} in sale record {sale}")
                continue
            sales_by_day[weekday] += sale['total_ticket']

    rows = [{"Weekday": day, "Tickets_Sold": qty} for day, qty in sales_by_day.items()]
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c5_ticket_sales_by_day.csv', index=False)
