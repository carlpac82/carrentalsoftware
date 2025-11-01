#!/usr/bin/env python3
"""Inicializa a base de dados e cria utilizador admin"""
import sqlite3
import hashlib
import secrets

def hash_password(pw: str, salt: str = "") -> str:
    """Hash password with SHA256"""
    if not salt:
        salt = secrets.token_hex(8)
    digest = hashlib.sha256((salt + ":" + pw).encode("utf-8")).hexdigest()
    return f"sha256:{salt}:{digest}"

def init_database():
    """Criar base de dados e utilizador admin"""
    conn = sqlite3.connect('carrental.db')
    c = conn.cursor()
    
    # Criar tabela users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        mobile TEXT,
        profile_picture_path TEXT,
        is_admin INTEGER DEFAULT 0,
        enabled INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Criar utilizador admin
    username = 'admin'
    password = 'admin123'
    password_hash = hash_password(password)
    
    try:
        c.execute('''INSERT INTO users 
                     (username, password_hash, first_name, last_name, is_admin, enabled) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (username, password_hash, 'Admin', 'User', 1, 1))
        print(f'✅ Utilizador "{username}" criado com sucesso!')
        print(f'   Username: {username}')
        print(f'   Password: {password}')
    except sqlite3.IntegrityError:
        print(f'ℹ️  Utilizador "{username}" já existe')
    
    conn.commit()
    conn.close()
    print('✅ Base de dados inicializada!')

if __name__ == '__main__':
    init_database()
