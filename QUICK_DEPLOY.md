# راهنمای سریع دیپلوی

## ⚠️ نکته مهم

**هاست‌های اشتراکی (cPanel/DirectAdmin) معمولاً برای ربات‌های تلگرام مناسب نیستند** چون ربات باید 24/7 اجرا باشد.

## ✅ بهترین راه‌حل: استفاده از سرویس‌های رایگان

### روش 1: Railway (توصیه می‌شود - رایگان)

1. **ایجاد اکانت:**
   - به [railway.app](https://railway.app) بروید
   - با GitHub وارد شوید

2. **دیپلوی:**
   - روی "New Project" کلیک کنید
   - "Deploy from GitHub repo" را انتخاب کنید
   - repository خود را انتخاب کنید
   - Railway به صورت خودکار دیپلوی می‌کند

3. **تنظیم متغیرهای محیطی:**
   - در dashboard، به "Variables" بروید
   - متغیرهای زیر را اضافه کنید:
     - `BOT_TOKEN`
     - `ADMIN_IDS`
     - `ZARINPAL_MERCHANT_ID`
     - و سایر متغیرها از فایل `env.example`

4. **اجرای setup:**
   - در "Deployments" یک shell باز کنید
   - دستور `python setup_db.py` را اجرا کنید

### روش 2: Render (رایگان)

1. **ایجاد اکانت:**
   - به [render.com](https://render.com) بروید
   - با GitHub وارد شوید

2. **دیپلوی:**
   - "New +" → "Background Worker"
   - Repository را انتخاب کنید
   - تنظیمات:
     - Build Command: `pip install -r requirements.txt && python setup_db.py`
     - Start Command: `python bot.py`

3. **تنظیم متغیرهای محیطی:**
   - در "Environment" متغیرها را اضافه کنید

### روش 3: Heroku (رایگان با محدودیت)

1. **نصب Heroku CLI:**
   ```bash
   # Windows: از heroku.com دانلود کنید
   # Linux/Mac:
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **ورود:**
   ```bash
   heroku login
   ```

3. **ایجاد اپ:**
   ```bash
   heroku create your-app-name
   ```

4. **تنظیم متغیرها:**
   ```bash
   heroku config:set BOT_TOKEN=your_token
   heroku config:set ADMIN_IDS=123456789
   # و سایر متغیرها
   ```

5. **دیپلوی:**
   ```bash
   git push heroku main
   ```

6. **اجرای setup:**
   ```bash
   heroku run python setup_db.py
   ```

## 🔧 اگر هاست شما VPS است

### مراحل:

1. **اتصال SSH:**
   ```bash
   ssh username@your-server-ip
   ```

2. **نصب Python:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

3. **آپلود فایل‌ها:**
   - از طریق FTP یا SCP
   - یا از cPanel File Manager

4. **تنظیم محیط:**
   ```bash
   cd /path/to/pubgbot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **ایجاد فایل .env:**
   ```bash
   cp env.example .env
   nano .env
   # مقادیر را تنظیم کنید
   ```

6. **راه‌اندازی دیتابیس:**
   ```bash
   python setup_db.py
   ```

7. **اجرای با screen:**
   ```bash
   screen -S bot
   python bot.py
   # برای خروج: Ctrl+A سپس D
   ```

## 📝 ایجاد فایل .env

فایل `.env` را از `env.example` کپی کنید:

```bash
cp env.example .env
```

سپس مقادیر را ویرایش کنید:
- `BOT_TOKEN`: توکن ربات از @BotFather
- `ADMIN_IDS`: شناسه تلگرام شما
- `ZARINPAL_MERCHANT_ID`: شناسه مرچنت زرین‌پال
- و سایر تنظیمات

## 🚀 دیپلوی پنل مدیریت روی هاست ابری

پنل مدیریت (Flask) را می‌توانید روی هاست ابری اجرا کنید:

### در cPanel:

1. **Python App ایجاد کنید:**
   - در cPanel، "Setup Python App" را پیدا کنید
   - Python version را انتخاب کنید
   - App directory را تنظیم کنید

2. **فایل `passenger_wsgi.py` ایجاد کنید:**
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.dirname(__file__))
   os.chdir(os.path.dirname(__file__))
   from admin_panel import app as application
   ```

3. **نصب وابستگی‌ها:**
   - در Virtual Environment:
   ```bash
   pip install -r requirements.txt
   ```

4. **تنظیم .env:**
   - فایل `.env` را در root directory قرار دهید

## 💡 توصیه

**بهترین روش:**
- ربات را روی Railway/Render اجرا کنید (رایگان)
- پنل مدیریت را روی هاست ابری خود اجرا کنید (اگر امکان دارد)

یا:
- همه چیز را روی یک VPS ارزان اجرا کنید ($5/ماه)

## 📞 کمک بیشتر

برای جزئیات بیشتر، فایل `DEPLOY_HOSTING.md` را مطالعه کنید.

