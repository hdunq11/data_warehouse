import pandas as pd
from src.db import db
import src.settings as settings
from datetime import datetime

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]


def c2_rev_by_weekday_hour():
    # Khởi tạo cấu trúc lưu doanh thu theo ngày trong tuần và giờ
    revenue_by_weekday_hour = {day: {hour: 0 for hour in range(24)} for day in range(7)}

    # Tải dữ liệu một lần
    sales_by_time = list(sales_by_time_db.find())
    time_data = {time['time_id']: time for time in time_db.find()}

    # Tính toán doanh thu theo ngày trong tuần và giờ
    for sale in sales_by_time:
        time_dimension = time_data.get(sale['time_dim_id'])

        if time_dimension:
            year = time_dimension.get('year')
            month = time_dimension.get('month')
            day = time_dimension.get('day')
            hour = time_dimension.get('hour')
            try:
                weekday = datetime(year, month, day).weekday()
            except ValueError:
                print(f"Warning: Invalid date {year}-{month}-{day} in sale record {sale}")
                continue

            if 0 <= hour <= 23:
                revenue_by_weekday_hour[weekday][hour] += sale['total_sales']
            else:
                print(f"Warning: Invalid hour {hour} in sale record {sale}")

    # Chuẩn bị dữ liệu và lưu thành CSV
    rows = []
    for weekday, hours in revenue_by_weekday_hour.items():
        for hour, revenue in hours.items():
            rows.append({
                "Weekday": weekday,
                "Hour": int(hour),
                "Revenue": revenue
            })

    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c2_rev_by_weekday_hour.csv', index=False)
