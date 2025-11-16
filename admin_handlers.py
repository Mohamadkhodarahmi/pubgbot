"""
Admin Panel Handlers
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import SessionLocal, User, Team, Settings, Payment, RegistrationLog
from i18n import get_text, get_user_language
from config import ADMIN_IDS
from datetime import datetime
import json
import pandas as pd
from io import BytesIO


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin panel"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
    
    db = SessionLocal()
    try:
        language = get_user_language(user_id, db)
        
        # Check registration status
        registration_setting = db.query(Settings).filter(Settings.key == 'registration_open').first()
        is_open = registration_setting and registration_setting.value == 'true'
        
        # Get price
        price_setting = db.query(Settings).filter(Settings.key == 'price_per_player').first()
        price = int(price_setting.value) if price_setting else 0
        
        # Get statistics
        total_teams = db.query(Team).count()
        confirmed_teams = db.query(Team).filter(Team.is_confirmed == True).count()
        paid_teams = db.query(Team).filter(Team.is_paid == True).count()
        waitlist_count = db.query(Team).filter(Team.is_waitlist == True).count()
        
        keyboard = [
            [InlineKeyboardButton(
                get_text('close_registration', language) if is_open else get_text('open_registration', language),
                callback_data='admin_toggle_registration'
            )],
            [InlineKeyboardButton(get_text('set_price', language), callback_data='admin_set_price')],
            [InlineKeyboardButton(get_text('view_registrations', language), callback_data='admin_view_registrations')],
            [InlineKeyboardButton(get_text('view_payments', language), callback_data='admin_view_payments')],
            [InlineKeyboardButton(get_text('manage_waitlist', language), callback_data='admin_waitlist')],
            [InlineKeyboardButton(get_text('export_csv', language), callback_data='admin_export_csv')],
        ]
        
        status_text = "باز" if is_open else "بسته"
        if language == 'en':
            status_text = "Open" if is_open else "Closed"
        
        text = f"🔧 {get_text('admin_panel', language)}\n\n"
        text += f"وضعیت ثبت‌نام: {status_text}\n" if language == 'fa' else f"Registration Status: {status_text}\n"
        text += f"قیمت هر نفر: {price:,} تومان\n" if language == 'fa' else f"Price per player: {price:,} Rials\n"
        text += f"تعداد کل تیم‌ها: {total_teams}\n" if language == 'fa' else f"Total Teams: {total_teams}\n"
        text += f"تیم‌های تایید شده: {confirmed_teams}\n" if language == 'fa' else f"Confirmed Teams: {confirmed_teams}\n"
        text += f"تیم‌های پرداخت شده: {paid_teams}\n" if language == 'fa' else f"Paid Teams: {paid_teams}\n"
        text += f"لیست انتظار: {waitlist_count}" if language == 'fa' else f"Waitlist: {waitlist_count}"
        
        # Handle both message and callback_query
        if update.message:
            await update.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    finally:
        db.close()


async def admin_toggle_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle registration status"""
    if not is_admin(update.callback_query.from_user.id):
        return
    
    query = update.callback_query
    await query.answer()
    
    db = SessionLocal()
    try:
        language = get_user_language(query.from_user.id, db)
        
        registration_setting = db.query(Settings).filter(Settings.key == 'registration_open').first()
        if not registration_setting:
            registration_setting = Settings(key='registration_open', value='false')
            db.add(registration_setting)
        
        new_value = 'false' if registration_setting.value == 'true' else 'true'
        registration_setting.value = new_value
        db.commit()
        
        message = get_text('registration_closed_admin', language) if new_value == 'false' else get_text('registration_opened', language)
        await query.edit_message_text(message)
        
        # Show admin panel again
        await admin_panel(update, context)
    finally:
        db.close()


async def admin_set_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set price per player"""
    if not is_admin(update.callback_query.from_user.id):
        return
    
    query = update.callback_query
    await query.answer()
    
    db = SessionLocal()
    try:
        language = get_user_language(query.from_user.id, db)
        
        # Check if we have price in callback data
        if query.data and '_' in query.data and query.data.split('_')[-1].isdigit():
            # Price provided in callback
            new_price = int(query.data.split('_')[-1])
            price_setting = db.query(Settings).filter(Settings.key == 'price_per_player').first()
            if not price_setting:
                price_setting = Settings(key='price_per_player', value=str(new_price))
                db.add(price_setting)
            else:
                price_setting.value = str(new_price)
            db.commit()
            
            await query.edit_message_text(
                get_text('price_updated', language, price=new_price)
            )
            # Return to admin panel
            await admin_panel(update, context)
        else:
            # Show current price and options
            price_setting = db.query(Settings).filter(Settings.key == 'price_per_player').first()
            current_price = int(price_setting.value) if price_setting else 0
            
            keyboard = [
                [InlineKeyboardButton("50000", callback_data='admin_set_price_50000'),
                 InlineKeyboardButton("100000", callback_data='admin_set_price_100000')],
                [InlineKeyboardButton("150000", callback_data='admin_set_price_150000'),
                 InlineKeyboardButton("200000", callback_data='admin_set_price_200000')],
                [InlineKeyboardButton(get_text('back', language), callback_data='admin_panel')]
            ]
            
            await query.edit_message_text(
                f"قیمت فعلی: {current_price:,} تومان\n\nقیمت جدید را انتخاب کنید:" if language == 'fa'
                else f"Current price: {current_price:,} Rials\n\nSelect new price:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    finally:
        db.close()


async def admin_view_registrations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all registrations"""
    if not is_admin(update.callback_query.from_user.id):
        return
    
    query = update.callback_query
    await query.answer()
    
    db = SessionLocal()
    try:
        language = get_user_language(query.from_user.id, db)
        
        teams = db.query(Team).order_by(Team.created_at.desc()).limit(10).all()
        
        if not teams:
            await query.edit_message_text(
                "هیچ ثبت‌نامی یافت نشد." if language == 'fa' else "No registrations found."
            )
            return
        
        text = "📋 آخرین ثبت‌نام‌ها:\n\n" if language == 'fa' else "📋 Latest Registrations:\n\n"
        for team in teams:
            players = json.loads(team.players) if isinstance(team.players, str) else team.players
            status = "✅" if team.is_confirmed else ("💰" if team.is_paid else "⏳")
            text += f"{status} {team.team_name} - {len(players)} بازیکن\n" if language == 'fa' else f"{status} {team.team_name} - {len(players)} players\n"
        
        keyboard = [[InlineKeyboardButton(get_text('back', language), callback_data='admin_panel')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    finally:
        db.close()


async def admin_view_payments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all payments"""
    if not is_admin(update.callback_query.from_user.id):
        return
    
    query = update.callback_query
    await query.answer()
    
    db = SessionLocal()
    try:
        language = get_user_language(query.from_user.id, db)
        
        payments = db.query(Payment).filter(Payment.status == 'success').order_by(Payment.created_at.desc()).limit(10).all()
        
        if not payments:
            await query.edit_message_text(
                "هیچ پرداختی یافت نشد." if language == 'fa' else "No payments found."
            )
            return
        
        text = "💰 آخرین پرداخت‌ها:\n\n" if language == 'fa' else "💰 Latest Payments:\n\n"
        for payment in payments:
            text += f"✅ {payment.amount:,} تومان - Ref: {payment.ref_id}\n" if language == 'fa' else f"✅ {payment.amount:,} Rials - Ref: {payment.ref_id}\n"
        
        keyboard = [[InlineKeyboardButton(get_text('back', language), callback_data='admin_panel')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    finally:
        db.close()


async def admin_export_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Export registrations to CSV"""
    if not is_admin(update.callback_query.from_user.id):
        return
    
    query = update.callback_query
    await query.answer()
    
    db = SessionLocal()
    try:
        language = get_user_language(query.from_user.id, db)
        
        teams = db.query(Team).all()
        
        data = []
        for team in teams:
            players = json.loads(team.players) if isinstance(team.players, str) else team.players
            data.append({
                'Team ID': team.id,
                'Team Name': team.team_name,
                'User ID': team.user.telegram_id,
                'Player Count': team.player_count,
                'Players': ', '.join(players),
                'Total Price': team.total_price,
                'Is Paid': team.is_paid,
                'Is Confirmed': team.is_confirmed,
                'Section Number': team.section_number or '',
                'Is Waitlist': team.is_waitlist,
                'Waitlist Position': team.waitlist_position or '',
                'Created At': team.created_at,
                'Paid At': team.paid_at or '',
                'Confirmed At': team.confirmed_at or ''
            })
        
        df = pd.DataFrame(data)
        
        # Create Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Registrations')
        
        output.seek(0)
        
        await query.message.reply_document(
            document=output,
            filename='registrations.xlsx',
            caption="فایل خروجی ثبت‌نام‌ها" if language == 'fa' else "Registrations Export"
        )
        
        await query.answer("✅ فایل ارسال شد" if language == 'fa' else "✅ File sent")
    finally:
        db.close()

