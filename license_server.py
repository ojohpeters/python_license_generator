from flask import Flask, request, jsonify
from datetime import datetime
import hashlib
import json
import os
from cryptography.fernet import Fernet
import sqlite3
import uuid

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('licenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            license_key TEXT UNIQUE,
            expiry_date TEXT,
            is_active INTEGER,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Generate encryption key
def generate_key():
    if not os.path.exists('encryption.key'):
        key = Fernet.generate_key()
        with open('encryption.key', 'wb') as key_file:
            key_file.write(key)
    return open('encryption.key', 'rb').read()

# Initialize
init_db()
ENCRYPTION_KEY = generate_key()
fernet = Fernet(ENCRYPTION_KEY)

@app.route('/generate_license', methods=['POST'])
def generate_license():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'error': 'Username required'}), 400
    
    license_key = str(uuid.uuid4())
    expiry_date = (datetime.now().replace(year=datetime.now().year + 1)
                  .strftime('%Y-%m-%d'))
    
    conn = sqlite3.connect('licenses.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO licenses (id, username, license_key, expiry_date, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()),
            username,
            license_key,
            expiry_date,
            1,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        
        return jsonify({
            'username': username,
            'license_key': license_key,
            'expiry_date': expiry_date,
            'encryption_key': ENCRYPTION_KEY.decode()
        })
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400
    finally:
        conn.close()

@app.route('/verify', methods=['POST'])
def verify_license():
    try:
        encrypted_data = request.json.get('data')
        decrypted_data = fernet.decrypt(encrypted_data.encode())
        data = json.loads(decrypted_data)
        
        username = data.get('username')
        license_key = data.get('license_key')
        machine_id = data.get('machine_id')
        
        conn = sqlite3.connect('licenses.db')
        c = conn.cursor()
        c.execute('''
            SELECT expiry_date, is_active 
            FROM licenses 
            WHERE username = ? AND license_key = ?
        ''', (username, license_key))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return jsonify({
                'status': 'error',
                'message': 'Invalid license',
                'approved': False
            })
        
        expiry_date, is_active = result
        
        if not is_active:
            return jsonify({
                'status': 'error',
                'message': 'License is inactive',
                'approved': False
            })
            
        if datetime.strptime(expiry_date, '%Y-%m-%d') < datetime.now():
            return jsonify({
                'status': 'error',
                'message': 'License expired',
                'approved': False
            })
        
        token = fernet.encrypt(json.dumps({
            'username': username,
            'machine_id': machine_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }).encode()).decode()
        
        return jsonify({
            'status': 'success',
            'message': 'License verified',
            'approved': True,
            'expiry': expiry_date,
            'token': token
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'approved': False
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
