# ==========================================
# Smart Immigration Advisor - OOP Version
# ==========================================

class Country:
    """Represents a country with immigration factors"""

    def __init__(self, name, language, language_difficulty, python_jobs,
                 culture_fit, living_cost, security, weather):
        self.name = name
        self.language = language
        self.language_difficulty = language_difficulty
        self.python_jobs = python_jobs
        self.culture_fit = culture_fit
        self.living_cost = living_cost
        self.security = security
        self.weather = weather
        self.immigration_score = 0
        self.final_score = 0

    def calculate_immigration_score(self, age, education, experience, english_level):
        """Calculate immigration score based on personal factors"""
        # Age score
        if age < 18:
            age_score = 0
        elif 18 <= age <= 30:
            age_score = 12
        elif 31 <= age <= 40:
            age_score = 8
        elif 41 <= age <= 60:
            age_score = 6
        else:
            age_score = 2

        # Experience score
        if experience >= 10:
            exp_score = 30
        elif 5 <= experience < 10:
            exp_score = 20
        elif 3 <= experience < 5:
            exp_score = 10
        else:
            exp_score = 2

        # Education score
        if education == 'phd':
            edu_score = 30
        elif education == 'master':
            edu_score = 20
        elif education == 'bachelor':
            edu_score = 10
        elif education == 'associate':
            edu_score = 5
        elif education == 'diploma':
            edu_score = 2
        else:
            edu_score = 2

        # Bonus score
        bonus = 0
        if self.name == 'canada' and age >= 30:
            bonus = 6
        elif self.name == 'germany' and (education == 'master' or education == 'phd'):
            bonus = 8
        elif self.name == 'australia' and english_level == 'Advanced':
            bonus = 5

        self.immigration_score = age_score + exp_score + edu_score + bonus
        return self.immigration_score

    def calculate_final_score(self):
        """Calculate final weighted score"""
        language_score = (10 - self.language_difficulty) * 2
        job_score = self.python_jobs * 2
        culture_score = self.culture_fit * 2
        cost_score = self.living_cost
        security_score = self.security
        weather_score = self.weather
        immigration_normalized = (self.immigration_score / 100) * 10

        self.final_score = round(
            language_score + job_score + culture_score +
            cost_score + security_score + weather_score +
            immigration_normalized, 1
        )
        return self.final_score

    def display(self):
        """Display country details"""
        print(f'\n🌍 {self.name.upper()}:')
        print(f'   🗣️  Language: {self.language} (Difficulty: {self.language_difficulty}/10)')
        print(f'   💼 Python Jobs: {self.python_jobs}/10')
        print(f'   🌏 Culture Fit: {self.culture_fit}/10')
        print(f'   🔒 Security: {self.security}/10')
        print(f'   ☀️  Weather: {self.weather}/10')
        print(f'   📊 Immigration Score: {self.immigration_score}')
        print(f'   ⭐ Final Score: {self.final_score}')

    def get_summary(self):
        """Return a one-line summary of the country"""
        return f"{self.name.upper()}: {self.final_score} points (Immigration: {self.immigration_score})"
# ==========================================
# Main Program
# ==========================================

print('=' * 50)
print('🌟 Smart Immigration Advisor (OOP Version)')
print('=' * 50)

name = input('Full Name: ')
age = int(input('Age: '))
education = input('Education (Diploma/Associate/Bachelor/Master/PhD): ').lower()
experience = int(input('Years of Experience: '))
english_level = input('English Level (Beginner/Intermediate/Advanced): ')

# Create country objects
countries = [
    Country('canada', 'English/French', 3, 9, 8, 7, 9, 4),
    Country('germany', 'German', 7, 8, 6, 6, 9, 5),
    Country('japan', 'Japanese', 9, 7, 5, 8, 10, 6),
    Country('australia', 'English', 2, 8, 9, 7, 9, 9)
]

print('\n' + '=' * 50)
print('📋 Country Details:')
print('=' * 50)

# Calculate scores for each country
for country in countries:
    country.calculate_immigration_score(age, education, experience, english_level)
    country.calculate_final_score()
    print(country.get_summary())
    country.display()

# Find best country
best_country = max(countries, key=lambda c: c.final_score)

print('\n' + '-' * 50)
print('📊 Final Results (out of 100):')
print('-' * 50)

for country in countries:
    print(f'🌍 {country.name.upper()}: {country.final_score} points')

print('\n' + '=' * 50)
print(f'🥇 Best Country: {best_country.name.upper()} with {best_country.final_score} points!')
print(f'🔥 {name}, {best_country.name.upper()} is your best option!')
print('=' * 50)

# Save report
with open('immigration_report_oop.txt', 'w', encoding='utf-8') as file:
    file.write('=' * 50 + '\n')
    file.write('Smart Immigration Advisor - OOP Report\n')
    file.write('=' * 50 + '\n')
    file.write(f'Name: {name}\n')
    file.write(f'Age: {age}\n')
    file.write(f'Education: {education}\n')
    file.write(f'Experience: {experience} years\n')
    file.write(f'English Level: {english_level}\n')
    file.write('-' * 50 + '\n')
    for country in countries:
        file.write(f'{country.name.upper()}: {country.final_score} points\n')
    file.write('-' * 50 + '\n')
    file.write(f'Best Country: {best_country.name.upper()}\n')
    file.write(f'Final Score: {best_country.final_score}\n')
    file.write('=' * 50 + '\n')






print('✅ Report saved to immigration_report_oop.txt')