# استخدام إصدار ثابت من بايثون
FROM python:3.11.9-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY . .

# أمر التشغيل
CMD ["python", "bot.py"]
