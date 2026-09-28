import random


def play_game(min_num=1, max_num=100, max_attempts=10):
    """Play the number guessing game"""
    print('=' * 50)
    print('🎮 Welcome to the Number Guessing Game!')
    print('=' * 50)

    secret_number = random.randint(min_num, max_num)
    attempts = 0

    print(f'🤔 I have selected a number between {min_num} and {max_num}.')
    print(f'💡 You have {max_attempts} attempts to guess it!')
    print('-' * 50)

    while attempts < max_attempts:
        try:
            guess = int(input(f'🎯 Attempt #{attempts + 1}: Enter your guess: '))
        except ValueError:
            print('❌ Invalid input! Please enter a number.')
            continue

        # چک کردن محدوده
        if guess < min_num or guess > max_num:
            print(f'⚠️ Please enter a number between {min_num} and {max_num}!')
            continue

        attempts += 1

        if guess < secret_number:
            print('📉 Too low! Try a higher number.')
        elif guess > secret_number:
            print('📈 Too high! Try a lower number.')
        else:
            print('\n' + '=' * 50)
            print(f'🎉 Congratulations! You guessed it in {attempts} attempts!')
            print(f'✅ The secret number was: {secret_number}')
            print('=' * 50)
            return True

    print('\n' + '=' * 50)
    print(f'😢 Game Over! You ran out of attempts.')
    print(f'🔍 The secret number was: {secret_number}')
    print('=' * 50)
    return False


# برنامه اصلی
print('🎮 NUMBER GUESSING GAME')
print('=' * 50)
print('Choose difficulty:')
print('1. Easy (1-20, 10 attempts)')
print('2. Medium (1-100, 10 attempts)')
print('3. Hard (1-1000, 5 attempts)')

difficulty = input('\nEnter your choice (1/2/3): ')

if difficulty == '1':
    min_num, max_num, max_attempts = 1, 20, 10
elif difficulty == '2':
    min_num, max_num, max_attempts = 1, 100, 10
elif difficulty == '3':
    min_num, max_num, max_attempts = 1, 1000, 5
else:
    print('❌ Invalid choice! Starting Medium...')
    min_num, max_num, max_attempts = 1, 100, 10

while True:
    play_game(min_num, max_num, max_attempts)
    play_again = input('\n🔄 Play again? (yes/no): ')
    if play_again.lower() != 'yes':
        print('👋 Thanks for playing!')
        break