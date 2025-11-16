from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import pytz
from config import DATABASE_URL, DEFAULT_TIMEZONE

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    language = Column(String(10), default='fa')
    timezone = Column(String(50), default=DEFAULT_TIMEZONE)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    teams = relationship("Team", back_populates="user")
    saved_players = relationship("SavedPlayer", back_populates="user")


class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    team_name = Column(String(255))
    player_count = Column(Integer, nullable=False)
    players = Column(JSON, nullable=False)  # List of player names
    total_price = Column(Integer, nullable=False)
    is_paid = Column(Boolean, default=False)
    is_confirmed = Column(Boolean, default=False)
    payment_id = Column(String(255))
    payment_authority = Column(String(255))
    payment_ref_id = Column(String(255))
    section_number = Column(Integer)  # 1-16
    is_waitlist = Column(Boolean, default=False)
    waitlist_position = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime)
    confirmed_at = Column(DateTime)
    
    user = relationship("User", back_populates="teams")


class SavedPlayer(Base):
    __tablename__ = 'saved_players'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    player_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="saved_players")


class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    authority = Column(String(255))
    ref_id = Column(String(255))
    status = Column(String(50))  # pending, success, failed
    callback_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Settings(Base):
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RegistrationLog(Base):
    __tablename__ = 'registration_logs'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    action = Column(String(100))  # registered, paid, confirmed, cancelled
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

