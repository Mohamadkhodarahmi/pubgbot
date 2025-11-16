"""
Payment Callback Handler
"""
from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal, Team, Payment, RegistrationLog, Settings
from payment_gateway import payment_gateway
from i18n import get_text, get_user_language
from config import TARGET_CHANNEL_ID, TARGET_GROUP_ID, PLAYERS_PER_SECTION, TOTAL_SLOTS
import json
from datetime import datetime


async def handle_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle payment callback from gateway"""
    # This will be called via webhook from payment gateway
    # For now, we'll create a command handler for manual verification
    pass


async def verify_payment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verify payment manually (for testing or manual verification)"""
    db = SessionLocal()
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id, db)
        
        # Get authority from message
        if not context.args or len(context.args) < 1:
            await update.message.reply_text(
                "لطفاً Authority را وارد کنید: /verify <authority>" if language == 'fa' 
                else "Please enter Authority: /verify <authority>"
            )
            return
        
        authority = context.args[0]
        
        # Find team with this authority
        team = db.query(Team).filter(Team.payment_authority == authority).first()
        if not team:
            await update.message.reply_text(
                "تیم یافت نشد." if language == 'fa' else "Team not found."
            )
            return
        
        # Verify payment
        verify_result = payment_gateway.verify_payment(authority, team.total_price)
        
        if verify_result['success']:
            team.is_paid = True
            team.payment_ref_id = verify_result['ref_id']
            team.paid_at = datetime.utcnow()
            
            # Create payment record
            payment = Payment(
                team_id=team.id,
                amount=team.total_price,
                authority=authority,
                ref_id=verify_result['ref_id'],
                status='success',
                callback_data={}
            )
            db.add(payment)
            
            # Create log
            log = RegistrationLog(
                team_id=team.id,
                action='paid',
                details={'ref_id': verify_result['ref_id']}
            )
            db.add(log)
            
            # Assign to section
            await assign_team_to_section(team, db, context.bot.token if context else None)
            
            db.commit()
            
            # Notify user
            if context:
                try:
                    await context.bot.send_message(
                        chat_id=team.user.telegram_id,
                        text=get_text('payment_success', language)
                    )
                except:
                    pass
            
            await update.message.reply_text(
                f"✅ پرداخت تایید شد. Ref ID: {verify_result['ref_id']}" if language == 'fa'
                else f"✅ Payment verified. Ref ID: {verify_result['ref_id']}"
            )
        else:
            await update.message.reply_text(
                f"❌ خطا: {verify_result['message']}" if language == 'fa'
                else f"❌ Error: {verify_result['message']}"
            )
    finally:
        db.close()


async def assign_team_to_section(team: Team, db, bot_token=None):
    """Assign team to a section (1-16)"""
    # Check if registration is still open
    registration_setting = db.query(Settings).filter(Settings.key == 'registration_open').first()
    if not registration_setting or registration_setting.value != 'true':
        # Add to waitlist
        team.is_waitlist = True
        waitlist_count = db.query(Team).filter(Team.is_waitlist == True).count()
        team.waitlist_position = waitlist_count + 1
        return
    
    # Find available section
    confirmed_teams = db.query(Team).filter(
        Team.is_confirmed == True,
        Team.is_waitlist == False
    ).all()
    
    # Count players per section
    section_counts = {}
    for t in confirmed_teams:
        if t.section_number:
            section_counts[t.section_number] = section_counts.get(t.section_number, 0) + t.player_count
    
    # Find section with available space
    assigned = False
    for section in range(1, TOTAL_SLOTS + 1):
        current_count = section_counts.get(section, 0)
        if current_count + team.player_count <= PLAYERS_PER_SECTION:
            team.section_number = section
            team.is_confirmed = True
            team.confirmed_at = datetime.utcnow()
            assigned = True
            
            # Create log
            log = RegistrationLog(
                team_id=team.id,
                action='confirmed',
                details={'section': section}
            )
            db.add(log)
            break
    
    if not assigned:
        # Add to waitlist
        team.is_waitlist = True
        waitlist_count = db.query(Team).filter(Team.is_waitlist == True).count()
        team.waitlist_position = waitlist_count + 1
    
    # Send to channel if confirmed
    if team.is_confirmed and team.section_number:
        await send_team_to_channel(team, db, bot_token)


async def send_team_to_channel(team: Team, db, bot_token=None):
    """Send team information to target channel/group"""
    from config import TARGET_CHANNEL_ID, TARGET_GROUP_ID, BOT_TOKEN
    
    players = json.loads(team.players) if isinstance(team.players, str) else team.players
    language = team.user.language or 'fa'
    
    text = f"✅ تیم تایید شده - بخش {team.section_number}\n\n" if language == 'fa' else f"✅ Confirmed Team - Section {team.section_number}\n\n"
    text += f"نام تیم: {team.team_name}\n" if language == 'fa' else f"Team Name: {team.team_name}\n"
    text += f"بازیکنان:\n" if language == 'fa' else f"Players:\n"
    for i, player in enumerate(players, 1):
        text += f"{i}. {player}\n"
    
    token = bot_token or BOT_TOKEN
    
    # Send to channel if configured
    if TARGET_CHANNEL_ID:
        try:
            from telegram import Bot
            bot = Bot(token=token)
            await bot.send_message(chat_id=TARGET_CHANNEL_ID, text=text)
        except Exception as e:
            print(f"Error sending to channel: {e}")
    
    # Send to group if configured
    if TARGET_GROUP_ID:
        try:
            from telegram import Bot
            bot = Bot(token=token)
            await bot.send_message(chat_id=TARGET_GROUP_ID, text=text)
        except Exception as e:
            print(f"Error sending to group: {e}")


async def webhook_payment_callback(request_data: dict, context: ContextTypes.DEFAULT_TYPE):
    """Handle payment callback from webhook"""
    db = SessionLocal()
    try:
        authority = request_data.get('Authority')
        status = request_data.get('Status')
        
        if status != 'OK':
            return {'success': False, 'message': 'Payment not completed'}
        
        # Find team
        team = db.query(Team).filter(Team.payment_authority == authority).first()
        if not team:
            return {'success': False, 'message': 'Team not found'}
        
        if team.is_paid:
            return {'success': True, 'message': 'Already verified', 'ref_id': team.payment_ref_id}
        
        # Verify payment
        verify_result = payment_gateway.verify_payment(authority, team.total_price)
        
        if verify_result['success']:
            team.is_paid = True
            team.payment_ref_id = verify_result['ref_id']
            team.paid_at = datetime.utcnow()
            
            # Create payment record
            payment = Payment(
                team_id=team.id,
                amount=team.total_price,
                authority=authority,
                ref_id=verify_result['ref_id'],
                status='success',
                callback_data=request_data
            )
            db.add(payment)
            
            # Create log
            log = RegistrationLog(
                team_id=team.id,
                action='paid',
                details={'ref_id': verify_result['ref_id'], 'callback': request_data}
            )
            db.add(log)
            
            # Assign to section
            await assign_team_to_section(team, db, context.bot.token if context else None)
            
            db.commit()
            
            # Notify user
            language = team.user.language or 'fa'
            if context:
                try:
                    await context.bot.send_message(
                        chat_id=team.user.telegram_id,
                        text=get_text('payment_success', language)
                    )
                    if team.is_confirmed:
                        await context.bot.send_message(
                            chat_id=team.user.telegram_id,
                            text=get_text('team_confirmed', language, section=team.section_number)
                        )
                except:
                    pass
            
            return {'success': True, 'ref_id': verify_result['ref_id']}
        else:
            # Create failed payment record
            payment = Payment(
                team_id=team.id,
                amount=team.total_price,
                authority=authority,
                status='failed',
                callback_data=request_data
            )
            db.add(payment)
            db.commit()
            
            return {'success': False, 'message': verify_result['message']}
    finally:
        db.close()

