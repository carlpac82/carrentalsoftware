#!/usr/bin/env python3
"""Script para restaurar veículos principais na base de dados"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data.db"

# Veículos principais por grupo (code deve ser único!)
VEHICLES = [
    # B1 - Mini 4 Doors
    ("Fiat", "500 4p", "B1-FIAT500", "MINI 4 Portas", 4, 4, "Manual", 1, "https://www.carjet.com/cdn/img/cars/M/car_C25.jpg", 1),
    
    # B2 - Mini 5 Doors
    ("Fiat", "Panda", "B2-PANDA", "MINI 5 Portas", 5, 4, "Manual", 1, "https://www.carjet.com/cdn/img/cars/M/car_C30.jpg", 1),
    ("Toyota", "Aygo", "B2-AYGO", "MINI 5 Portas", 5, 4, "Manual", 1, "https://www.carjet.com/cdn/img/cars/M/car_C29.jpg", 1),
    ("Peugeot", "108", "B2-108", "MINI 5 Portas", 5, 4, "Manual", 1, "https://www.carjet.com/cdn/img/cars/M/car_C15.jpg", 1),
    
    # D - Economy
    ("Renault", "Clio", "D-CLIO", "ECONOMY", 5, 5, "Manual", 2, "https://www.carjet.com/cdn/img/cars/M/car_C04.jpg", 1),
    ("Peugeot", "208", "D-208", "ECONOMY", 5, 5, "Manual", 2, "https://www.carjet.com/cdn/img/cars/M/car_C60.jpg", 1),
    ("Ford", "Fiesta", "D-FIESTA", "ECONOMY", 5, 5, "Manual", 2, "https://www.carjet.com/cdn/img/cars/M/car_C17.jpg", 1),
    
    # E1 - Mini Automatic
    ("Fiat", "500 Auto", "E1-FIAT500A", "MINI Auto", 4, 4, "Automatic", 1, "https://www.carjet.com/cdn/img/cars/M/car_C25.jpg", 1),
    
    # E2 - Economy Automatic
    ("Opel", "Corsa Auto", "E2-CORSA", "ECONOMY Auto", 5, 5, "Automatic", 2, "https://www.carjet.com/cdn/img/cars/M/car_A03.jpg", 1),
    
    # F - SUV
    ("Nissan", "Juke", "F-JUKE", "SUV", 5, 5, "Manual", 2, "https://www.carjet.com/cdn/img/cars/M/car_F29.jpg", 1),
    ("Peugeot", "2008", "F-2008", "SUV", 5, 5, "Manual", 2, "https://www.carjet.com/cdn/img/cars/M/car_F91.jpg", 1),
    
    # G - Premium
    ("Mini", "Cooper Countryman", "G-MINI", "Premium", 5, 5, "Manual", 2, "https://www.carjet.com/cdn/img/cars/M/car_F209.jpg", 1),
    
    # J1 - Crossover
    ("Citroen", "C3 Aircross", "J1-C3AIR", "Crossover", 5, 5, "Manual", 3, "https://www.carjet.com/cdn/img/cars/M/car_A782.jpg", 1),
    ("Fiat", "500X", "J1-500X", "Crossover", 5, 5, "Manual", 3, "https://www.carjet.com/cdn/img/cars/M/car_A112.jpg", 1),
    
    # J2 - Station Wagon
    ("Seat", "Leon SW", "J2-LEON", "Station Wagon", 5, 5, "Manual", 3, "https://www.carjet.com/cdn/img/cars/M/car_F46.jpg", 1),
    
    # L1 - SUV Automatic
    ("Peugeot", "3008 Auto", "L1-3008", "SUV Auto", 5, 5, "Automatic", 3, "https://www.carjet.com/cdn/img/cars/M/car_A132.jpg", 1),
    
    # L2 - Station Wagon Automatic
    ("Toyota", "Corolla SW Auto", "L2-COROLLA", "Station Wagon Auto", 5, 5, "Automatic", 3, "https://www.carjet.com/cdn/img/cars/M/car_A590.jpg", 1),
    
    # M1 - 7 Seater
    ("Dacia", "Lodgy", "M1-LODGY", "7 Lugares", 5, 7, "Manual", 4, "https://www.carjet.com/cdn/img/cars/M/car_M117.jpg", 1),
    ("Peugeot", "Rifter", "M1-RIFTER", "7 Lugares", 5, 7, "Manual", 4, "https://www.carjet.com/cdn/img/cars/M/car_M124.jpg", 1),
    
    # M2 - 7 Seater Automatic
    ("Renault", "Grand Scenic Auto", "M2-SCENIC", "7 Lugares Auto", 5, 7, "Automatic", 4, "https://www.carjet.com/cdn/img/cars/M/car_M15.jpg", 1),
    
    # N - 9 Seater
    ("Ford", "Tourneo", "N-TOURNEO", "9 Lugares", 5, 9, "Manual", 4, "https://www.carjet.com/cdn/img/cars/M/car_M44.jpg", 1),
    ("Mercedes", "Vito", "N-VITO", "9 Lugares", 5, 9, "Manual", 4, "https://www.carjet.com/cdn/img/cars/M/car_A230.jpg", 1),
]

def restore_vehicles():
    """Restaurar veículos na base de dados"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Criar tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS car_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            code TEXT NOT NULL,
            category TEXT NOT NULL,
            doors INTEGER DEFAULT 5,
            seats INTEGER DEFAULT 5,
            transmission TEXT DEFAULT 'Manual',
            luggage INTEGER DEFAULT 2,
            photo_url TEXT,
            enabled INTEGER DEFAULT 1
        )
    """)
    
    # Limpar tabela
    cursor.execute("DELETE FROM car_groups")
    
    # Inserir veículos
    inserted = 0
    for vehicle in VEHICLES:
        brand, model, code, category, doors, seats, transmission, luggage, photo_url, enabled = vehicle
        is_automatic = 1 if transmission == "Automatic" else 0
        name = f"{brand} {model}"
        
        cursor.execute("""
            INSERT INTO car_groups (code, name, brand, model, category, doors, seats, transmission, is_automatic, photo_url, enabled)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (code, name, brand, model, category, doors, seats, transmission, is_automatic, photo_url, enabled))
        inserted += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ {inserted} veículos restaurados com sucesso!")
    print(f"📊 Base de dados: {DB_PATH}")

if __name__ == "__main__":
    restore_vehicles()
