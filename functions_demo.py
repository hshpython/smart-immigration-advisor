# ==========================================
# Smart Immigration Advisor - Refactored
# ==========================================

def calculate_age_score(age):
    """Calculate age score based on immigration rules"""
    if age < 18:
        return 0
    elif 18 <= age <= 30:
        return 12
    elif 31 <= age <= 40:
        return 8
    elif 41 <= age <= 60:
        return 6
    else:
        return 2


def calculate_experience_score(experience):
    """Calculate experience score"""
    if experience >= 10:
        return 30
    elif 5 <= experience < 10:
        return 20
    elif 3 <= experience < 5:
        return 10
    else:
        return 2


def calculate_education_score(education):
    """Calculate education score"""
    education = education.lower()
    if education == 'phd':
        return 30
    elif education == 'master':
        return 20
    elif education == 'bachelor':
        return 10
    elif education == 'associate':
        return 5
    elif education == 'diploma':
        return 2
    else:
        return 2


def calculate_bonus(country, age, education, english_level):
    """Calculate country-specific bonus points"""
    if country == 'canada' and age >= 30:
        return 6
    elif country == 'germany' and (education == 'master' or education == 'phd'):
        return 8
    elif country == 'australia' and english_level == 'Advanced':
        return 5
    return 0


# def calculate_immigration_score(country, age, education, experience, english_level):
#     """Calculate total immigration score for a country"""
#     age_score = calculate_age_score(age)
#     exp_score = calculate_experience_score(experience)
#     edu_score = calculate_education_score(education)
#     bonus = calculate_bonus(country, age, education, english_level)
#     return age_score + exp_score + edu_score + bonus


def calculate_final_score(country_data, immigration_score):
    """Calculate final weighted score"""
    language_score = (10 - country_data['language_difficulty']) * 2
    job_score = country_data['python_jobs'] * 2
    culture_score = country_data['culture_fit'] * 2
    cost_score = country_data['living_cost']
    security_score = country_data['security']
    weather_score = country_data['weather']
    immigration_normalized = (immigration_score / 100) * 10

    total = (language_score + job_score + culture_score +
             cost_score + security_score + weather_score +
             immigration_normalized)
    return round(total, 1)

def calculate_total_score(age, education, experience, english_level, country):
    """Calculate total immigration score"""
    # اینجا از توابع دیگه استفاده کن
    age_score = calculate_age_score(age)
    exp_score = calculate_experience_score(experience)
    edu_score = calculate_education_score(education)
    bonus = calculate_bonus(country, age, education, english_level)
    return age_score + exp_score + edu_score + bonus

def get_country_details(country, data, immigration_score):
    """Return formatted details for a country"""
    return {
        'name': country.upper(),
        'language': data['language'],
        'language_difficulty': data['language_difficulty'],
        'python_jobs': data['python_jobs'],
        'culture_fit': data['culture_fit'],
        'living_cost': data['living_cost'],
        'security': data['security'],
        'weather': data['weather'],
        'immigration_score': immigration_score
    }

def save_report(name, age, education, experience, english_level, final_scores, best_country):
    """Save full report to a text file"""
    with open('immigration_report.txt', 'w', encoding='utf-8') as file:
        file.write('=' * 50 + '\n')
        file.write('📋 Smart Immigration Advisor - Full Report\n')
        file.write('=' * 50 + '\n')
        file.write(f'👤 Name: {name}\n')
        file.write(f'📅 Age: {age}\n')
        file.write(f'🎓 Education: {education}\n')
        file.write(f'💼 Experience: {experience} years\n')
        file.write(f'🗣️  English Level: {english_level}\n')
        file.write('-' * 50 + '\n')
        file.write('📊 Final Scores:\n')
        for country, score in final_scores.items():
            file.write(f'   {country.upper()}: {score} points\n')
        file.write('-' * 50 + '\n')
        file.write(f'🥇 Best Country: {best_country.upper()}\n')
        file.write(f'⭐ Final Score: {final_scores[best_country]}\n')
        file.write('=' * 50 + '\n')
    print('✅ Report saved to immigration_report.txt')
# ==========================================
# Main Program
# ==========================================

print('=' * 50)
print('🌟 Smart Immigration Advisor')
print('=' * 50)

name = input('Full Name: ')
age = int(input('Age: '))
education = input('Education (Diploma/Associate/Bachelor/Master/PhD): ').lower()
experience = int(input('Years of Experience: '))
english_level = input('English Level (Beginner/Intermediate/Advanced): ')

countries_data = {
    'canada': {'language': 'English/French', 'language_difficulty': 3, 'python_jobs': 9, 'culture_fit': 8,
               'living_cost': 7, 'security': 9, 'weather': 4},
    'germany': {'language': 'German', 'language_difficulty': 7, 'python_jobs': 8, 'culture_fit': 6, 'living_cost': 6,
                'security': 9, 'weather': 5},
    'japan': {'language': 'Japanese', 'language_difficulty': 9, 'python_jobs': 7, 'culture_fit': 5, 'living_cost': 8,
              'security': 10, 'weather': 6},
    'australia': {'language': 'English', 'language_difficulty': 2, 'python_jobs': 8, 'culture_fit': 9, 'living_cost': 7,
                  'security': 9, 'weather': 9}
}

final_scores = {}

for country, data in countries_data.items():
    immigration_score = calculate_total_score(age, education, experience, english_level,country)
    final_score = calculate_final_score(data, immigration_score)
    final_scores[country] = final_score

print('\n' + '=' * 50)
print('📋 Country Details:')
print('=' * 50)

for country, data in countries_data.items():
    immigration_score = calculate_total_score(age, education, experience, english_level,country)
    details = get_country_details(country, data, immigration_score)

    print(f'\n🌍 {details["name"]}:')
    print(f'   🗣️  Language: {details["language"]} (Difficulty: {details["language_difficulty"]}/10)')
    print(f'   💼 Python Jobs: {details["python_jobs"]}/10')
    print(f'   🌏 Culture Fit: {details["culture_fit"]}/10')
    print(f'   🔒 Security: {details["security"]}/10')
    print(f'   ☀️  Weather: {details["weather"]}/10')
    print(f'   📊 Immigration Score: {details["immigration_score"]}')

best_country = max(final_scores, key=final_scores.get)

print('\n' + '-' * 50)
print('📊 Final Results (out of 100):')
print('-' * 50)

for country, score in final_scores.items():
    print(f'🌍 {country.upper()}: {score} points')

print('\n' + '=' * 50)
print(f'🥇 Best Country: {best_country.upper()} with {final_scores[best_country]} points!')
print(f'🔥 {name}, {best_country.upper()} is your best option!')
save_report(name, age, education, experience, english_level, final_scores, best_country)
print('=' * 50)







