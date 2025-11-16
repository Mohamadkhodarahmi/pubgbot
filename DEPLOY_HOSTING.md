# راهنمای دیپلوی روی هاست ابری (cPanel / DirectAdmin)

## ⚠️ نکته مهم

**ربات‌های تلگرام معمولاً نیاز به اجرای دائمی دارند** و روی هاست‌های اشتراکی (shared hosting) که فقط cPanel یا DirectAdmin دارند، **به صورت مستقیم قابل اجرا نیستند** چون:

1. هاست‌های اشتراکی معمولاً Python را به صورت دائمی اجرا نمی‌کنند
2. ربات نیاز به اجرای 24/7 دارد
3. هاست‌های اشتراکی برای وب‌سایت‌ها طراحی شده‌اند نه برای ربات‌ها

## ✅ راه‌حل‌های ممکن

### روش 1: استفاده از VPS (توصیه می‌شود)

اگر هاست ابری شما VPS است (نه shared hosting):

1. **اتصال به سرور از طریق SSH**
2. **نصب Python و pip**
3. **آپلود فایل‌ها**
4. **اجرای ربات با screen یا systemd**

### روش 2: استفاده از Cron Job (محدود)

برخی هاست‌ها اجازه اجرای cron job با Python را می‌دهند، اما این روش **توصیه نمی‌شود** چون:
- ربات باید دائماً اجرا باشد
- Cron job فقط در زمان‌های مشخص اجرا می‌شود

### روش 3: استفاده از سرویس‌های رایگان/ارزان

- **Heroku** (رایگان با محدودیت)
- **Railway** (رایگان)
- **Render** (رایگان)
- **DigitalOcean App Platform** (ارزان)
- **VPS ایرانی** (مثل نوبیتکس، سرورپارس)

## 📋 راهنمای دیپلوی روی VPS (اگر هاست شما VPS است)

### مرحله 1: اتصال به سرور

```bash
ssh username@your-server-ip
```

### مرحله 2: نصب Python و pip

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip
```

### مرحله 3: آپلود فایل‌ها

از طریق FTP یا SCP:

```bash
# از کامپیوتر خود
scp -r pubgbot/* username@your-server-ip:/home/username/pubgbot/
```

یا از طریق cPanel File Manager:
1. وارد cPanel شوید
2. File Manager را باز کنید
3. فایل‌ها را آپلود کنید

### مرحله 4: تنظیم محیط

```bash
cd /home/username/pubgbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### مرحله 5: تنظیم فایل .env

```bash
nano .env
# یا از طریق cPanel File Manager ویرایش کنید
```

مقادیر را تنظیم کنید:
- `BOT_TOKEN`
- `ADMIN_IDS`
- `ZARINPAL_MERCHANT_ID`
- و سایر تنظیمات

### مرحله 6: راه‌اندازی دیتابیس

```bash
python3 setup_db.py
```

### مرحله 7: اجرای ربات با screen (برای اجرای دائمی)

```bash
# نصب screen
sudo apt install screen  # یا yum install screen

# ایجاد یک session جدید
screen -S telegram_bot

# اجرای ربات
python3 bot.py

# برای خروج از screen (بدون بستن ربات): Ctrl+A سپس D
# برای بازگشت: screen -r telegram_bot
```

### مرحله 8: اجرای پنل مدیریت (اختیاری)

در یک screen دیگر:

```bash
screen -S admin_panel
python3 admin_panel.py
```

## 🔧 استفاده از systemd (روش حرفه‌ای)

### ایجاد سرویس برای ربات

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

محتوای زیر را اضافه کنید:

```ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
Type=simple
User=username
WorkingDirectory=/home/username/pubgbot
Environment="PATH=/home/username/pubgbot/venv/bin"
ExecStart=/home/username/pubgbot/venv/bin/python3 /home/username/pubgbot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

فعال‌سازی و اجرا:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

## 🌐 دیپلوی پنل مدیریت روی هاست

پنل مدیریت (Flask) را می‌توانید روی هاست ابری اجرا کنید:

### روش 1: استفاده از Passenger (cPanel)

1. **فایل `passenger_wsgi.py` ایجاد کنید:**

```python
import sys
import os

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.dirname(__file__))

# تغییر به دایرکتوری پروژه
os.chdir(os.path.dirname(__file__))

# import کردن app
from admin_panel import app as application

if __name__ == "__main__":
    application.run()
```

2. **تنظیمات در cPanel:**
   - Python App را فعال کنید
   - مسیر را به دایرکتوری پروژه تنظیم کنید
   - Python version را انتخاب کنید

### روش 2: استفاده از CGI (DirectAdmin)

1. **فایل `app.cgi` ایجاد کنید:**

```python
#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

from admin_panel import app

if __name__ == "__main__":
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(app)
```

2. **اجازه اجرا بدهید:**

```bash
chmod +x app.cgi
```

## 📝 نکات مهم برای هاست ابری

### 1. محدودیت‌های هاست اشتراکی

- **Timeout:** برخی هاست‌ها timeout دارند (مثلاً 30 ثانیه)
- **Memory:** محدودیت حافظه
- **CPU:** محدودیت پردازنده
- **Background Processes:** ممکن است اجازه اجرای background process نداشته باشند

### روش جایگزین: استفاده از سرویس‌های رایگان

#### Heroku (رایگان)

1. **نصب Heroku CLI**
2. **ایجاد `Procfile`:**

```
worker: python bot.py
web: python admin_panel.py
```

3. **دیپلوی:**

```bash
heroku create your-app-name
git push heroku main
```

#### Railway (رایگان)

1. اتصال GitHub repository
2. Railway به صورت خودکار دیپلوی می‌کند
3. متغیرهای محیطی را در dashboard تنظیم کنید

#### Render (رایگان)

1. اتصال GitHub repository
2. انتخاب نوع سرویس (Web Service یا Background Worker)
3. تنظیمات و متغیرهای محیطی

## 🔍 بررسی اینکه هاست شما VPS است یا Shared

### نشانه‌های VPS:
- دسترسی SSH دارید
- می‌توانید systemd استفاده کنید
- می‌توانید screen/tmux استفاده کنید
- دسترسی root یا sudo دارید

### نشانه‌های Shared Hosting:
- فقط cPanel/DirectAdmin دارید
- دسترسی SSH ندارید (یا محدود است)
- نمی‌توانید background process اجرا کنید
- محدودیت‌های زیادی دارید

## 💡 توصیه نهایی

**اگر هاست شما Shared Hosting است:**

1. **از سرویس‌های رایگان استفاده کنید:**
   - Railway (توصیه می‌شود)
   - Render
   - Heroku

2. **یا یک VPS ارزان خریداری کنید:**
   - VPS ایرانی (نوبیتکس، سرورپارس)
   - DigitalOcean ($5/ماه)
   - Vultr ($2.5/ماه)

3. **پنل مدیریت را روی هاست ابری نگه دارید** (اگر امکان دارد)
4. **ربات را روی VPS یا سرویس رایگان اجرا کنید**

## 📞 پشتیبانی

اگر سوالی دارید یا به کمک نیاز دارید، لطفاً issue ایجاد کنید.

