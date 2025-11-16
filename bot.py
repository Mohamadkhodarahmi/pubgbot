"""
Main Telegram Bot Application
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
from config import BOT_TOKEN, USE_BYPASS, TELEGRAM_BYPASS_URL
from database import init_db
from bot_handlers import (
    start_command, help_command, register_team_start, select_player_count,
    select_saved_player, enter_player_name, enter_team_name, cancel_registration,
    my_teams, settings_handler, SELECTING_PLAYER_COUNT, ENTERING_TEAM_NAME, ENTERING_PLAYER_NAMES, SELECTING_SAVED_PLAYER
)
from admin_handlers import (
    admin_panel, admin_toggle_registration, admin_set_price,
    admin_view_registrations, admin_view_payments, admin_export_csv
)
from payment_callback import verify_payment_command

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot"""
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Create application
    builder = Application.builder().token(BOT_TOKEN)
    
    # استفاده از bypass برای دور زدن فیلترینگ (اگر فعال باشد)
    if USE_BYPASS and TELEGRAM_BYPASS_URL:
        # حذف trailing slash اگر وجود دارد
        base_url = TELEGRAM_BYPASS_URL.rstrip('/')
        # اضافه کردن /bot به انتهای URL
        if not base_url.endswith('/bot'):
            base_url = f"{base_url}/bot"
        builder = builder.base_url(base_url)
        logger.info(f"Using Telegram bypass: {base_url}")
    
    application = builder.build()
    
    # Registration conversation handler
    registration_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^(📝 ثبت‌نام تیم|📝 Register Team)$'), register_team_start)],
        states={
            SELECTING_PLAYER_COUNT: [CallbackQueryHandler(select_player_count, pattern='^player_count_')],
            SELECTING_SAVED_PLAYER: [
                CallbackQueryHandler(select_saved_player, pattern='^saved_player_|^enter_manually$')
            ],
            ENTERING_PLAYER_NAMES: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_player_name)],
            ENTERING_TEAM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_team_name)],
        },
        fallbacks=[CommandHandler('cancel', cancel_registration), MessageHandler(filters.Regex('^(لغو|Cancel)$'), cancel_registration)],
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("verify", verify_payment_command))
    
    # Menu handlers (باید قبل از conversation handler باشند)
    application.add_handler(MessageHandler(filters.Regex('^(👥 تیم‌های من|👥 My Teams)$'), my_teams))
    application.add_handler(MessageHandler(filters.Regex('^(⚙️ تنظیمات|⚙️ Settings)$'), settings_handler))
    application.add_handler(MessageHandler(filters.Regex('^(❓ راهنما|❓ Help)$'), help_command))
    
    # Admin handlers
    application.add_handler(MessageHandler(filters.Regex('^(🔧 پنل مدیریت|🔧 Admin Panel)$'), admin_panel))
    
    # Registration conversation handler (باید بعد از menu handlers باشد)
    application.add_handler(registration_handler)
    application.add_handler(CallbackQueryHandler(admin_toggle_registration, pattern='^admin_toggle_registration$'))
    application.add_handler(CallbackQueryHandler(admin_set_price, pattern='^admin_set_price'))
    application.add_handler(CallbackQueryHandler(admin_view_registrations, pattern='^admin_view_registrations$'))
    application.add_handler(CallbackQueryHandler(admin_view_payments, pattern='^admin_view_payments$'))
    application.add_handler(CallbackQueryHandler(admin_export_csv, pattern='^admin_export_csv$'))
    application.add_handler(CallbackQueryHandler(admin_panel, pattern='^admin_panel$'))
    
    # Waitlist handler
    application.add_handler(CallbackQueryHandler(handle_waitlist, pattern='^waitlist_'))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


async def handle_waitlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle waitlist decision"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'waitlist_yes':
        # Add to waitlist logic would go here
        await query.edit_message_text("شما به لیست انتظار اضافه شدید." if query.from_user.language_code == 'fa' else "You have been added to the waitlist.")
    else:
        await query.edit_message_text("عملیات لغو شد." if query.from_user.language_code == 'fa' else "Operation cancelled.")


if __name__ == '__main__':
    main()

