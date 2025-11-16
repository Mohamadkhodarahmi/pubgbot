"""
Web-based Admin Panel
"""
from flask import Flask, render_template_string, request, redirect, url_for, flash, send_file
from flask_cors import CORS
from database import SessionLocal, Team, Settings, Payment, RegistrationLog, User
from config import PANEL_SECRET_KEY, PANEL_PORT, ADMIN_IDS
from datetime import datetime
import json
import pandas as pd
from io import BytesIO
import pytz

app = Flask(__name__)
app.secret_key = PANEL_SECRET_KEY
CORS(app)

# Simple authentication (in production, use proper auth)
def is_admin(telegram_id):
    return telegram_id in ADMIN_IDS


ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پنل مدیریت - New State Mobile Registration</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-card h3 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5568d3;
        }
        .btn-success {
            background: #28a745;
            color: white;
        }
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        .btn-warning {
            background: #ffc107;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .status-open {
            color: #28a745;
            font-weight: bold;
        }
        .status-closed {
            color: #dc3545;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 پنل مدیریت ثبت‌نام</h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{{ stats.total_teams }}</h3>
                <p>کل تیم‌ها</p>
            </div>
            <div class="stat-card">
                <h3>{{ stats.confirmed_teams }}</h3>
                <p>تایید شده</p>
            </div>
            <div class="stat-card">
                <h3>{{ stats.paid_teams }}</h3>
                <p>پرداخت شده</p>
            </div>
            <div class="stat-card">
                <h3>{{ stats.waitlist_count }}</h3>
                <p>لیست انتظار</p>
            </div>
        </div>
        
        <div class="controls">
            <form method="POST" action="/admin/toggle_registration" style="display: inline;">
                <button type="submit" class="btn {% if registration_open %}btn-danger{% else %}btn-success{% endif %}">
                    {% if registration_open %}بستن ثبت‌نام{% else %}باز کردن ثبت‌نام{% endif %}
                </button>
            </form>
            
            <form method="POST" action="/admin/set_price" style="display: inline;">
                <div class="form-group">
                    <label>قیمت هر نفر (تومان):</label>
                    <input type="number" name="price" value="{{ current_price }}" required>
                </div>
                <button type="submit" class="btn btn-primary">ذخیره قیمت</button>
            </form>
            
            <a href="/admin/export" class="btn btn-warning">📥 خروجی Excel</a>
        </div>
        
        <h2>آخرین ثبت‌نام‌ها</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>نام تیم</th>
                    <th>تعداد بازیکن</th>
                    <th>مبلغ</th>
                    <th>وضعیت</th>
                    <th>بخش</th>
                    <th>تاریخ</th>
                </tr>
            </thead>
            <tbody>
                {% for team in teams %}
                <tr>
                    <td>{{ team.id }}</td>
                    <td>{{ team.team_name }}</td>
                    <td>{{ team.player_count }}</td>
                    <td>{{ "{:,}".format(team.total_price) }}</td>
                    <td>
                        {% if team.is_confirmed %}✅ تایید شده
                        {% elif team.is_paid %}💰 پرداخت شده
                        {% elif team.is_waitlist %}⏳ لیست انتظار
                        {% else %}⏳ در انتظار پرداخت{% endif %}
                    </td>
                    <td>{{ team.section_number or '-' }}</td>
                    <td>{{ team.created_at.strftime('%Y/%m/%d %H:%M') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""


@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    # Simple auth check (in production, use proper authentication)
    # For now, we'll skip auth for development
    
    db = SessionLocal()
    try:
        # Get statistics
        total_teams = db.query(Team).count()
        confirmed_teams = db.query(Team).filter(Team.is_confirmed == True).count()
        paid_teams = db.query(Team).filter(Team.is_paid == True).count()
        waitlist_count = db.query(Team).filter(Team.is_waitlist == True).count()
        
        # Get registration status
        registration_setting = db.query(Settings).filter(Settings.key == 'registration_open').first()
        registration_open = registration_setting and registration_setting.value == 'true'
        
        # Get current price
        price_setting = db.query(Settings).filter(Settings.key == 'price_per_player').first()
        current_price = int(price_setting.value) if price_setting else 0
        
        # Get recent teams
        teams = db.query(Team).order_by(Team.created_at.desc()).limit(20).all()
        
        stats = {
            'total_teams': total_teams,
            'confirmed_teams': confirmed_teams,
            'paid_teams': paid_teams,
            'waitlist_count': waitlist_count
        }
        
        return render_template_string(
            ADMIN_TEMPLATE,
            stats=stats,
            registration_open=registration_open,
            current_price=current_price,
            teams=teams
        )
    finally:
        db.close()


@app.route('/admin/toggle_registration', methods=['POST'])
def toggle_registration():
    """Toggle registration status"""
    db = SessionLocal()
    try:
        registration_setting = db.query(Settings).filter(Settings.key == 'registration_open').first()
        if not registration_setting:
            registration_setting = Settings(key='registration_open', value='false')
            db.add(registration_setting)
        
        new_value = 'false' if registration_setting.value == 'true' else 'true'
        registration_setting.value = new_value
        db.commit()
        
        flash('وضعیت ثبت‌نام تغییر کرد', 'success')
    finally:
        db.close()
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/set_price', methods=['POST'])
def set_price():
    """Set price per player"""
    db = SessionLocal()
    try:
        price = int(request.form.get('price', 0))
        
        price_setting = db.query(Settings).filter(Settings.key == 'price_per_player').first()
        if not price_setting:
            price_setting = Settings(key='price_per_player', value=str(price))
            db.add(price_setting)
        else:
            price_setting.value = str(price)
        
        db.commit()
        flash(f'قیمت به {price:,} تومان تغییر کرد', 'success')
    finally:
        db.close()
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/export')
def export_data():
    """Export registrations to Excel"""
    db = SessionLocal()
    try:
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
                'Created At': team.created_at.strftime('%Y-%m-%d %H:%M:%S') if team.created_at else '',
                'Paid At': team.paid_at.strftime('%Y-%m-%d %H:%M:%S') if team.paid_at else '',
                'Confirmed At': team.confirmed_at.strftime('%Y-%m-%d %H:%M:%S') if team.confirmed_at else ''
            })
        
        df = pd.DataFrame(data)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Registrations')
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='registrations.xlsx'
        )
    finally:
        db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PANEL_PORT, debug=True)

