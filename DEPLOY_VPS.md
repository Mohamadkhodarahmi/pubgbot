# راهنمای کامل دیپلوی روی VPS

## 🔧 مشکل Clone از GitHub

اگر با خطای `Permission denied (publickey)` مواجه شدید، از HTTPS استفاده کنید:

```bash
git clone https://github.com/Mohamadkhodarahmi/pubgbot.git
```

یا اگر repository private است، از token استفاده کنید:

```bash
git clone https://YOUR_TOKEN@github.com/Mohamadkhodarahmi/pubgbot.git
```

## 📋 مراحل کامل دیپلوی روی VPS

### مرحله 1: Clone پروژه

```bash
cd /home
git clone https://github.com/Mohamadkhodarahmi/pubgbot.git
cd pubgbot
```

### مرحله 2: نصب Python و وابستگی‌ها

```bash
# بررسی نسخه Python
python3 --version

# اگر Python نصب نیست:
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# ایجاد محیط مجازی
python3 -m venv venv
source venv/bin/activate

# نصب وابستگی‌ها
pip install -r requirements.txt
```

### مرحله 3: تنظیم فایل .env

```bash
# کپی کردن فایل نمونه
cp env.example .env

# ویرایش فایل .env
nano .env
```

مقادیر مهم را تنظیم کنید:
- `BOT_TOKEN`: توکن ربات از @BotFather
- `ADMIN_IDS`: شناسه تلگرام شما (از @userinfobot بگیرید)
- `ZARINPAL_MERCHANT_ID`: شناسه مرچنت زرین‌پال
- `USE_BYPASS=true`: اگر در ایران هستید
- `TELEGRAM_BYPASS_URL`: آدرس ورکر bypass

### مرحله 4: راه‌اندازی دیتابیس

```bash
python setup_db.py
```

### مرحله 5: تست ربات

```bash
# اجرای ربات برای تست
python bot.py
```

اگر همه چیز درست بود، Ctrl+C بزنید و به مرحله بعد بروید.

### مرحله 6: اجرای دائمی با screen

```bash
# نصب screen (اگر نصب نیست)
sudo apt install screen -y

# ایجاد session جدید
screen -S telegram_bot

# اجرای ربات
cd /home/pubgbot
source venv/bin/activate
python bot.py

# برای خروج از screen (بدون بستن ربات):
# Ctrl+A سپس D را بزنید

# برای بازگشت به screen:
screen -r telegram_bot

# برای دیدن لیست screen ها:
screen -ls
```

### مرحله 7: اجرای با systemd (روش حرفه‌ای)

#### ایجاد فایل سرویس

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

محتوای زیر را اضافه کنید (مسیرها را تغییر دهید):

```ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pubgbot
Environment="PATH=/home/pubgbot/venv/bin"
ExecStart=/home/pubgbot/venv/bin/python3 /home/pubgbot/bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### فعال‌سازی و اجرا

```bash
# بارگذاری مجدد systemd
sudo systemctl daemon-reload

# فعال‌سازی سرویس (اجرای خودکار بعد از reboot)
sudo systemctl enable telegram-bot

# شروع سرویس
sudo systemctl start telegram-bot

# بررسی وضعیت
sudo systemctl status telegram-bot

# مشاهده لاگ‌ها
sudo journalctl -u telegram-bot -f
```

### مرحله 8: اجرای پنل مدیریت (اختیاری)

#### با screen:

```bash
screen -S admin_panel
cd /home/pubgbot
source venv/bin/activate
python admin_panel.py
```

#### با systemd:

```bash
sudo nano /etc/systemd/system/admin-panel.service
```

```ini
[Unit]
Description=Admin Panel Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pubgbot
Environment="PATH=/home/pubgbot/venv/bin"
Environment="FLASK_APP=admin_panel.py"
ExecStart=/home/pubgbot/venv/bin/python3 /home/pubgbot/admin_panel.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable admin-panel
sudo systemctl start admin-panel
```

## 🔐 تنظیم SSH Key برای GitHub (اختیاری)

اگر می‌خواهید از SSH استفاده کنید:

### 1. ایجاد SSH Key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Enter را بزنید (مسیر پیش‌فرض)
# پسورد را خالی بگذارید یا یک پسورد بگذارید
```

### 2. نمایش کلید عمومی

```bash
cat ~/.ssh/id_ed25519.pub
```

### 3. اضافه کردن به GitHub

1. به GitHub بروید
2. Settings → SSH and GPG keys
3. New SSH key
4. کلید را paste کنید

### 4. تست اتصال

```bash
ssh -T git@github.com
```

## 🔍 عیب‌یابی

### مشکل: ربات کار نمی‌کند

```bash
# بررسی لاگ‌ها
sudo journalctl -u telegram-bot -n 50

# یا اگر با screen اجرا کرده‌اید:
screen -r telegram_bot
```

### مشکل: خطای import

```bash
# مطمئن شوید venv فعال است
source venv/bin/activate

# نصب مجدد وابستگی‌ها
pip install -r requirements.txt
```

### مشکل: خطای دیتابیس

```bash
# بررسی دسترسی
ls -la pubg_bot.db

# اگر فایل وجود ندارد:
python setup_db.py
```

### مشکل: خطای .env

```bash
# بررسی وجود فایل
ls -la .env

# اگر وجود ندارد:
cp env.example .env
nano .env
```

## 📝 دستورات مفید

```bash
# توقف سرویس
sudo systemctl stop telegram-bot

# شروع مجدد
sudo systemctl restart telegram-bot

# غیرفعال کردن
sudo systemctl disable telegram-bot

# مشاهده لاگ‌های زنده
sudo journalctl -u telegram-bot -f

# بررسی استفاده از منابع
htop
# یا
top
```

## 🔄 به‌روزرسانی پروژه

```bash
cd /home/pubgbot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart telegram-bot
```

## ✅ چک‌لیست نهایی

- [ ] پروژه clone شده
- [ ] Python و pip نصب شده
- [ ] venv ایجاد و فعال شده
- [ ] وابستگی‌ها نصب شده
- [ ] فایل .env تنظیم شده
- [ ] دیتابیس راه‌اندازی شده
- [ ] ربات تست شده
- [ ] سرویس systemd ایجاد شده (یا screen)
- [ ] ربات در حال اجرا است
- [ ] پنل مدیریت (اختیاری) راه‌اندازی شده

## 📞 کمک بیشتر

اگر مشکلی پیش آمد:
1. لاگ‌ها را بررسی کنید
2. فایل `DEPLOY_HOSTING.md` را مطالعه کنید
3. Issue در GitHub ایجاد کنید



