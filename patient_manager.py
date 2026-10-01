import sqlite3
import re
from datetime import datetime

DB_NAME = 'hospital.db'


def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_NAME)


def is_valid_name(name):
    """Check if name contains only letters"""
    pattern = r'^[A-Za-z\s\u0600-\u06FF]+$'
    return bool(re.match(pattern, name))


def is_valid_phone(phone):
    """Check if phone is valid Iranian number"""
    pattern = r'^09\d{9}$'
    return bool(re.match(pattern, phone))


def is_valid_national_id(nid):
    """Check if national ID is 10 digits"""
    return nid.isdigit() and len(nid) == 10


def is_valid_email(email):
    """Check email format"""
    if not email:
        return True  # Email is optional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_valid_input(prompt, validator, error_msg):
    """Keep asking until valid input"""
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f'❌ {error_msg}')
        print('   Please try again.\n')


# ==========================================
# CRUD Operations
# ==========================================

def add_patient():
    """Add a new patient"""
    print('\n' + '=' * 50)
    print('➕ Add New Patient')
    print('=' * 50)

    national_id = get_valid_input(
        'National ID (10 digits): ',
        is_valid_national_id,
        'National ID must be exactly 10 digits!'
    )

    # چک تکراری
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE national_id = ?', (national_id,))
    if cursor.fetchone():
        print('❌ Patient with this National ID already exists!')
        conn.close()
        return
    conn.close()

    first_name = get_valid_input(
        'First Name: ',
        is_valid_name,
        'First name must contain only letters!'
    )

    last_name = get_valid_input(
        'Last Name: ',
        is_valid_name,
        'Last name must contain only letters!'
    )

    age = get_valid_input(
        'Age: ',
        lambda x: x.isdigit() and 0 < int(x) < 120,
        'Age must be a number between 1 and 120!'
    )

    gender = get_valid_input(
        'Gender (Male/Female): ',
        lambda x: x.lower() in ['male', 'female'],
        'Gender must be Male or Female!'
    ).capitalize()

    phone = get_valid_input(
        'Phone (09xxxxxxxxx): ',
        is_valid_phone,
        'Phone must start with 09 and be 11 digits!'
    )

    email = input('Email (optional): ').strip()
    if email and not is_valid_email(email):
        print('⚠️  Invalid email format! Skipping...')
        email = ''

    address = input('Address: ').strip()

    blood_type = get_valid_input(
        'Blood Type (A+/A-/B+/B-/AB+/AB-/O+/O-): ',
        lambda x: x.upper() in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'Invalid blood type!'
    ).upper()

    # ذخیره
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (national_id, first_name, last_name, age, gender, phone, email, address, blood_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (national_id, first_name, last_name, int(age), gender, phone, email, address, blood_type))
    conn.commit()
    conn.close()

    print(f'\n✅ Patient "{first_name} {last_name}" added successfully!')


def view_all_patients():
    """View all patients"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients ORDER BY last_name, first_name')
    patients = cursor.fetchall()
    conn.close()

    if not patients:
        print('📭 No patients found.')
        return

    print('\n' + '=' * 90)
    print(f'📋 All Patients ({len(patients)})')
    print('=' * 90)
    print(f'{"ID":<5} {"Name":<25} {"Age":<5} {"Gender":<8} {"Phone":<13} {"Blood":<6}')
    print('-' * 90)

    for p in patients:
        pid, nid, first, last, age, gender, phone, email, address, blood, created = p
        print(f'{pid:<5} {first + " " + last:<25} {age:<5} {gender:<8} {phone:<13} {blood:<6}')

    print('=' * 90)


def search_patient():
    """Search for a patient"""
    query = input('Enter name, national ID, or phone: ').strip()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM patients 
        WHERE first_name LIKE ? OR last_name LIKE ? 
           OR national_id = ? OR phone = ?
    ''', (f'%{query}%', f'%{query}%', query, query))
    patients = cursor.fetchall()
    conn.close()

    if not patients:
        print(f'❌ No patients found for "{query}"')
        return

    print(f'\n✅ Found {len(patients)} patient(s):')
    print('-' * 90)

    for p in patients:
        pid, nid, first, last, age, gender, phone, email, address, blood, created = p
        print(f'\n🆔 ID: {pid}')
        print(f'👤 Name: {first} {last}')
        print(f'📅 Age: {age} | Gender: {gender}')
        print(f'📞 Phone: {phone}')
        print(f'📧 Email: {email or "N/A"}')
        print(f'🏠 Address: {address or "N/A"}')
        print(f'🩸 Blood Type: {blood}')
        print(f'📅 Registered: {created}')
        print('-' * 90)


def edit_patient():
    """Edit patient information"""
    pid = input('Enter patient ID to edit: ').strip()

    if not pid.isdigit():
        print('❌ Invalid ID!')
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE id = ?', (int(pid),))
    patient = cursor.fetchone()

    if not patient:
        print(f'❌ Patient with ID {pid} not found!')
        conn.close()
        return

    print(f'\n📝 Editing: {patient[2]} {patient[3]}')
    print('💡 Press Enter to keep current value.\n')

    # دریافت مقادیر جدید
    new_phone = input(f'Phone [{patient[6]}]: ').strip()
    if new_phone and is_valid_phone(new_phone):
        cursor.execute('UPDATE patients SET phone = ? WHERE id = ?', (new_phone, int(pid)))
    elif new_phone:
        print('⚠️  Invalid phone! Skipping...')

    new_email = input(f'Email [{patient[7] or "N/A"}]: ').strip()
    if new_email:
        if is_valid_email(new_email):
            cursor.execute('UPDATE patients SET email = ? WHERE id = ?', (new_email, int(pid)))
        else:
            print('⚠️  Invalid email! Skipping...')

    new_address = input(f'Address [{patient[8] or "N/A"}]: ').strip()
    if new_address:
        cursor.execute('UPDATE patients SET address = ? WHERE id = ?', (new_address, int(pid)))

    conn.commit()
    conn.close()
    print(f'\n✅ Patient updated successfully!')


def delete_patient():
    """Delete a patient"""
    pid = input('Enter patient ID to delete: ').strip()

    if not pid.isdigit():
        print('❌ Invalid ID!')
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, last_name FROM patients WHERE id = ?', (int(pid),))
    patient = cursor.fetchone()

    if not patient:
        print(f'❌ Patient with ID {pid} not found!')
        conn.close()
        return

    confirm = input(f'⚠️  Delete "{patient[0]} {patient[1]}"? (yes/no): ').strip().lower()

    if confirm == 'yes':
        cursor.execute('DELETE FROM patients WHERE id = ?', (int(pid),))
        conn.commit()
        print(f'✅ Patient deleted!')
    else:
        print('❌ Cancelled.')

    conn.close()


# ==========================================
# Main Menu
# ==========================================

def main():
    """Main program"""
    print('=' * 50)
    print('🏥 Hospital Management - Patients')
    print('=' * 50)

    while True:
        print('\n📋 Menu:')
        print('1. ➕ Add patient')
        print('2. 👁️  View all patients')
        print('3. 🔍 Search patient')
        print('4. ✏️  Edit patient')
        print('5. 🗑️  Delete patient')
        print('6. 🚪 Quit')

        choice = input('\nEnter choice (1-6): ').strip()

        if choice == '1':
            add_patient()
        elif choice == '2':
            view_all_patients()
        elif choice == '3':
            search_patient()
        elif choice == '4':
            edit_patient()
        elif choice == '5':
            delete_patient()
        elif choice == '6':
            print('👋 Goodbye!')
            break
        else:
            print('❌ Invalid choice!')


if __name__ == '__main__':
    main()