# Sử dụng image Python 3.10-slim
FROM python:3.10-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy file requirements.txt vào container và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn (bao gồm bot_report.py) vào container
COPY . .

# Lệnh mặc định để chạy bot
CMD ["python", "bot_report.py"]
