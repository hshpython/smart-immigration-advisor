import sqlite3

DB_NAME = 'hospital.db'


def add_pharmacy_tables():
    """Add pharmacy-related tables"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # جدول داروها
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT,
            manufacturer TEXT,
            price REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            min_stock INTEGER DEFAULT 10,
            expiry_date TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول فروش دارو
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicine_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            prescription_id INTEGER,
            notes TEXT,
            FOREIGN KEY (medicine_id) REFERENCES medicines(id),
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    ''')

    # اضافه کردن داروهای نمونه
    medicines = [
        ('Paracetamol 500mg', 'Painkiller', 'Tehran Pharma', 15000, 500, 50, '2027-06-30', 'For pain and fever'),
        ('Amoxicillin 500mg', 'Antibiotic', 'Pars Daru', 45000, 200, 30, '2027-03-15', 'Antibiotic'),
        ('Ibuprofen 400mg', 'Painkiller', 'Alborz Pharma', 25000, 300, 40, '2027-09-20', 'Anti-inflammatory'),
        ('Omeprazole 20mg', 'Antacid', 'Tehran Pharma', 35000, 150, 20, '2027-12-01', 'For stomach acid'),
        ('Metformin 500mg', 'Diabetes', 'Pars Daru', 30000, 400, 50, '2028-01-15', 'For diabetes'),
        ('Atorvastatin 20mg', 'Cholesterol', 'Alborz Pharma', 55000, 100, 25, '2027-08-10', 'For cholesterol'),
        ('Losartan 50mg', 'Blood Pressure', 'Tehran Pharma', 40000, 180, 30, '2027-11-20', 'For blood pressure'),
        ('Vitamin D3 1000IU', 'Supplement', 'Pars Daru', 20000, 600, 60, '2028-06-30', 'Vitamin supplement'),
        ('Iron Supplement', 'Supplement', 'Alborz Pharma', 18000, 350, 40, '2028-03-15', 'Iron supplement'),
        ('Cetirizine 10mg', 'Antihistamine', 'Tehran Pharma', 22000, 250, 30, '2027-10-05', 'For allergies'),
    ]

    for med in medicines:
        try:
            cursor.execute('''
                INSERT INTO medicines (name, category, manufacturer, price, stock_quantity, min_stock, expiry_date, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', med)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print('✅ Pharmacy tables created!')


if __name__ == '__main__':
    add_pharmacy_tables()
    print('🎉 Database updated with pharmacy tables!')