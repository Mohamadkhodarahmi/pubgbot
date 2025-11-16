"""
Timezone conversion utilities
"""
from datetime import datetime
import pytz
from typing import Optional


TIMEZONES = {
    'tehran': 'Asia/Tehran',
    'riyadh': 'Asia/Riyadh',
    'utc': 'UTC'
}

TIMEZONE_NAMES = {
    'fa': {
        'tehran': 'تهران',
        'riyadh': 'ریاض',
        'utc': 'UTC'
    },
    'en': {
        'tehran': 'Tehran',
        'riyadh': 'Riyadh',
        'utc': 'UTC'
    }
}


def convert_timezone(dt: datetime, from_tz: str, to_tz: str) -> datetime:
    """Convert datetime from one timezone to another"""
    if isinstance(from_tz, str) and from_tz in TIMEZONES:
        from_tz = TIMEZONES[from_tz]
    if isinstance(to_tz, str) and to_tz in TIMEZONES:
        to_tz = TIMEZONES[to_tz]
    
    from_tz_obj = pytz.timezone(from_tz)
    to_tz_obj = pytz.timezone(to_tz)
    
    if dt.tzinfo is None:
        dt = from_tz_obj.localize(dt)
    
    return dt.astimezone(to_tz_obj)


def format_datetime(dt: datetime, timezone: str = 'Asia/Tehran', language: str = 'fa') -> str:
    """Format datetime for display"""
    if dt.tzinfo is None:
        tz = pytz.timezone(timezone)
        dt = tz.localize(dt)
    else:
        dt = dt.astimezone(pytz.timezone(timezone))
    
    if language == 'fa':
        # Persian date format
        months_fa = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                     'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        # Simple format for now
        return dt.strftime('%Y/%m/%d %H:%M:%S')
    else:
        return dt.strftime('%Y-%m-%d %H:%M:%S')


def get_current_time(timezone: str = 'Asia/Tehran') -> datetime:
    """Get current time in specified timezone"""
    tz = pytz.timezone(timezone)
    return datetime.now(tz)

