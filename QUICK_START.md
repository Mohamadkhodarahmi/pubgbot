# راهنمای سریع شروع

## نصب سریع (5 دقیقه)

### 1. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### 2. تنظیم .env
فایل `.env.example` را کپی کرده و به `.env` تغییر نام دهید، سپس مقادیر زیر را تنظیم کنید:

```env
BOT_TOKEN=توکن_ربات_تلگرام
ADMIN_IDS=شناسه_تلگرام_شما
ZARINPAL_MERCHANT_ID=شناسه_مرچنت_زرینپال
ZARINPAL_CALLBACK_URL=https://yourdomain.com/payment/callback
```

### 3. راه‌اندازی دیتابیس
```bash
python setup_db.py
```

### 4. اجرای ربات
```bash
python bot.py
```

### 5. اجرای پنل مدیریت (اختیاری)
```bash
python admin_panel.py
```

## استفاده اولیه

1. ربات را در تلگرام پیدا کنید و `/start` بزنید
2. از پنل مدیریت، ثبت‌نام را باز کنید
3. قیمت را تنظیم کنید
4. کاربران می‌توانند ثبت‌نام کنند

## نکات مهم

- در حالت sandbox، از کارت‌های تست استفاده کنید
- برای production، `ZARINPAL_SANDBOX=false` تنظیم کنید
- فایل `.env` را هرگز commit نکنید

## پشتیبانی

برای راهنمای کامل، فایل `INSTALLATION_FA.md` را مطالعه کنید.

