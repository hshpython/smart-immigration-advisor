import requests


def calculate_weather_score(temperature):
    """Calculate weather score based on temperature"""
    if temperature is None:
        return 5  # امتیاز پیش‌فرض اگه دما موجود نبود
    elif 15 <= temperature <= 25:
        return 10  # دمای عالی
    elif 10 <= temperature < 15 or 25 < temperature <= 30:
        return 7  # دمای قابل قبول
    else:
        return 4  # دمای سخت

def get_current_weather(latitude, longitude):
        """Get current temperature from Open-Meteo API"""
        try:
            url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
            response = requests.get(url, timeout=5)
            data = response.json()
            return data['current_weather']['temperature']
        except Exception as e:
            return None




def calculate_age_score(age):
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
    if experience >= 10:
        return 30
    elif 5 <= experience < 10:
        return 20
    elif 3 <= experience < 5:
        return 10
    else:
        return 2


def calculate_education_score(education):
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
        return 0


def calculate_bonus(country, age, education, english_level):
    if country == 'canada' and age >= 30:
        return 6
    elif country == 'germany' and (education == 'master' or education == 'phd'):
        return 8
    elif country == 'australia' and english_level == 'Advanced':
        return 5
    return 0


class Country:
    """A class representing a country for immigration comparison"""

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

    def display_info(self):
        """Display country information"""
        print(f'🌍 {self.name.upper()}:')
        print(f'   🗣️  Language: {self.language} (Difficulty: {self.language_difficulty}/10)')
        print(f'   💼 Python Jobs: {self.python_jobs}/10')
        print(f'   🌏 Culture Fit: {self.culture_fit}/10')
        print(f'   🔒 Security: {self.security}/10')
        print(f'   ☀️  Weather: {self.weather}/10')
        print(f'   📊 Immigration Score: {self.immigration_score}')

    def get_summary(self):
        """Return a short summary of the country"""
        return f'{self.name.upper()}: {self.final_score} points (Language: {self.language})'

    def compare_with(self, other_country):
        """Compare this country with another country"""
        if self.final_score > other_country.final_score:
            return f'{self.name.upper()} is better than {other_country.name.upper()} by {round(self.final_score - other_country.final_score, 1)} points'
        elif self.final_score < other_country.final_score:
            return f'{other_country.name.upper()} is better than {self.name.upper()} by {round(other_country.final_score - self.final_score, 1)} points'
        else:
            return f'{self.name.upper()} and {other_country.name.upper()} are equal!'





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

# ساخت کشورها با کلاس
countries = [
    Country('canada', 'English/French', 3, 9, 8, 7, 9, 4),
    Country('germany', 'German', 7, 8, 6, 6, 9, 5),
    Country('japan', 'Japanese', 9, 7, 5, 8, 10, 6),
    Country('australia', 'English', 2, 8, 9, 7, 9, 9)
]

city_coordinates = {
    'canada': {'name': 'Toronto', 'lat': 43.6532, 'lon': -79.3832},
    'germany': {'name': 'Berlin', 'lat': 52.5200, 'lon': 13.4050},
    'japan': {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503},
    'australia': {'name': 'Sydney', 'lat': -33.8688, 'lon': 151.2093}
}

# محاسبه امتیازها
for country in countries:
    country.immigration_score = (
            calculate_age_score(age) +
            calculate_experience_score(experience) +
            calculate_education_score(education) +
            calculate_bonus(country.name, age, education, english_level)
    )

    # محاسبه امتیاز نهایی
    language_score = (10 - country.language_difficulty) * 2
    job_score = country.python_jobs * 2
    culture_score = country.culture_fit * 2
    cost_score = country.living_cost
    security_score = country.security
    coord = city_coordinates[country.name]
    temp = get_current_weather(coord['lat'], coord['lon'])
    weather_score = calculate_weather_score(temp)
    immigration_normalized = (country.immigration_score / 100) * 10

    total = (language_score + job_score + culture_score +
             cost_score + security_score + weather_score +
             immigration_normalized)
    country.final_score = round(total, 1)

# پیدا کردن بهترین کشور
best_country = max(countries, key=lambda c: c.final_score)

# نمایش اطلاعات
print('\n' + '=' * 50)
print('📋 Country Details:')
print('=' * 50)

for country in countries:
    country.display_info()
    print()

print('-' * 50)
print('📊 Final Results (out of 100):')
print('-' * 50)

for country in countries:
    print(f'🌍 {country.name.upper()}: {country.final_score} points')

print('\n' + '=' * 50)
print(f'🥇 Best Country: {best_country.name.upper()} with {best_country.final_score} points!')
print(f'🔥 {name}, {best_country.name.upper()} is your best option!')
print('=' * 50)



for country in countries:
    print(country.get_summary())

# مقایسه‌ی دو کشور برتر
sorted_countries = sorted(countries, key=lambda c: c.final_score, reverse=True)
print('\n📊 Comparison:')
print(sorted_countries[0].compare_with(sorted_countries[1]))


import requests

def get_current_weather(latitude, longitude):
    """Get current temperature from Open-Meteo API"""
    try:
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
        response = requests.get(url, timeout=5)
        data = response.json()
        return data['current_weather']['temperature']
    except Exception as e:
        return None


# مختصات شهرهای اصلی کشورها
city_coordinates = {
    'canada': {'name': 'Toronto', 'lat': 43.6532, 'lon': -79.3832},
    'germany': {'name': 'Berlin', 'lat': 52.5200, 'lon': 13.4050},
    'japan': {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503},
    'australia': {'name': 'Sydney', 'lat': -33.8688, 'lon': 151.2093}
}

print('\n' + '=' * 50)
print('🌡️  Current Weather in Main Cities:')
print('=' * 50)

for country, coord in city_coordinates.items():
    temp = get_current_weather(coord['lat'], coord['lon'])
    if temp is not None:
        print(f'🌍 {country.upper()} ({coord["name"]}): {temp}°C')
    else:
        print(f'🌍 {country.upper()}: Weather data unavailable')

