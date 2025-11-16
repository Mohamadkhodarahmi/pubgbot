# مراحل نصب و راه‌اندازی روی سرور

## مشکل: ModuleNotFoundError

اگر با خطای `ModuleNotFoundError: No module named 'sqlalchemy'` مواجه شدید، مراحل زیر را انجام دهید:

## ✅ راه‌حل

### 1. فعال کردن محیط مجازی (venv)

```bash
cd /home/pubgbot
source venv/bin/activate
```

**نکته مهم:** بعد از فعال کردن venv، باید `(venv)` در ابتدای خط فرمان شما ظاهر شود.

### 2. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

یا اگر pip3 استفاده می‌کنید:

```bash
pip3 install -r requirements.txt
```

### 3. بررسی نصب

```bash
pip list | grep sqlalchemy
```

باید `sqlalchemy` را ببینید.

### 4. اجرای setup_db

```bash
python setup_db.py
```

یا:

```bash
python3 setup_db.py
```

## 📋 مراحل کامل (از ابتدا)

اگر از ابتدا شروع می‌کنید:

```bash
# 1. رفتن به پوشه پروژه
cd /home/pubgbot

# 2. ایجاد محیط مجازی (اگر ایجاد نشده)
python3 -m venv venv

# 3. فعال کردن محیط مجازی
source venv/bin/activate

# 4. به‌روزرسانی pip
pip install --upgrade pip

# 5. نصب وابستگی‌ها
pip install -r requirements.txt

# 6. کپی فایل .env (اگر وجود ندارد)
cp env.example .env

# 7. ویرایش فایل .env
nano .env

# 8. راه‌اندازی دیتابیس
python setup_db.py

# 9. تست ربات
python bot.py
```

## 🔍 عیب‌یابی

### مشکل: venv فعال نمی‌شود

```bash
# بررسی وجود venv
ls -la venv/

# اگر وجود ندارد، ایجاد کنید
python3 -m venv venv
source venv/bin/activate
```

### مشکل: pip install خطا می‌دهد

```bash
# به‌روزرسانی pip
pip install --upgrade pip

# نصب مجدد
pip install -r requirements.txt
```

### مشکل: python3 پیدا نمی‌شود

```bash
# نصب Python
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

## ✅ چک‌لیست

- [ ] Python3 نصب است (`python3 --version`)
- [ ] pip نصب است (`pip --version`)
- [ ] venv ایجاد شده (`ls venv/`)
- [ ] venv فعال است (باید `(venv)` ببینید)
- [ ] وابستگی‌ها نصب شده (`pip list`)
- [ ] فایل .env تنظیم شده
- [ ] setup_db.py اجرا شده
- [ ] ربات تست شده

## 💡 نکته مهم

**همیشه قبل از اجرای دستورات Python، venv را فعال کنید:**

```bash
source venv/bin/activate
```

اگر venv فعال نباشد، Python از کتابخانه‌های سیستم استفاده می‌کند که ممکن است نصب نباشند.


