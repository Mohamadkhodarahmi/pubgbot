# راهنمای نصب و راه‌اندازی - ربات ثبت‌نام New State Mobile

## پیش‌نیازها

- Python 3.8 یا بالاتر
- pip (مدیر بسته Python)
- حساب کاربری در [Zarinpal](https://zarinpal.com) برای درگاه پرداخت
- یک ربات تلگرام (از [@BotFather](https://t.me/BotFather))

## مراحل نصب

### 1. نصب Python و pip

اگر Python نصب ندارید:
- Windows: از [python.org](https://www.python.org/downloads/) دانلود کنید
- Linux: `sudo apt install python3 python3-pip`
- Mac: `brew install python3`

### 2. دانلود و استخراج پروژه

پروژه را دانلود کرده و در یک پوشه استخراج کنید.

### 3. نصب وابستگی‌ها

در ترمینال/CMD، به پوشه پروژه بروید و دستور زیر را اجرا کنید:

```bash
pip install -r requirements.txt
```

**نکته:** در برخی سیستم‌ها ممکن است نیاز به استفاده از `pip3` باشد.

### 4. تنظیم فایل .env

فایل `.env.example` را کپی کرده و به `.env` تغییر نام دهید:

**Windows:**
```cmd
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

سپس فایل `.env` را با یک ویرایشگر متن باز کرده و مقادیر زیر را تنظیم کنید:

#### تنظیمات ضروری:

```env
# توکن ربات تلگرام (از @BotFather دریافت کنید)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# شناسه‌های تلگرام مدیران (با کاما جدا کنید)
ADMIN_IDS=123456789,987654321

# شناسه کانال/گروه مقصد (اختیاری)
TARGET_CHANNEL_ID=@your_channel
TARGET_GROUP_ID=-1001234567890

# شناسه مرچنت زرین‌پال
ZARINPAL_MERCHANT_ID=your_merchant_id_here

# آدرس callback برای پرداخت (باید قابل دسترسی از اینترنت باشد)
ZARINPAL_CALLBACK_URL=https://yourdomain.com/payment/callback

# حالت sandbox (برای تست: true، برای production: false)
ZARINPAL_SANDBOX=true
```

### 5. دریافت توکن ربات تلگرام

1. در تلگرام، به [@BotFather](https://t.me/BotFather) بروید
2. دستور `/newbot` را ارسال کنید
3. نام ربات را وارد کنید
4. username ربات را وارد کنید (باید به `bot` ختم شود)
5. توکن دریافتی را در فایل `.env` در قسمت `BOT_TOKEN` قرار دهید

### 6. دریافت شناسه تلگرام خود

برای دریافت شناسه تلگرام خود:
1. به [@userinfobot](https://t.me/userinfobot) بروید
2. شناسه عددی خود را کپی کنید
3. در فایل `.env` در قسمت `ADMIN_IDS` قرار دهید

### 7. راه‌اندازی دیتابیس

دستور زیر را اجرا کنید تا دیتابیس و تنظیمات اولیه ایجاد شود:

```bash
python setup_db.py
```

یا

```bash
python3 setup_db.py
```

### 8. اجرای ربات

برای اجرای ربات، دستور زیر را اجرا کنید:

```bash
python bot.py
```

یا

```bash
python3 bot.py
```

اگر همه چیز درست باشد، پیام "Starting bot..." را خواهید دید.

### 9. اجرای پنل مدیریت (اختیاری)

در یک ترمینال/CMD دیگر، دستور زیر را اجرا کنید:

```bash
python admin_panel.py
```

پنل مدیریت در آدرس `http://localhost:5000/admin` در دسترس خواهد بود.

## تنظیمات پیشرفته

### استفاده از PostgreSQL

1. PostgreSQL را نصب کنید
2. یک دیتابیس ایجاد کنید
3. adapter را نصب کنید:
   ```bash
   pip install psycopg2-binary
   ```
4. در فایل `.env`، `DATABASE_URL` را تغییر دهید:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

### تنظیم Webhook (برای production)

برای استفاده از webhook به جای polling:

1. یک سرور با HTTPS داشته باشید
2. در فایل `.env`، `WEBHOOK_URL` را تنظیم کنید
3. کد ربات را برای استفاده از webhook تغییر دهید

### تنظیم کانال/گروه مقصد

**برای کانال:**
- کانال را ایجاد کنید
- ربات را به عنوان ادمین اضافه کنید
- username کانال را در `TARGET_CHANNEL_ID` قرار دهید (مثلاً: `@mychannel`)

**برای گروه:**
- گروه را ایجاد کنید
- ربات را به گروه اضافه کنید
- شناسه عددی گروه را از ربات‌های دیگر دریافت کنید
- در `TARGET_GROUP_ID` قرار دهید (مثلاً: `-1001234567890`)

## تست ربات

1. ربات را در تلگرام پیدا کنید
2. دستور `/start` را ارسال کنید
3. منوی اصلی را مشاهده کنید
4. یک تیم تستی ثبت کنید

## عیب‌یابی

### ربات کار نمی‌کند

- بررسی کنید که `BOT_TOKEN` درست باشد
- بررسی کنید که تمام وابستگی‌ها نصب شده باشند: `pip install -r requirements.txt`
- لاگ‌های خطا را بررسی کنید

### خطای دیتابیس

- بررسی کنید که Python دسترسی نوشتن در پوشه پروژه دارد
- برای PostgreSQL، اتصال به دیتابیس را بررسی کنید

### پرداخت کار نمی‌کند

- بررسی کنید که `ZARINPAL_MERCHANT_ID` درست باشد
- در حالت sandbox، از کارت‌های تست استفاده کنید
- `ZARINPAL_CALLBACK_URL` باید قابل دسترسی باشد

### پنل مدیریت باز نمی‌شود

- بررسی کنید که پورت 5000 آزاد باشد
- فایروال را بررسی کنید
- لاگ‌های خطا را بررسی کنید

## نکات امنیتی

1. **هرگز فایل `.env` را در Git commit نکنید**
2. در production، `PANEL_SECRET_KEY` را به یک مقدار تصادفی قوی تغییر دهید
3. از HTTPS برای webhook استفاده کنید
4. دسترسی به پنل مدیریت را محدود کنید

## پشتیبانی

در صورت بروز مشکل، لطفاً issue ایجاد کنید یا با توسعه‌دهنده تماس بگیرید.

