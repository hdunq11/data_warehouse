import pandas as pd
from src.db import db
import src.settings as settings
from datetime import datetime

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]


def c4_total_popcorn_sales_by_weekday_hour():
    # Cấu trúc lưu doanh thu từ bán bắp rang theo ngày và giờ
    popcorn_sales_by_weekday_hour = {day: {hour: 0 for hour in range(24)} for day in range(7)}

    # Tải dữ liệu
    sales_by_time = list(sales_by_time_db.find())
    time_data = {time['time_id']: time for time in time_db.find()}

    # Tính tổng doanh thu từ bắp rang theo ngày và giờ
    for sale in sales_by_time:
        time_dimension = time_data.get(sale['time_dim_id'])

        if time_dimension:
            year = time_dimension.get('year')
            month = time_dimension.get('month')
            day = time_dimension.get('day')
            hour = time_dimension.get('hour')
            popcorn_sales = sale['total_popcorn']

            # Chuyển đổi ngày thành ngày trong tuần (0-6, với 0 là Thứ Hai và 6 là Chủ Nhật)
            try:
                weekday = datetime(year, month, day).weekday()
            except ValueError:
                print(f"Warning: Invalid date {year}-{month}-{day} in sale record {sale}")
                continue

            # Kiểm tra nếu giờ nằm trong phạm vi hợp lệ (0-23)
            if 0 <= hour <= 23:
                popcorn_sales_by_weekday_hour[weekday][hour] += popcorn_sales
            else:
                print(f"Warning: Invalid hour {hour} in sale record {sale}")

    # Chuyển đổi dữ liệu và lưu thành CSV
    rows = []
    for weekday, hours in popcorn_sales_by_weekday_hour.items():
        for hour, total_sales in hours.items():
            rows.append({
                "Weekday": weekday,
                "Hour": hour,
                "Total_Popcorn_Sales": total_sales
            })

    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c4_total_popcorn_sales_by_weekday_hour.csv', index=False)
