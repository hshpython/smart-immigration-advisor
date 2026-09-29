def add(a, b):
    """Add two numbers"""
    return a + b


def subtract(a, b):
    """Subtract two numbers"""
    return a - b


def multiply(a, b):
    """Multiply two numbers"""
    return a * b


def divide(a, b):
    """Divide two numbers"""
    if b == 0:
        return 'Error: Division by zero!'
    return a / b


def power(a, b):
    """Calculate a to the power of b"""
    return a ** b


def modulo(a, b):
    """Calculate remainder of a divided by b"""
    if b == 0:
        return 'Error: Division by zero!'
    return a % b


# دیکشنری عملیات
operations = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
    '**': power,
    '%': modulo,
}


def calculator():
    """Main calculator function"""
    print('=' * 50)
    print('🧮 Simple Calculator')
    print('=' * 50)
    print('Operations:')
    print('  +  : Addition')
    print('  -  : Subtraction')
    print('  *  : Multiplication')
    print('  /  : Division')
    print('  ** : Power')
    print('  %  : Modulo')
    print('  q  : Quit')
    print('=' * 50)

    while True:
        try:
            # دریافت عدد اول
            num1_input = input('\nEnter first number (or "q" to quit): ')
            if num1_input.lower() == 'q':
                print('👋 Goodbye!')
                break
            num1 = float(num1_input)

            # دریافت عملیات
            operator = input('Enter operator (+, -, *, /, **, %): ').strip()
            if operator not in operations:
                print('❌ Invalid operator! Please try again.')
                continue

            # دریافت عدد دوم
            num2 = float(input('Enter second number: '))

            # محاسبه
            result = operations[operator](num1, num2)

            # بعد از محاسبه
            if isinstance(result, float) and result.is_integer():
                result = int(result)  # تبدیل به عدد صحیح

            print(f'✅ Result: {num1} {operator} {num2} = {result}')

            # نمایش نتیجه
            print('-' * 50)
            print(f'✅ Result: {num1} {operator} {num2} = {result}')
            print('-' * 50)

        except ValueError:
            print('❌ Invalid input! Please enter numbers only.')
        except Exception as e:
            print(f'❌ Error: {e}')


# اجرای ماشین‌حساب
if __name__ == '__main__':
    calculator()