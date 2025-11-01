#!/usr/bin/env python3
"""
Script para criar tabela de suppliers com logos na base de dados
"""
import sqlite3
import os

# Conectar à base de dados
db_path = 'carrental.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criar tabela suppliers
cursor.execute('''
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    logo_path TEXT,
    aliases TEXT,
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Dados dos suppliers (código, nome, logo, aliases)
suppliers_data = [
    ('ABB', 'Abbycar', '/static/logos/logo_ABB.png.avif', 'ABB1,Abbycar Não reembolsável'),
    ('ACE', 'Ace Rent a Car', '/static/logos/logo_ACE.png', ''),
    ('ADA', 'Ada', '/static/logos/logo_ADA.png', 'Ada Rent a Car,Ada Car Rental'),
    ('AIR', 'Airauto', '/static/logos/logo_AIR.png', ''),
    ('ALM', 'Alamo', '/static/logos/logo_ALM.png.avif', ''),
    ('AMI', 'Amigoautos', '/static/logos/logo_AMI.png', 'AMI1,Amigoautos Não reembolsável'),
    ('ATR', 'Autorent', '/static/logos/logo_ATR.png', 'Auto Rent'),
    ('AUP', 'Autoprudente', '/static/logos/logo_AUP.png', 'Auto Prudente'),
    ('AUU', 'Auto Union', '/static/logos/logo_AUU.png', ''),
    ('AVX', 'Avis', '/static/logos/logo_AVX.png', ''),
    ('BGX', 'Budget', '/static/logos/logo_BGX.png.avif', ''),
    ('BSD', 'Best Deal', '/static/logos/logo_BSD.png', ''),
    ('CAE', 'Cael', '/static/logos/logo_CAE.png', 'CarRentals'),
    ('CAL', 'Caleche', '/static/logos/logo_CAE.png', ''),
    ('CAR', 'Carnect', '/static/logos/logo_CAR.png', 'Car Nect,Car-Nect'),
    ('CEN', 'Centauro', '/static/logos/logo_CEN.png.avif', ''),
    ('CLA', 'Caldera', '/static/logos/logo_CLA.png', ''),
    ('D4F', 'Drive4fun', '/static/logos/logo_D4F.png.avif', ''),
    ('DOH', 'Drive on Holidays', '/static/logos/logo_DOY.png', 'DOY'),
    ('DTG', 'Dollar', '/static/logos/logo_DTG.png', 'DTG1'),
    ('DVM', 'Drive4move', '/static/logos/logo_DVM.png', 'Drive 4 Move'),
    ('ECR', 'Europcar', '/static/logos/logo_ECR.png.avif', ''),
    ('ENT', 'Enterprise', '/static/logos/logo_ENT.png', ''),
    ('EPI', 'Epi', '/static/logos/logo_EPI.png', ''),
    ('EU2', 'Goldcar', '/static/logos/logo_EUR.png', 'EUR,Goldcar Não reembolsável'),
    ('EUK', 'Goldcar Keyn Go', '/static/logos/logo_EUK.png', ''),
    ('FFX', 'Firefly', '/static/logos/logo_FFX.png', ''),
    ('FLZ', 'Flizzr by Sixt', '/static/logos/logo_FLZ.png.avif', ''),
    ('GMO', 'Green Motion', '/static/logos/logo_GMO.png', 'GMO1,Green Motion Não reembolsável,GRE,GRM'),
    ('GUE', 'Guerin', '/static/logos/logo_GUE.png', ''),
    ('HER', 'Hertz', '/static/logos/logo_HER.png', ''),
    ('ICT', 'International', '/static/logos/logo_ICT.png', 'Interrent,InterRent'),
    ('KED', 'Keddy by Europcar', '/static/logos/logo_KED.png.avif', ''),
    ('KLA', 'Klass Wagen', '/static/logos/logo_KLA.png', ''),
    ('LCR', 'Localcar', '/static/logos/logo_LCR.png', ''),
    ('LOC', 'Locauto', '/static/logos/logo_LOC.png', 'Million'),
    ('LOZ', 'Localiza', '/static/logos/logo_MIL.png?v=2', 'Millioncarhire,Million Car Hire'),
    ('MVY', 'Movyng', '/static/logos/logo_MVY.png', 'Mouvng'),
    ('NAT', 'National', '/static/logos/logo_NAT.png', ''),
    ('OKR', 'OK Mobility', '/static/logos/logo_OKR.png', 'OKR1,OK Mobility Não reembolsável,OK Rent a Car'),
    ('PAR', 'Paa', '/static/logos/logo_PAR.png', ''),
    ('REC', 'Record', '/static/logos/logo_REC.png', 'Record Go'),
    ('RNA', 'Rentauto', '/static/logos/logo_RNA.png', 'Rentacar'),
    ('SAD', 'Drivalia', '/static/logos/logo_SAD.png', ''),
    ('SEV', 'Sevenseas', '/static/logos/logo_SEV.png', ''),
    ('SUR', 'Surprice', '/static/logos/logo_SUR.png', ''),
    ('SVN', 'Sevens', '/static/logos/logo_SVN.png', ''),
    ('SXT', 'Sixt', '/static/logos/logo_SXT.png', ''),
    ('TAN', 'Tangerine Rent a Car', '/static/logos/logo_TAN.png', 'Tangerine'),
    ('TAN1', 'Rent a Car', '/static/logos/logo_TAN1.png', ''),
    ('TAX', 'Tax', '/static/logos/logo_TAX.png', ''),
    ('THR', 'Thrifty', '/static/logos/logo_THR.png.avif', ''),
    ('WIN', 'Winrent', '/static/logos/logo_WIN.png', 'Win Rent'),
    ('YES', 'Yescar', '/static/logos/logo_YES.png?v=2', ''),
    ('YNO', 'Ynot', '/static/logos/logo_YNO.png.avif?v=2', 'YesNo,YNOT,YNO Rent a Car'),
]

# Inserir dados
for code, name, logo, aliases in suppliers_data:
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO suppliers (code, name, logo_path, aliases, active)
            VALUES (?, ?, ?, ?, 1)
        ''', (code, name, logo, aliases))
        print(f"✅ {code} - {name}")
    except Exception as e:
        print(f"❌ Erro ao inserir {code}: {e}")

conn.commit()
conn.close()

print(f"\n✅ Tabela suppliers criada com {len(suppliers_data)} registos!")
print(f"📁 Base de dados: {db_path}")
