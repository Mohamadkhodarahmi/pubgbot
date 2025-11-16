"""
Database Setup Script
"""
from database import init_db, SessionLocal, Settings
from config import DEFAULT_PRICE_PER_PLAYER

def setup_initial_settings():
    """Setup initial settings in database"""
    db = SessionLocal()
    try:
        # Check if settings exist
        registration_setting = db.query(Settings).filter(Settings.key == 'registration_open').first()
        if not registration_setting:
            registration_setting = Settings(key='registration_open', value='false')
            db.add(registration_setting)
        
        price_setting = db.query(Settings).filter(Settings.key == 'price_per_player').first()
        if not price_setting:
            price_setting = Settings(key='price_per_player', value=str(DEFAULT_PRICE_PER_PLAYER))
            db.add(price_setting)
        
        db.commit()
        print("✅ Initial settings created successfully!")
    except Exception as e:
        print(f"❌ Error setting up initial settings: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("✅ Database initialized!")
    
    print("Setting up initial settings...")
    setup_initial_settings()
    
    print("✅ Setup complete!")

