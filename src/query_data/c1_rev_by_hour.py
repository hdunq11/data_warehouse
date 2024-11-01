import pandas as pd
from src.db import db
import src.settings as settings

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]

def c1_rev_by_hour():
    # Khởi tạo cấu trúc để lưu doanh thu theo giờ
    revenue_by_hour = {hour: 0 for hour in range(24)}

    # Tải dữ liệu từ MongoDB
    sales_by_time = list(sales_by_time_db.find())
    time_data = {time['time_id']: time for time in time_db.find()}

    # Tính doanh thu theo từng giờ
    for sale in sales_by_time:
        time_dimension = time_data.get(sale['time_dim_id'])
        if time_dimension:
            hour = time_dimension['hour']
            revenue_by_hour[hour] += sale['total_sales']

    # Chuẩn bị dữ liệu để lưu thành CSV
    rows = [{"Hour": hour, "Revenue": revenue} for hour, revenue in revenue_by_hour.items()]
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c1_rev_by_hour.csv', index=False)
