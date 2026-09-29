import json
import re  # برای اعتبارسنجی با Regex

CONTACTS_FILE = 'contacts.json'


def load_contacts():
    """Load contacts from file"""
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_contacts(contacts):
    """Save contacts to file"""
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)


def is_valid_name(name):
    """Check if name contains only letters and spaces"""
    # فقط حروف (فارسی و انگلیسی) و فاصله
    pattern = r'^[A-Za-z\s\u0600-\u06FF]+$'
    return bool(re.match(pattern, name))


def is_valid_phone(phone):
    """Check if phone contains only digits"""
    # فقط عدد، حداقل ۱۰ رقم
    return phone.isdigit() and len(phone) >= 10


def is_valid_email(email):
    """Check if email has valid format"""
    # قالب: user@domain.com
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_valid_input(prompt, validator, error_message):
    """Keep asking until valid input is provided"""
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f'❌ {error_message}')
        print('   Please try again.\n')


def add_contact(contacts):
    """Add a new contact with validation"""
    print('\n' + '=' * 50)
    print('➕ Add New Contact')
    print('=' * 50)

    # اعتبارسنجی نام
    name = get_valid_input(
        '👤 Enter name (letters only): ',
        is_valid_name,
        'Name must contain only letters (no numbers or symbols)!'
    )

    # چک تکراری بودن
    if name in contacts:
        print(f'⚠️ Contact "{name}" already exists!')
        return

    # اعتبارسنجی تلفن
    phone = get_valid_input(
        '📞 Enter phone (digits only, min 10): ',
        is_valid_phone,
        'Phone must contain only digits (at least 10 digits)!'
    )

    # اعتبارسنجی ایمیل
    email = get_valid_input(
        '📧 Enter email (example: user@domain.com): ',
        is_valid_email,
        'Invalid email format! Must be like: user@domain.com'
    )

    # ذخیره
    contacts[name] = {'phone': phone, 'email': email}
    save_contacts(contacts)

    print('-' * 50)
    print(f'✅ Contact "{name}" added successfully!')
    print('-' * 50)


def view_contacts(contacts):
    """View all contacts"""
    if not contacts:
        print('📭 No contacts found.')
        return

    print('\n' + '=' * 50)
    print('📒 All Contacts:')
    print('=' * 50)
    for name, info in contacts.items():
        print(f'👤 {name}')
        print(f'   📞 Phone: {info["phone"]}')
        print(f'   📧 Email: {info["email"]}')
        print('-' * 50)


def search_contact(contacts):
    """Search for a contact"""
    name = input('Enter name to search: ').strip()
    if name in contacts:
        info = contacts[name]
        print(f'✅ Found: {name}')
        print(f'   📞 Phone: {info["phone"]}')
        print(f'   📧 Email: {info["email"]}')
    else:
        print(f'❌ Contact "{name}" not found!')


def delete_contact(contacts):
    """Delete a contact"""
    name = input('Enter name to delete: ').strip()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        print(f'✅ Contact "{name}" deleted!')
    else:
        print(f'❌ Contact "{name}" not found!')


def edit_contact(contacts):
    """Edit an existing contact"""
    name = input('Enter name to edit: ').strip()

    if name not in contacts:
        print(f'❌ Contact "{name}" not found!')
        return

    print(f'\n📝 Editing "{name}":')
    print(f'   Current phone: {contacts[name]["phone"]}')
    print(f'   Current email: {contacts[name]["email"]}')
    print('\n💡 Press Enter to keep current value, or type new value.\n')

    # ویرایش تلفن
    new_phone = input(f'📞 New phone [{contacts[name]["phone"]}]: ').strip()
    if new_phone:
        if is_valid_phone(new_phone):
            contacts[name]['phone'] = new_phone
        else:
            print('❌ Invalid phone! Keeping old value.')

    # ویرایش ایمیل
    new_email = input(f'📧 New email [{contacts[name]["email"]}]: ').strip()
    if new_email:
        if is_valid_email(new_email):
            contacts[name]['email'] = new_email
        else:
            print('❌ Invalid email! Keeping old value.')

    save_contacts(contacts)
    print(f'\n✅ Contact "{name}" updated successfully!')


def main():
    """Main program"""
    contacts = load_contacts()

    print('=' * 50)
    print('📞 Phone Book Application')
    print('=' * 50)

    while True:
        print('\n📋 Menu:')
        print('1. ➕ Add contact')
        print('2. 👁️  View all contacts')
        print('3. 🔍 Search contact')
        print('4. ✏️  Edit contact')
        print('5. 🗑️  Delete contact')
        print('6. 🚪 Quit')

        choice = input('\nEnter your choice (1-6): ').strip()

        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            view_contacts(contacts)
        elif choice == '3':
            search_contact(contacts)
        elif choice == '4':
            edit_contact(contacts)
        elif choice == '5':
            delete_contact(contacts)
        elif choice == '6':
            print('👋 Goodbye!')
            break
        else:
            print('❌ Invalid choice! Please try again.')


if __name__ == '__main__':
    main()