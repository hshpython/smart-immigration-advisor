import sqlite3
import re

DB_NAME = 'hospital.db'


def get_connection():
    return sqlite3.connect(DB_NAME)


def is_valid_name(name):
    pattern = r'^[A-Za-z\s\u0600-\u06FF]+$'
    return bool(re.match(pattern, name))


def is_valid_phone(phone):
    pattern = r'^09\d{9}$'
    return bool(re.match(pattern, phone))


def is_valid_national_id(nid):
    return nid.isdigit() and len(nid) == 10


def is_valid_email(email):
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_valid_input(prompt, validator, error_msg):
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f'❌ {error_msg}')
        print('   Please try again.\n')


# ==========================================
# CRUD Operations
# ==========================================

def add_doctor():
    """Add a new doctor"""
    print('\n' + '=' * 50)
    print('➕ Add New Doctor')
    print('=' * 50)

    national_id = get_valid_input(
        'National ID (10 digits): ',
        is_valid_national_id,
        'National ID must be exactly 10 digits!'
    )

    # چک تکراری
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM doctors WHERE national_id = ?', (national_id,))
    if cursor.fetchone():
        print('❌ Doctor with this National ID already exists!')
        conn.close()
        return
    conn.close()

    first_name = get_valid_input(
        'First Name (without Dr.): ',
        is_valid_name,
        'First name must contain only letters!'
    )

    last_name = get_valid_input(
        'Last Name: ',
        is_valid_name,
        'Last name must contain only letters!'
    )

    specialties = ['Cardiology', 'Pediatrics', 'Orthopedics', 'Neurology',
                   'Dermatology', 'Internal Medicine', 'Surgery', 'Radiology']

    print('\nAvailable Specialties:')
    for i, s in enumerate(specialties, 1):
        print(f'  {i}. {s}')

    while True:
        try:
            choice = int(input('Choose specialty (1-8): '))
            if 1 <= choice <= len(specialties):
                specialty = specialties[choice - 1]
                break
            else:
                print('❌ Invalid choice!')
        except ValueError:
            print('❌ Please enter a number!')

    phone = get_valid_input(
        'Phone (09xxxxxxxxx): ',
        is_valid_phone,
        'Phone must start with 09 and be 11 digits!'
    )

    email = input('Email (optional): ').strip()
    if email and not is_valid_email(email):
        print('⚠️  Invalid email format! Skipping...')
        email = ''

    available_days = input('Available Days (e.g., Mon,Wed,Fri): ').strip()

    while True:
        try:
            fee = float(input('Consultation Fee (e.g., 500000): ').strip())
            if fee >= 0:
                break
            else:
                print('❌ Fee cannot be negative!')
        except ValueError:
            print('❌ Please enter a valid number!')

    # ذخیره
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO doctors (national_id, first_name, last_name, specialty, phone, email, available_days, consultation_fee)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (national_id, first_name, last_name, specialty, phone, email, available_days, fee))
    conn.commit()
    conn.close()

    print(f'\n✅ Doctor " {first_name} {last_name}" added successfully!')


def view_all_doctors():
    """View all doctors"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM doctors ORDER BY specialty, last_name')
    doctors = cursor.fetchall()
    conn.close()

    if not doctors:
        print('📭 No doctors found.')
        return

    print('\n' + '=' * 100)
    print(f'📋 All Doctors ({len(doctors)})')
    print('=' * 100)
    print(f'{"ID":<5} {"Name":<25} {"Specialty":<20} {"Phone":<13} {"Fee":<12}')
    print('-' * 100)

    for d in doctors:
        did, nid, first, last, spec, phone, email, days, fee = d
        print(f'{did:<5} {first + " " + last:<20} {spec:<20} {phone:<13} {fee:,.0f}')


def search_doctor():
    """Search for a doctor"""
    query = input('Enter name or specialty: ').strip()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM doctors 
        WHERE first_name LIKE ? OR last_name LIKE ? OR specialty LIKE ?
    ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
    doctors = cursor.fetchall()
    conn.close()

    if not doctors:
        print(f'❌ No doctors found for "{query}"')
        return

    print(f'\n✅ Found {len(doctors)} doctor(s):')
    print('-' * 100)

    for d in doctors:
        did, nid, first, last, spec, phone, email, days, fee = d
        print(f'\n🆔 ID: {did}')
        print(f'👨‍⚕️  Name: {first} {last}')
        print(f'🏥 Specialty: {spec}')
        print(f'📞 Phone: {phone}')
        print(f'📧 Email: {email or "N/A"}')
        print(f'📅 Available: {days or "N/A"}')
        print(f'💰 Fee: {fee:,.0f}')
        print('-' * 100)


def edit_doctor():
    """Edit doctor information"""
    did = input('Enter doctor ID to edit: ').strip()

    if not did.isdigit():
        print('❌ Invalid ID!')
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM doctors WHERE id = ?', (int(did),))
    doctor = cursor.fetchone()

    if not doctor:
        print(f'❌ Doctor with ID {did} not found!')
        conn.close()
        return

    print(f'\n📝 Editing: Dr. {doctor[2]} {doctor[3]}')
    print('💡 Press Enter to keep current value.\n')

    new_phone = input(f'Phone [{doctor[5]}]: ').strip()
    if new_phone and is_valid_phone(new_phone):
        cursor.execute('UPDATE doctors SET phone = ? WHERE id = ?', (new_phone, int(did)))
    elif new_phone:
        print('⚠️  Invalid phone! Skipping...')

    new_email = input(f'Email [{doctor[6] or "N/A"}]: ').strip()
    if new_email:
        if is_valid_email(new_email):
            cursor.execute('UPDATE doctors SET email = ? WHERE id = ?', (new_email, int(did)))
        else:
            print('⚠️  Invalid email! Skipping...')

    new_days = input(f'Available Days [{doctor[7] or "N/A"}]: ').strip()
    if new_days:
        cursor.execute('UPDATE doctors SET available_days = ? WHERE id = ?', (new_days, int(did)))

    new_fee = input(f'Consultation Fee [{doctor[8]:,.0f}]: ').strip()
    if new_fee:
        try:
            fee = float(new_fee)
            if fee >= 0:
                cursor.execute('UPDATE doctors SET consultation_fee = ? WHERE id = ?', (fee, int(did)))
            else:
                print('⚠️  Fee cannot be negative! Skipping...')
        except ValueError:
            print('⚠️  Invalid fee! Skipping...')

    conn.commit()
    conn.close()
    print(f'\n✅ Doctor updated successfully!')


def delete_doctor():
    """Delete a doctor"""
    did = input('Enter doctor ID to delete: ').strip()

    if not did.isdigit():
        print('❌ Invalid ID!')
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, last_name FROM doctors WHERE id = ?', (int(did),))
    doctor = cursor.fetchone()

    if not doctor:
        print(f'❌ Doctor with ID {did} not found!')
        conn.close()
        return

    # چک نوبت‌های فعال
    cursor.execute('SELECT COUNT(*) FROM appointments WHERE doctor_id = ? AND status = "Scheduled"', (int(did),))
    active_appointments = cursor.fetchone()[0]

    if active_appointments > 0:
        print(f'⚠️  This doctor has {active_appointments} active appointments!')
        print('   Cancel them first or reassign.')
        conn.close()
        return

    confirm = input(f'⚠️  Delete "Dr. {doctor[0]} {doctor[1]}"? (yes/no): ').strip().lower()

    if confirm == 'yes':
        cursor.execute('DELETE FROM doctors WHERE id = ?', (int(did),))
        conn.commit()
        print(f'✅ Doctor deleted!')
    else:
        print('❌ Cancelled.')

    conn.close()


# ==========================================
# Main Menu
# ==========================================

def main():
    """Main program"""
    print('=' * 50)
    print('🏥 Hospital Management - Doctors')
    print('=' * 50)

    while True:
        print('\n📋 Menu:')
        print('1. ➕ Add doctor')
        print('2. 👁️  View all doctors')
        print('3. 🔍 Search doctor')
        print('4. ✏️  Edit doctor')
        print('5. 🗑️  Delete doctor')
        print('6. 🚪 Quit')

        choice = input('\nEnter choice (1-6): ').strip()

        if choice == '1':
            add_doctor()
        elif choice == '2':
            view_all_doctors()
        elif choice == '3':
            search_doctor()
        elif choice == '4':
            edit_doctor()
        elif choice == '5':
            delete_doctor()
        elif choice == '6':
            print('👋 Goodbye!')
            break
        else:
            print('❌ Invalid choice!')


if __name__ == '__main__':
    main()