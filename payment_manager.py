import sqlite3
from datetime import datetime
import random

DB_NAME = 'hospital.db'


def get_connection():
    return sqlite3.connect(DB_NAME)


def generate_receipt_number():
    """Generate unique receipt number"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_num = random.randint(100, 999)
    return f'RCP-{timestamp}-{random_num}'


def list_patients():
    """List all patients for selection"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name FROM patients ORDER BY last_name')
    patients = cursor.fetchall()
    conn.close()

    if not patients:
        print('📭 No patients!')
        return []

    print('\n📋 Patients:')
    for p in patients:
        print(f'  ID {p[0]}: {p[1]} {p[2]}')
    return patients


def list_services():
    """List all services"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, price FROM services ORDER BY name')
    services = cursor.fetchall()
    conn.close()

    print('\n💼 Available Services:')
    for s in services:
        print(f'  ID {s[0]}: {s[1]} - {s[2]:,.0f}')
    return services


def create_payment():
    """Create a new payment"""
    print('\n' + '=' * 50)
    print('💰 New Payment')
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
            print('❌ Invalid ID!')
        except ValueError:
            print('❌ Enter a number!')

    # انتخاب خدمات
    services = list_services()
    if not services:
        return

    print('\n💡 You can add multiple services (type 0 to finish)')
    selected_services = []
    total_amount = 0

    while True:
        try:
            service_id = int(input('Enter Service ID (0 to finish): '))
            if service_id == 0:
                break
            service = next((s for s in services if s[0] == service_id), None)
            if service:
                quantity = int(input(f'Quantity for {service[1]} (default 1): ') or 1)
                subtotal = service[2] * quantity
                selected_services.append((service[1], quantity, service[2], subtotal))
                total_amount += subtotal
                print(f'   ✅ Added: {service[1]} x{quantity} = {subtotal:,.0f}')
            else:
                print('❌ Invalid service ID!')
        except ValueError:
            print('❌ Enter a number!')

    if not selected_services:
        print('❌ No services selected!')
        return

    # تخفیف
    discount = 0
    discount_input = input('\nDiscount amount (0 if none): ').strip()
    if discount_input:
        try:
            discount = float(discount_input)
        except ValueError:
            discount = 0

    final_amount = total_amount - discount

    # روش پرداخت
    print('\n💳 Payment Method:')
    print('1. Cash')
    print('2. Card')
    print('3. Insurance')
    print('4. Online')

    methods = {'1': 'Cash', '2': 'Card', '3': 'Insurance', '4': 'Online'}
    while True:
        choice = input('Choose (1-4): ').strip()
        if choice in methods:
            payment_method = methods[choice]
            break
        print('❌ Invalid choice!')

    # وضعیت
    status_input = input('\nPaid now? (y/n): ').strip().lower()
    payment_status = 'Paid' if status_input == 'y' else 'Pending'

    notes = input('Notes (optional): ').strip()

    # ذخیره
    receipt_number = generate_receipt_number()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO payments 
        (receipt_number, patient_id, amount, discount, final_amount, payment_method, payment_status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (receipt_number, patient_id, total_amount, discount, final_amount,
          payment_method, payment_status, notes))
    conn.commit()
    conn.close()

    # نمایش رسید
    print('\n' + '=' * 50)
    print('🧾 RECEIPT')
    print('=' * 50)
    print(f'Receipt #: {receipt_number}')
    print(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'Patient ID: {patient_id}')
    print('-' * 50)
    print('Services:')
    for s in selected_services:
        print(f'  {s[0]} x{s[1]} = {s[3]:,.0f}')
    print('-' * 50)
    print(f'Subtotal:  {total_amount:,.0f}')
    print(f'Discount:  -{discount:,.0f}')
    print(f'Total:     {final_amount:,.0f}')
    print(f'Method:    {payment_method}')
    print(f'Status:    {payment_status}')
    print('=' * 50)
    print('✅ Payment recorded!')


def view_all_payments():
    """View all payments"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            p.id, p.receipt_number, p.final_amount, p.payment_method,
            p.payment_status, p.payment_date,
            pt.first_name || ' ' || pt.last_name
        FROM payments p
        JOIN patients pt ON p.patient_id = pt.id
        ORDER BY p.payment_date DESC
    ''')
    payments = cursor.fetchall()
    conn.close()

    if not payments:
        print('📭 No payments found.')
        return

    print('\n' + '=' * 110)
    print(f'💰 All Payments ({len(payments)})')
    print('=' * 110)
    print(f'{"ID":<5} {"Receipt":<25} {"Patient":<22} {"Amount":<15} {"Method":<12} {"Status":<12}')
    print('-' * 110)

    for p in payments:
        status_icon = '✅' if p[4] == 'Paid' else '⏳' if p[4] == 'Pending' else '↩️'
        print(f'{p[0]:<5} {p[1]:<25} {p[6]:<22} {p[2]:>13,.0f} {p[3]:<12} {status_icon} {p[4]}')

    print('=' * 110)


def view_daily_report():
    """View daily income report"""
    date_str = input('Enter date (YYYY-MM-DD) or Enter for today: ').strip()
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            COUNT(*) as total_count,
            SUM(CASE WHEN payment_status = 'Paid' THEN final_amount ELSE 0 END) as total_paid,
            SUM(CASE WHEN payment_status = 'Pending' THEN final_amount ELSE 0 END) as total_pending
        FROM payments
        WHERE DATE(payment_date) = ?
    ''', (date_str,))
    result = cursor.fetchone()
    conn.close()

    print('\n' + '=' * 50)
    print(f'📊 Daily Report - {date_str}')
    print('=' * 50)
    print(f'Total payments: {result[0]}')
    print(f'✅ Paid: {result[1] or 0:,.0f} IRR')
    print(f'⏳ Pending: {result[2] or 0:,.0f} IRR')
    print('=' * 50)


def main():
    """Main program"""
    print('=' * 50)
    print('💰 Hospital Payment System')
    print('=' * 50)

    while True:
        print('\n📋 Menu:')
        print('1. 💰 New Payment')
        print('2. 📋 View All Payments')
        print('3. 📊 Daily Report')
        print('4. 🚪 Quit')

        choice = input('\nChoice (1-4): ').strip()

        if choice == '1':
            create_payment()
        elif choice == '2':
            view_all_payments()
        elif choice == '3':
            view_daily_report()
        elif choice == '4':
            print('👋 Goodbye!')
            break
        else:
            print('❌ Invalid!')


if __name__ == '__main__':
    main()