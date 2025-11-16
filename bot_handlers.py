"""
Telegram Bot Handlers
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from database import SessionLocal, User, Team, SavedPlayer, Settings, RegistrationLog, Payment
from i18n import get_text, get_user_language
from payment_gateway import payment_gateway
from config import DEFAULT_PRICE_PER_PLAYER, MAX_PLAYERS_PER_TEAM, MIN_PLAYERS_PER_TEAM, ADMIN_IDS
from datetime import datetime
import json

# Conversation states
SELECTING_PLAYER_COUNT, ENTERING_TEAM_NAME, ENTERING_PLAYER_NAMES, SELECTING_SAVED_PLAYER = range(4)


def get_main_keyboard(language: str = 'fa'):
    """Get main menu keyboard"""
    if language == 'fa':
        keyboard = [
            [KeyboardButton('📝 ثبت‌نام تیم'), KeyboardButton('👥 تیم‌های من')],
            [KeyboardButton('⚙️ تنظیمات'), KeyboardButton('❓ راهنما')]
        ]
    else:
        keyboard = [
            [KeyboardButton('📝 Register Team'), KeyboardButton('👥 My Teams')],
            [KeyboardButton('⚙️ Settings'), KeyboardButton('❓ Help')]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_admin_keyboard(language: str = 'fa'):
    """Get admin keyboard"""
    if language == 'fa':
        keyboard = [
            [KeyboardButton('🔧 پنل مدیریت')]
        ]
    else:
        keyboard = [
            [KeyboardButton('🔧 Admin Panel')]
        ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    db = SessionLocal()
    try:
        user_id = update.effective_user.id
        username = update.effective_user.username
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name
        
        # Get or create user
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            user = User(
                telegram_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_admin=user_id in ADMIN_IDS
            )
            db.add(user)
            db.commit()
        else:
            # Update user info
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            if user_id in ADMIN_IDS:
                user.is_admin = True
            db.commit()
        
        language = user.language or 'fa'
        
        welcome_text = get_text('welcome', language)
        instructions_text = get_text('instructions', language)
        
        keyboard = get_main_keyboard(language)
        if user.is_admin:
            admin_keyboard = get_admin_keyboard(language)
            keyboard.keyboard.append(admin_keyboard.keyboard[0])
        
        await update.message.reply_text(
            f"{welcome_text}\n\n{instructions_text}",
            reply_markup=keyboard
        )
    finally:
        db.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle help command"""
    db = SessionLocal()
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id, db)
        help_text = get_text('instructions', language)
        await update.message.reply_text(help_text)
    finally:
        db.close()


async def register_team_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start team registration process"""
    db = SessionLocal()
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id, db)
        
        # Check if registration is open
        registration_setting = db.query(Settings).filter(Settings.key == 'registration_open').first()
        if not registration_setting or registration_setting.value != 'true':
            await update.message.reply_text(get_text('registration_closed', language))
            return ConversationHandler.END
        
        # Check capacity
        confirmed_teams = db.query(Team).filter(
            Team.is_confirmed == True,
            Team.is_waitlist == False
        ).count()
        
        total_capacity = 64  # 16 sections * 4 players
        if confirmed_teams >= total_capacity:
            keyboard = [
                [InlineKeyboardButton(get_text('yes', language), callback_data='waitlist_yes'),
                 InlineKeyboardButton(get_text('no', language), callback_data='waitlist_no')]
            ]
            await update.message.reply_text(
                get_text('capacity_full', language),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return ConversationHandler.END
        
        # Show player count selection
        keyboard = []
        for count in range(MIN_PLAYERS_PER_TEAM, MAX_PLAYERS_PER_TEAM + 1):
            keyboard.append([InlineKeyboardButton(
                str(count),
                callback_data=f'player_count_{count}'
            )])
        
        await update.message.reply_text(
            get_text('select_player_count', language),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return SELECTING_PLAYER_COUNT
    finally:
        db.close()


async def select_player_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle player count selection"""
    query = update.callback_query
    await query.answer()
    
    player_count = int(query.data.split('_')[-1])
    context.user_data['player_count'] = player_count
    context.user_data['current_player'] = 1
    context.user_data['players'] = []
    
    db = SessionLocal()
    try:
        language = get_user_language(query.from_user.id, db)
        
        # Check for saved players
        user = db.query(User).filter(User.telegram_id == query.from_user.id).first()
        saved_players = db.query(SavedPlayer).filter(SavedPlayer.user_id == user.id).all()
        
        if saved_players:
            keyboard = []
            for saved_player in saved_players[:10]:  # Limit to 10
                keyboard.append([InlineKeyboardButton(
                    saved_player.player_name,
                    callback_data=f'saved_player_{saved_player.id}'
                )])
            keyboard.append([InlineKeyboardButton(
                get_text('enter_manually', language),
                callback_data='enter_manually'
            )])
            
            await query.edit_message_text(
                get_text('select_saved_player', language, number=1),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return SELECTING_SAVED_PLAYER
        else:
            await query.edit_message_text(
                get_text('enter_player_name', language, number=1)
            )
            return ENTERING_PLAYER_NAMES
    finally:
        db.close()


async def select_saved_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle saved player selection"""
    query = update.callback_query
    await query.answer()
    
    db = SessionLocal()
    try:
        language = get_user_language(query.from_user.id, db)
        
        if query.data == 'enter_manually':
            await query.edit_message_text(
                get_text('enter_player_name', language, number=context.user_data['current_player'])
            )
            return ENTERING_PLAYER_NAMES
        
        # Get saved player
        saved_player_id = int(query.data.split('_')[-1])
        saved_player = db.query(SavedPlayer).filter(SavedPlayer.id == saved_player_id).first()
        
        if saved_player:
            context.user_data['players'].append(saved_player.player_name)
            context.user_data['current_player'] += 1
            
            if context.user_data['current_player'] > context.user_data['player_count']:
                # All players entered, ask for team name
                await query.edit_message_text(
                    get_text('enter_team_name', language)
                )
                return ENTERING_TEAM_NAME
            else:
                # Ask for next player
                user = db.query(User).filter(User.telegram_id == query.from_user.id).first()
                saved_players = db.query(SavedPlayer).filter(SavedPlayer.user_id == user.id).all()
                
                keyboard = []
                for sp in saved_players[:10]:
                    keyboard.append([InlineKeyboardButton(
                        sp.player_name,
                        callback_data=f'saved_player_{sp.id}'
                    )])
                keyboard.append([InlineKeyboardButton(
                    get_text('enter_manually', language),
                    callback_data='enter_manually'
                )])
                
                await query.edit_message_text(
                    get_text('select_saved_player', language, number=context.user_data['current_player']),
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return SELECTING_SAVED_PLAYER
    finally:
        db.close()


async def enter_player_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle player name input"""
    player_name = update.message.text.strip()
    
    if not player_name:
        db = SessionLocal()
        try:
            language = get_user_language(update.effective_user.id, db)
            await update.message.reply_text(get_text('player_name_required', language))
            return ENTERING_PLAYER_NAMES
        finally:
            db.close()
    
    context.user_data['players'].append(player_name)
    context.user_data['current_player'] += 1
    
    db = SessionLocal()
    try:
        language = get_user_language(update.effective_user.id, db)
        
        # Save player for future use
        user = db.query(User).filter(User.telegram_id == update.effective_user.id).first()
        if user:
            existing = db.query(SavedPlayer).filter(
                SavedPlayer.user_id == user.id,
                SavedPlayer.player_name == player_name
            ).first()
            if not existing:
                saved_player = SavedPlayer(user_id=user.id, player_name=player_name)
                db.add(saved_player)
                db.commit()
        
        if context.user_data['current_player'] > context.user_data['player_count']:
            # All players entered, ask for team name
            await update.message.reply_text(get_text('enter_team_name', language))
            return ENTERING_TEAM_NAME
        else:
            await update.message.reply_text(
                get_text('enter_player_name', language, number=context.user_data['current_player'])
            )
            return ENTERING_PLAYER_NAMES
    finally:
        db.close()


async def enter_team_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle team name input and create team"""
    team_name = update.message.text.strip()
    
    if not team_name:
        db = SessionLocal()
        try:
            language = get_user_language(update.effective_user.id, db)
            await update.message.reply_text(get_text('team_name_required', language))
            return ENTERING_TEAM_NAME
        finally:
            db.close()
    
    db = SessionLocal()
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id, db)
        
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            await update.message.reply_text(get_text('error', language, message='User not found'))
            return ConversationHandler.END
        
        # Get price per player
        price_setting = db.query(Settings).filter(Settings.key == 'price_per_player').first()
        price_per_player = int(price_setting.value) if price_setting else DEFAULT_PRICE_PER_PLAYER
        total_price = price_per_player * context.user_data['player_count']
        
        # Create team
        team = Team(
            user_id=user.id,
            team_name=team_name,
            player_count=context.user_data['player_count'],
            players=json.dumps(context.user_data['players']),
            total_price=total_price,
            is_paid=False,
            is_confirmed=False
        )
        db.add(team)
        db.commit()
        
        # Create registration log
        log = RegistrationLog(
            team_id=team.id,
            action='registered',
            details={'team_name': team_name, 'players': context.user_data['players']}
        )
        db.add(log)
        db.commit()
        
        # Create payment request
        description = f"Team: {team_name} - {context.user_data['player_count']} players"
        payment_result = payment_gateway.create_payment_request(
            amount=total_price,
            description=description,
            metadata={'team_id': team.id, 'user_id': user_id}
        )
        
        if payment_result['success']:
            team.payment_authority = payment_result['authority']
            db.commit()
            
            keyboard = [[InlineKeyboardButton(
                get_text('payment_link', language, link=payment_result['payment_url']).split('\n')[1],
                url=payment_result['payment_url']
            )]]
            
            await update.message.reply_text(
                f"{get_text('team_saved', language)}\n\n"
                f"{get_text('total_price', language, price=total_price)}\n\n"
                f"{get_text('payment_link', language, link=payment_result['payment_url'])}",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text(
                get_text('error', language, message=payment_result['message'])
            )
        
        return ConversationHandler.END
    finally:
        db.close()


async def cancel_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel registration"""
    db = SessionLocal()
    try:
        language = get_user_language(update.effective_user.id, db)
        await update.message.reply_text(
            get_text('cancel', language),
            reply_markup=get_main_keyboard(language)
        )
    finally:
        db.close()
    return ConversationHandler.END


async def my_teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's teams"""
    db = SessionLocal()
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id, db)
        
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            await update.message.reply_text(get_text('error', language, message='User not found'))
            return
        
        teams = db.query(Team).filter(Team.user_id == user.id).order_by(Team.created_at.desc()).all()
        
        if not teams:
            await update.message.reply_text("شما هنوز تیمی ثبت نکرده‌اید." if language == 'fa' else "You haven't registered any teams yet.")
            return
        
        for team in teams:
            players = json.loads(team.players) if isinstance(team.players, str) else team.players
            status = "✅ تایید شده" if team.is_confirmed else ("💰 پرداخت شده" if team.is_paid else "⏳ در انتظار پرداخت")
            if language == 'en':
                status = "✅ Confirmed" if team.is_confirmed else ("💰 Paid" if team.is_paid else "⏳ Pending Payment")
            
            text = f"تیم: {team.team_name}\n" if language == 'fa' else f"Team: {team.team_name}\n"
            text += f"بازیکنان: {', '.join(players)}\n" if language == 'fa' else f"Players: {', '.join(players)}\n"
            text += f"وضعیت: {status}\n"
            if team.section_number:
                text += f"بخش: {team.section_number}" if language == 'fa' else f"Section: {team.section_number}"
            
            await update.message.reply_text(text)
    finally:
        db.close()

