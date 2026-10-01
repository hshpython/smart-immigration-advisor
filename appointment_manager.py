import sqlite3
import re
from datetime import datetime, date

DB_NAME = 'hospital.db'


def get_connection():
    return sqlite3.connect(DB_NAME)


def is_valid_date(date_str):
    """Check date format YYYY-MM-DD"""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_valid_time(time_str):
    """Check time format HH:MM"""
    pattern = r'^\d{2}:\d{2}$'
    if not re.match(pattern, time_str):
        return False
    try:
        hour, minute = time_str.split(':')
        return 0 <= int(hour) < 24 and 0 <= int(minute) < 60
    except ValueError:
        return False


# ==========================================
# Helper Functions
# ==========================================

def list_patients():
    """List all patients for selection"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, national_id FROM patients ORDER BY last_name')
    patients = cursor.fetchall()
    conn.close()

    if not patients:
        print('📭 No patients in database!')
        return None

    print('\n📋 Available Patients:')
    for p in patients:
        print(f'  ID {p[0]}: {p[1]} {p[2]} (National ID: {p[3]})')

    return patients


def list_doctors():
    """List all doctors for selection"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, specialty, consultation_fee FROM doctors ORDER BY specialty')
    doctors = cursor.fetchall()
    conn.close()

    if not doctors:
        print('📭 No doctors in database!')
        return None

    print('\n📋 Available Doctors:')
    for d in doctors:
        print(f'  ID {d[0]}: {d[1]} {d[2]} ({d[3]}) - Fee: {d[4]:,.0f}')

    return doctors


def is_time_slot_free(doctor_id, date_str, time_str):
    """Check if time slot is free"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM appointments 
        WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ? 
        AND status = 'Scheduled'
    ''', (doctor_id, date_str, time_str))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0


# ==========================================
# CRUD Operations
# ==========================================

def create_appointment():
    """Create a new appointment"""
    print('\n' + '=' * 50)
    print('➕ New Appointment')
    print('=' * 50)

    # انتخاب بیمار
    patients = list_patients()
    if not patients:
        return

    while True:
        try:
            patient_id = int(input('\nEnter Patient ID: '))
            if any(p[0] == patient_id for p in patients):
                break
            print('❌ Invalid Patient ID!')
        except ValueError:
            print('❌ Please enter a number!')

    # انتخاب پزشک
    doctors = list_doctors()
    if not doctors:
        return

    while True:
        try:
            doctor_id = int(input('\nEnter Doctor ID: '))
            if any(d[0] == doctor_id for d in doctors):
                break
            print('❌ Invalid Doctor ID!')
        except ValueError:
            print('❌ Please enter a number!')

    # تاریخ
    while True:
        date_str = input('\nAppointment Date (YYYY-MM-DD): ').strip()
        if is_valid_date(date_str):
            if date_str >= str(date.today()):
                break
            print('❌ Date must be today or in the future!')
        else:
            print('❌ Invalid date format! Use YYYY-MM-DD')

    # ساعت
    while True:
        time_str = input('Appointment Time (HH:MM): ').strip()
        if is_valid_time(time_str):
            if is_time_slot_free(doctor_id, date_str, time_str):
                break
            print('❌ This time slot is already taken! Choose another time.')
        else:
            print('❌ Invalid time format! Use HH:MM')

    notes = input('Notes (optional): ').strip()

    # ذخیره
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
        VALUES (?, ?, ?, ?, 'Scheduled', ?)
    ''', (patient_id, doctor_id, date_str, time_str, notes))
    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()

    print(f'\n✅ Appointment #{appointment_id} created successfully!')
    print(f'   📅 {date_str} at {time_str}')


def view_all_appointments():
    """View all appointments"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            a.id, a.appointment_date, a.appointment_time, a.status,
            p.first_name || ' ' || p.last_name AS patient_name,
            p.national_id AS patient_nid,
            d.first_name || ' ' || d.last_name AS doctor_name,
            d.specialty
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
    ''')
    appointments = cursor.fetchall()
    conn.close()

    if not appointments:
        print('📭 No appointments found.')
        return

    print('\n' + '=' * 110)
    print(f'📋 All Appointments ({len(appointments)})')
    print('=' * 110)
    print(f'{"ID":<5} {"Date":<12} {"Time":<7} {"Patient":<22} {"Doctor":<22} {"Specialty":<18} {"Status":<12}')
    print('-' * 110)

    for a in appointments:
        aid, date_str, time_str, status, patient, pnid, doctor, specialty = a
        status_icon = '✅' if status == 'Scheduled' else '✔️' if status == 'Completed' else '❌'
        print(
            f'{aid:<5} {date_str:<12} {time_str:<7} {patient:<22} Dr. {doctor:<19} {specialty:<18} {status_icon} {status}')

    print('=' * 110)


def view_appointments_by_date():
    """View appointments by date"""
    date_str = input('Enter date (YYYY-MM-DD): ').strip()

    if not is_valid_date(date_str):
        print('❌ Invalid date!')
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            a.id, a.appointment_time, a.status,
            p.first_name || ' ' || p.last_name AS patient_name,
            p.phone AS patient_phone,
            d.first_name || ' ' || d.last_name AS doctor_name,
            d.specialty
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.appointment_date = ?
        ORDER BY a.appointment_time
    ''', (date_str,))
    appointments = cursor.fetchall()
    conn.close()

    if not appointments:
        print(f'📭 No appointments on {date_str}')
        return

    print(f'\n📅 Appointments on {date_str} ({len(appointments)})')
    print('=' * 110)

    for a in appointments:
        aid, time_str, status, patient, phone, doctor, specialty = a
        print(f'\n🆔 Appointment #{aid}')
        print(f'   ⏰ Time: {time_str}')
        print(f'   👤 Patient: {patient} ({phone})')
        print(f'   👨‍⚕️  Doctor: {doctor} ({specialty})')
        print(f'   📊 Status: {status}')
        print('-' * 110)


def update_appointment_status():
    """Update appointment status"""
    aid = input('Enter appointment ID: ').strip()

    if not aid.isdigit():
        print('❌ Invalid ID!')
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments WHERE id = ?', (int(aid),))
    appointment = cursor.fetchone()

    if not appointment:
        print(f'❌ Appointment #{aid} not found!')
        conn.close()
        return

    print(f'\n📊 Current status: {appointment[5]}')
    print('\nNew status options:')
    print('1. Scheduled')
    print('2. Completed')
    print('3. Cancelled')

    choice = input('Choose (1-3): ').strip()

    status_map = {'1': 'Scheduled', '2': 'Completed', '3': 'Cancelled'}
    new_status = status_map.get(choice)

    if not new_status:
        print('❌ Invalid choice!')
        conn.close()
        return

    cursor.execute('UPDATE appointments SET status = ? WHERE id = ?', (new_status, int(aid)))
    conn.commit()
    conn.close()

    print(f'✅ Appointment status updated to "{new_status}"')


def cancel_appointment():
    """Cancel an appointment"""
    aid = input('Enter appointment ID to cancel: ').strip()

    if not aid.isdigit():
        print('❌ Invalid ID!')
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments WHERE id = ?', (int(aid),))
    appointment = cursor.fetchone()

    if not appointment:
        print(f'❌ Appointment #{aid} not found!')
        conn.close()
        return

    if appointment[5] == 'Cancelled':
        print('⚠️  This appointment is already cancelled!')
        conn.close()
        return

    confirm = input(f'⚠️  Cancel appointment #{aid}? (yes/no): ').strip().lower()

    if confirm == 'yes':
        cursor.execute('UPDATE appointments SET status = ? WHERE id = ?', ('Cancelled', int(aid)))
        conn.commit()
        print(f'✅ Appointment #{aid} cancelled!')
    else:
        print('❌ Cancelled.')

    conn.close()


# ==========================================
# Main Menu
# ==========================================

def main():
    """Main program"""
    print('=' * 50)
    print('🏥 Hospital Management - Appointments')
    print('=' * 50)

    while True:
        print('\n📋 Menu:')
        print('1. ➕ New appointment')
        print('2. 👁️  View all appointments')
        print('3. 📅 View by date')
        print('4. ✏️  Update status')
        print('5. ❌ Cancel appointment')
        print('6. 🚪 Quit')

        choice = input('\nEnter choice (1-6): ').strip()

        if choice == '1':
            create_appointment()
        elif choice == '2':
            view_all_appointments()
        elif choice == '3':
            view_appointments_by_date()
        elif choice == '4':
            update_appointment_status()
        elif choice == '5':
            cancel_appointment()
        elif choice == '6':
            print('👋 Goodbye!')
            break
        else:
            print('❌ Invalid choice!')


if __name__ == '__main__':
    main()