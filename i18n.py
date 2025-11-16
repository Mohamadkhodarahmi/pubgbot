"""
Internationalization (i18n) module for multi-language support
"""
from typing import Dict

TRANSLATIONS = {
    'fa': {
        'welcome': 'خوش آمدید! 👋\n\nاین ربات برای ثبت‌نام تیم‌ها در کاستروم New State Mobile طراحی شده است.',
        'instructions': '📋 دستورالعمل:\n\n1️⃣ تعداد بازیکنان تیم خود را انتخاب کنید (3 یا 4 نفر)\n2️⃣ نام بازیکنان را وارد کنید\n3️⃣ مبلغ را پرداخت کنید\n4️⃣ پس از تایید، در لیست قرار خواهید گرفت',
        'select_player_count': 'تعداد بازیکنان تیم را انتخاب کنید:',
        'enter_team_name': 'نام تیم را وارد کنید:',
        'enter_player_name': 'نام بازیکن {number} را وارد کنید:',
        'team_saved': '✅ تیم با موفقیت ذخیره شد!',
        'calculating_price': '💰 در حال محاسبه مبلغ...',
        'total_price': 'مبلغ کل: {price:,} تومان',
        'payment_link': '🔗 لینک پرداخت:\n{link}',
        'registration_closed': '❌ ثبت‌نام در حال حاضر بسته است.',
        'capacity_full': '⚠️ ظرفیت پر است. آیا می‌خواهید در لیست انتظار قرار بگیرید؟',
        'waitlist_added': '✅ شما به لیست انتظار اضافه شدید. موقعیت شما: {position}',
        'payment_success': '✅ پرداخت با موفقیت انجام شد!',
        'payment_failed': '❌ پرداخت ناموفق بود.',
        'team_confirmed': '✅ تیم شما تایید شد و در بخش {section} قرار گرفت.',
        'admin_panel': '🔧 پنل مدیریت',
        'open_registration': 'باز کردن ثبت‌نام',
        'close_registration': 'بستن ثبت‌نام',
        'set_price': 'تعیین قیمت',
        'view_registrations': 'مشاهده ثبت‌نام‌ها',
        'view_payments': 'مشاهده پرداخت‌ها',
        'manage_waitlist': 'مدیریت لیست انتظار',
        'export_csv': 'خروجی CSV',
        'back': 'بازگشت',
        'cancel': 'لغو',
        'save': 'ذخیره',
        'edit': 'ویرایش',
        'delete': 'حذف',
        'confirm': 'تایید',
        'yes': 'بله',
        'no': 'خیر',
        'error': '❌ خطا: {message}',
        'invalid_input': 'ورودی نامعتبر است.',
        'team_name_required': 'نام تیم الزامی است.',
        'player_name_required': 'نام بازیکن الزامی است.',
        'select_saved_player': 'بازیکن ذخیره شده را انتخاب کنید یا نام جدید وارد کنید:',
        'enter_manually': '✍️ وارد کردن دستی',
        'no_saved_players': 'هیچ بازیکن ذخیره شده‌ای ندارید.',
        'registration_opened': '✅ ثبت‌نام باز شد.',
        'registration_closed_admin': '✅ ثبت‌نام بسته شد.',
        'price_updated': '✅ قیمت به‌روزرسانی شد: {price:,} تومان',
        'waitlist': 'لیست انتظار',
        'main_menu': 'منوی اصلی',
        'my_teams': 'تیم‌های من',
        'help': 'راهنما',
        'language': 'زبان',
        'timezone': 'منطقه زمانی',
    },
    'en': {
        'welcome': 'Welcome! 👋\n\nThis bot is designed for team registration in New State Mobile custom matches.',
        'instructions': '📋 Instructions:\n\n1️⃣ Select the number of players in your team (3 or 4)\n2️⃣ Enter player names\n3️⃣ Pay the amount\n4️⃣ After confirmation, you will be placed in the list',
        'select_player_count': 'Select the number of players in your team:',
        'enter_team_name': 'Enter team name:',
        'enter_player_name': 'Enter player {number} name:',
        'team_saved': '✅ Team saved successfully!',
        'calculating_price': '💰 Calculating price...',
        'total_price': 'Total amount: {price:,} Rials',
        'payment_link': '🔗 Payment link:\n{link}',
        'registration_closed': '❌ Registration is currently closed.',
        'capacity_full': '⚠️ Capacity is full. Would you like to be added to the waitlist?',
        'waitlist_added': '✅ You have been added to the waitlist. Your position: {position}',
        'payment_success': '✅ Payment successful!',
        'payment_failed': '❌ Payment failed.',
        'team_confirmed': '✅ Your team has been confirmed and placed in section {section}.',
        'admin_panel': '🔧 Admin Panel',
        'open_registration': 'Open Registration',
        'close_registration': 'Close Registration',
        'set_price': 'Set Price',
        'view_registrations': 'View Registrations',
        'view_payments': 'View Payments',
        'manage_waitlist': 'Manage Waitlist',
        'export_csv': 'Export CSV',
        'back': 'Back',
        'cancel': 'Cancel',
        'save': 'Save',
        'edit': 'Edit',
        'delete': 'Delete',
        'confirm': 'Confirm',
        'yes': 'Yes',
        'no': 'No',
        'error': '❌ Error: {message}',
        'invalid_input': 'Invalid input.',
        'team_name_required': 'Team name is required.',
        'player_name_required': 'Player name is required.',
        'select_saved_player': 'Select a saved player or enter a new name:',
        'enter_manually': '✍️ Enter Manually',
        'no_saved_players': 'You have no saved players.',
        'registration_opened': '✅ Registration opened.',
        'registration_closed_admin': '✅ Registration closed.',
        'price_updated': '✅ Price updated: {price:,} Rials',
        'waitlist': 'Waitlist',
        'main_menu': 'Main Menu',
        'my_teams': 'My Teams',
        'help': 'Help',
        'language': 'Language',
        'timezone': 'Timezone',
    }
}


def get_text(key: str, language: str = 'fa', **kwargs) -> str:
    """Get translated text"""
    lang = language if language in TRANSLATIONS else 'fa'
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS['fa'].get(key, key))
    return text.format(**kwargs) if kwargs else text


def get_user_language(user_id: int, db) -> str:
    """Get user's preferred language"""
    from database import User
    user = db.query(User).filter(User.telegram_id == user_id).first()
    return user.language if user and user.language else 'fa'

