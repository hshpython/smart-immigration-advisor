import sqlite3
from datetime import datetime

DB_NAME = 'hospital.db'


def create_tables():
    """Create all tables in the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # جدول بیماران
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            national_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT,
            blood_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول پزشکان
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            national_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            available_days TEXT,
            consultation_fee REAL
        )
    ''')

    # جدول نوبت‌ها
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT DEFAULT 'Scheduled',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        )
    ''')

    # جدول پرونده پزشکی
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            diagnosis TEXT NOT NULL,
            prescription TEXT,
            notes TEXT,
            visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        )
    ''')

    conn.commit()
    conn.close()
    print('✅ Database and tables created successfully!')


def add_sample_data():
    """Add sample data for testing"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # نمونه بیماران
    patients = [
        ('0012345678', 'Ali', 'Rezaei', 35, 'Male', '09121234567', 'ali@example.com', 'Tehran', 'A+'),
        ('0023456789', 'Sara', 'Ahmadi', 28, 'Female', '09129876543', 'sara@example.com', 'Isfahan', 'B+'),
        ('0034567890', 'Reza', 'Karimi', 42, 'Male', '09131112233', 'reza@example.com', 'Shiraz', 'O+'),
        ('0045678901', 'Maryam', 'Hosseini', 31, 'Female', '09134445566', 'maryam@example.com', 'Tabriz', 'AB+'),
        ('0056789012', 'Hossein', 'Shahabi', 43, 'Male', '09135557788', 'hossein@example.com', 'Qom', 'A-'),
    ]

    for p in patients:
        try:
            cursor.execute('''
                INSERT INTO patients (national_id, first_name, last_name, age, gender, phone, email, address, blood_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', p)
        except sqlite3.IntegrityError:
            pass  # Skip if already exists

    # نمونه پزشکان
    doctors = [
        ('1012345678', 'Dr. Ahmad', 'Tehrani', 'Cardiology', '09121110000', 'ahmad@hospital.com', 'Mon,Wed,Fri',
         500000),
        ('1023456789', 'Dr. Fatemeh', 'Alavi', 'Pediatrics', '09122220000', 'fatemeh@hospital.com', 'Sat,Mon,Wed',
         400000),
        ('1034567890', 'Dr. Mohammad', 'Rahimi', 'Orthopedics', '09123330000', 'mohammad@hospital.com', 'Sun,Tue,Thu',
         600000),
        ('1045678901', 'Dr. Zahra', 'Sadeghi', 'Neurology', '09124440000', 'zahra@hospital.com', 'Mon,Wed', 700000),
        ('1056789012', 'Dr. Reza', 'Moradi', 'Dermatology', '09125550000', 'reza.m@hospital.com', 'Tue,Thu,Sat',
         350000),
    ]

    for d in doctors:
        try:
            cursor.execute('''
                INSERT INTO doctors (national_id, first_name, last_name, specialty, phone, email, available_days, consultation_fee)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', d)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print('✅ Sample data added successfully!')


def show_tables():
    """Show all tables and row counts"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print('\n' + '=' * 50)
    print('📊 Database Status')
    print('=' * 50)

    for table in ['patients', 'doctors', 'appointments', 'medical_records']:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f'📋 {table}: {count} records')

    conn.close()
    print('=' * 50)


if __name__ == '__main__':
    print('🏥 Hospital Database Setup')
    print('=' * 50)

    create_tables()
    add_sample_data()
    show_tables()

    print('\n✅ Database is ready!')
    print(f'📁 Database file: {DB_NAME}')