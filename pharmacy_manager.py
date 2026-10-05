import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'hospital.db'


def get_connection():
    return sqlite3.connect(DB_NAME)


def list_medicines():
    """List all medicines"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, category, price, stock_quantity FROM medicines ORDER BY name')
    meds = cursor.fetchall()
    conn.close()

    if not meds:
        print('📭 No medicines!')
        return []

    print('\n💊 Medicines:')
    print(f'{"ID":<5} {"Name":<25} {"Category":<15} {"Price":<12} {"Stock":<8}')
    print('-' * 70)
    for m in meds:
        stock = m[4]
        warning = ''
        if stock < 0:
            warning = ' ❌ (منفی!)'
        elif stock < 20:
            warning = ' ⚠️'
        print(f'{m[0]:<5} {m[1]:<25} {m[2]:<15} {m[3]:>10,.0f} {stock:>6}{warning}')
    return meds


def list_patients():
    """List all patients"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name FROM patients ORDER BY last_name')
    patients = cursor.fetchall()
    conn.close()

    if not patients:
        return []

    print('\n👥 Patients:')
    for p in patients:
        print(f'  ID {p[0]}: {p[1]} {p[2]}')
    return patients


def sell_medicine():
    """Sell medicine to a patient with proper stock validation"""
    print('\n' + '=' * 50)
    print('💊 Sell Medicine')
    print('=' * 50)

    patients = list_patients()
    if not patients:
        print('❌ No patients!')
        return

    while True:
        try:
            patient_id = int(input('\nEnter Patient ID: '))
            if any(p[0] == patient_id for p in patients):
                break
            print('❌ Invalid ID!')
        except ValueError:
            print('❌ Enter a number!')

    meds = list_medicines()
    if not meds:
        return

    # ✅ فیلتر: فقط داروهایی که موجودی مثبت دارن
    available_meds = [m for m in meds if m[4] > 0]
    if not available_meds:
        print('❌ No medicines in stock!')
        return

    cart = []
    total = 0

    while True:
        try:
            med_id = int(input('\nEnter Medicine ID (0 to finish): '))
            if med_id == 0:
                break

            med = next((m for m in available_meds if m[0] == med_id), None)
            if not med:
                print('❌ Invalid ID or out of stock!')
                continue

            max_qty = med[4]
            qty_str = input(f'Quantity for {med[1]} (max {max_qty}): ').strip()
            if not qty_str:
                continue
            qty = int(qty_str)

            if qty <= 0:
                print('❌ Quantity must be positive!')
                continue
            if qty > max_qty:
                print(f'❌ Only {max_qty} available!')
                continue

            line_total = med[3] * qty
            cart.append((med[0], med[1], qty, med[3], line_total))
            total += line_total
            print(f'   ✅ Added: {med[1]} x{qty} = {line_total:,.0f}')

            # ✅ آپدیت موجودی در حافظه برای جلوگیری از انتخاب دوباره بیشتر از موجودی
            med_list = list(med)
            med_list[4] -= qty
            available_meds = [m if m[0] != med[0] else tuple(med_list) for m in available_meds]

        except ValueError:
            print('❌ Enter a number!')

    if not cart:
        print('❌ No items!')
        return

    print('\n📋 Cart:')
    for item in cart:
        print(f'  {item[1]} x{item[2]} = {item[4]:,.0f}')
    print(f'\n💰 TOTAL: {total:,.0f} IRR')

    confirm = input('\n✅ Confirm sale? (y/n): ').strip().lower()
    if confirm != 'y':
        print('❌ Cancelled.')
        return

    # ✅ ذخیره در دیتابیس
    conn = get_connection()
    cursor = conn.cursor()

    for med_id, med_name, qty, unit_price, line_total in cart:
        cursor.execute('''
            INSERT INTO medicine_sales (medicine_id, patient_id, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (med_id, patient_id, qty, unit_price, line_total))

        cursor.execute('''
            UPDATE medicines SET stock_quantity = stock_quantity - ? WHERE id = ?
        ''', (qty, med_id))

    conn.commit()
    conn.close()

    print(f'\n✅ Sale completed! Total: {total:,.0f} IRR')


def add_stock():
    """Add stock to a medicine"""
    print('\n' + '=' * 50)
    print('📦 Add Stock')
    print('=' * 50)

    meds = list_medicines()
    if not meds:
        return

    try:
        med_id = int(input('\nEnter Medicine ID: '))
        med = next((m for m in meds if m[0] == med_id), None)
        if not med:
            print('❌ Invalid ID!')
            return

        qty_str = input(f'Quantity to add for {med[1]}: ').strip()
        if not qty_str:
            return
        qty = int(qty_str)

        if qty <= 0:
            print('❌ Invalid quantity!')
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE medicines SET stock_quantity = stock_quantity + ? WHERE id = ?',
                       (qty, med_id))
        conn.commit()
        conn.close()

        print(f'✅ Added {qty} units of "{med[1]}"')
        print(f'   New stock: {med[4] + qty}')

    except ValueError:
        print('❌ Enter a number!')


def low_stock_report():
    """Show medicines with low stock"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, stock_quantity, min_stock 
        FROM medicines 
        WHERE stock_quantity < min_stock
        ORDER BY stock_quantity
    ''')
    low = cursor.fetchall()
    conn.close()

    if not low:
        print('✅ All medicines have sufficient stock!')
        return

    print('\n' + '=' * 60)
    print('⚠️  LOW STOCK ALERT')
    print('=' * 60)
    for name, stock, min_stock in low:
        if stock < 0:
            print(f'  ❌ {name:<30} Stock: {stock:<5} (منفی!) (min: {min_stock})')
        else:
            print(f'  ⚠️  {name:<30} Stock: {stock:<5} (min: {min_stock})')
    print('=' * 60)


def sales_report():
    """Show sales report"""
    date_str = input('Date (YYYY-MM-DD) or Enter for today: ').strip()
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # ✅ اعتبارسنجی قالب تاریخ
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print('❌ Invalid date format! Use YYYY-MM-DD')
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            COUNT(*) as total_sales,
            SUM(quantity) as total_items,
            SUM(total_price) as total_revenue
        FROM medicine_sales
        WHERE DATE(sale_date) = ?
    ''', (date_str,))
    result = cursor.fetchone()
    conn.close()

    print('\n' + '=' * 50)
    print(f'📊 Sales Report - {date_str}')
    print('=' * 50)
    print(f'Total sales: {result[0]}')
    print(f'Total items: {result[1] or 0}')
    print(f'Total revenue: {result[2] or 0:,.0f} IRR')
    print('=' * 50)


def fix_negative_stock():
    """Fix negative stock values (set to 0)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE medicines SET stock_quantity = 0 WHERE stock_quantity < 0')
    affected = cursor.rowcount
    conn.commit()
    conn.close()

    if affected > 0:
        print(f'✅ Fixed {affected} medicine(s) with negative stock')
    else:
        print('✅ No negative stock found')


def main():
    """Main menu"""
    print('=' * 50)
    print('💊 Pharmacy Management')
    print('=' * 50)

    # ✅ اول از همه: اصلاح موجودی منفی
    fix_negative_stock()

    while True:
        print('\n📋 Menu:')
        print('1. 💊 List all medicines')
        print('2. 💰 Sell medicine')
        print('3. 📦 Add stock')
        print('4. ⚠️  Low stock alert')
        print('5. 📊 Sales report')
        print('6. 🚪 Quit')

        choice = input('\nChoice (1-6): ').strip()

        if choice == '1':
            list_medicines()
        elif choice == '2':
            sell_medicine()
        elif choice == '3':
            add_stock()
        elif choice == '4':
            low_stock_report()
        elif choice == '5':
            sales_report()
        elif choice == '6':
            print('👋 Goodbye!')
            break
        else:
            print('❌ Invalid! Please choose 1-6.')


if __name__ == '__main__':
    main()