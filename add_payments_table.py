import sqlite3

DB_NAME = 'hospital.db'


def add_payments_table():
    """Add payments table to the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # جدول پرداخت‌ها
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_number TEXT UNIQUE NOT NULL,
            patient_id INTEGER NOT NULL,
            appointment_id INTEGER,
            amount REAL NOT NULL,
            discount REAL DEFAULT 0,
            final_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_status TEXT DEFAULT 'Pending',
            payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (appointment_id) REFERENCES appointments(id)
        )
    ''')

    # جدول خدمات (برای محاسبه‌ی هزینه)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    ''')

    # اضافه کردن خدمات پیش‌فرض
    services = [
        ('Consultation', 500000, 'Doctor consultation fee'),
        ('Blood Test', 200000, 'Complete blood count'),
        ('X-Ray', 800000, 'Chest X-ray'),
        ('MRI', 3000000, 'Magnetic resonance imaging'),
        ('ECG', 600000, 'Electrocardiogram'),
        ('Ultrasound', 1200000, 'Ultrasound imaging'),
        ('Vaccination', 300000, 'Vaccine injection'),
        ('Dressing', 150000, 'Wound dressing'),
    ]

    for service in services:
        try:
            cursor.execute('INSERT INTO services (name, price, description) VALUES (?, ?, ?)', service)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print('✅ Payments and services tables created!')


if __name__ == '__main__':
    add_payments_table()
    print('🎉 Database updated successfully!')