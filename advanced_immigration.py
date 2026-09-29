import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================
# 1. Classes
# ==========================================

class Country:
    """Country class with all data"""

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

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'language': self.language,
            'language_difficulty': self.language_difficulty,
            'python_jobs': self.python_jobs,
            'culture_fit': self.culture_fit,
            'living_cost': self.living_cost,
            'security': self.security,
            'weather': self.weather,
            'immigration_score': self.immigration_score,
            'final_score': self.final_score
        }


class User:
    """User class"""

    def __init__(self, name, age, education, experience, english_level):
        self.name = name
        self.age = age
        self.education = education
        self.experience = experience
        self.english_level = english_level

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'education': self.education,
            'experience': self.experience,
            'english_level': self.english_level
        }


# ==========================================
# 2. Helper Functions
# ==========================================

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


def calculate_weather_score(temperature):
    if temperature is None:
        return 5
    elif 15 <= temperature <= 25:
        return 10
    elif 10 <= temperature < 15 or 25 < temperature <= 30:
        return 7
    else:
        return 4


def get_current_weather(latitude, longitude):
    try:
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
        response = requests.get(url, timeout=5)
        data = response.json()
        return data['current_weather']['temperature']
    except Exception:
        return None


# ==========================================
# 3. GUI Application
# ==========================================

class ImmigrationApp:
    """Main GUI application"""

    def __init__(self, root):
        self.root = root
        self.root.title('🌟 Smart Immigration Advisor - Advanced')
        self.root.geometry('900x750')
        self.root.configure(bg='#f0f0f0')

        # داده‌های کشورها
        self.countries_data = {
            'canada': {'language': 'English/French', 'language_difficulty': 3, 'python_jobs': 9,
                       'culture_fit': 8, 'living_cost': 7, 'security': 9, 'weather': 4,
                       'coords': (43.6532, -79.3832), 'city': 'Toronto'},
            'germany': {'language': 'German', 'language_difficulty': 7, 'python_jobs': 8,
                        'culture_fit': 6, 'living_cost': 6, 'security': 9, 'weather': 5,
                        'coords': (52.5200, 13.4050), 'city': 'Berlin'},
            'japan': {'language': 'Japanese', 'language_difficulty': 9, 'python_jobs': 7,
                      'culture_fit': 5, 'living_cost': 8, 'security': 10, 'weather': 6,
                      'coords': (35.6762, 139.6503), 'city': 'Tokyo'},
            'australia': {'language': 'English', 'language_difficulty': 2, 'python_jobs': 8,
                          'culture_fit': 9, 'living_cost': 7, 'security': 9, 'weather': 9,
                          'coords': (-33.8688, 151.2093), 'city': 'Sydney'}
        }

        # تاریخچه
        self.history = []
        self.load_history()

        # ساخت UI
        self.create_widgets()

    def create_widgets(self):
        """Create all GUI widgets"""
        # عنوان
        title = tk.Label(self.root, text='🌟 Smart Immigration Advisor - Advanced',
                         font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=15)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # تب ۱: ورودی
        self.input_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.input_tab, text='📝 Input')
        self.create_input_tab()

        # تب ۲: نتایج
        self.results_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.results_tab, text='📊 Results')
        self.create_results_tab()

        # تب ۳: تاریخچه
        self.history_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.history_tab, text='📜 History')
        self.create_history_tab()

    def create_input_tab(self):
        """Create input tab"""
        frame = tk.Frame(self.input_tab, bg='#f0f0f0')
        frame.pack(pady=20)

        labels = ['Full Name:', 'Age:', 'Education (Diploma/Associate/Bachelor/Master/PhD):',
                  'Years of Experience:', 'English Level (Beginner/Intermediate/Advanced):']

        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame, text=label, bg='#f0f0f0', font=('Arial', 11),
                     anchor='w').grid(row=i, column=0, sticky='w', pady=8, padx=5)
            entry = tk.Entry(frame, width=35, font=('Arial', 11))
            entry.grid(row=i, column=1, pady=8, padx=5)
            self.entries[label] = entry

        # دکمه محاسبه
        calculate_btn = tk.Button(frame, text='🔍 Calculate', command=self.calculate,
                                  bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                  padx=25, pady=10, cursor='hand2')
        calculate_btn.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def create_results_tab(self):
        """Create results tab"""
        self.results_text = tk.Text(self.results_tab, height=15, width=80,
                                    font=('Arial', 11), bg='white', relief='solid', bd=2)
        self.results_text.pack(pady=10, padx=10, fill='both', expand=True)

        # فریم برای نمودار
        self.chart_frame = tk.Frame(self.results_tab, bg='#f0f0f0')
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=10)

    def create_history_tab(self):
        """Create history tab"""
        self.history_text = tk.Text(self.history_tab, height=20, width=80,
                                    font=('Arial', 11), bg='white', relief='solid', bd=2)
        self.history_text.pack(pady=10, padx=10, fill='both', expand=True)

        # دکمه‌ها
        btn_frame = tk.Frame(self.history_tab, bg='#f0f0f0')
        btn_frame.pack(pady=5)

        clear_btn = tk.Button(btn_frame, text='🗑️ Clear History', command=self.clear_history,
                              bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                              padx=15, pady=5)
        clear_btn.pack(side='left', padx=5)

        refresh_btn = tk.Button(btn_frame, text='🔄 Refresh', command=self.refresh_history,
                                bg='#2ecc71', fg='white', font=('Arial', 10, 'bold'),
                                padx=15, pady=5)
        refresh_btn.pack(side='left', padx=5)

        self.refresh_history()

    def calculate(self):
        """Calculate immigration scores"""
        try:
            # دریافت اطلاعات
            name = self.entries['Full Name:'].get()
            age = int(self.entries['Age:'].get())
            education = self.entries['Education (Diploma/Associate/Bachelor/Master/PhD):'].get().lower()
            experience = int(self.entries['Years of Experience:'].get())
            english_level = self.entries['English Level (Beginner/Intermediate/Advanced):'].get()

            if not name:
                messagebox.showerror('Error', 'Please enter your name!')
                return

            # ساخت کشورها
            countries = []
            for country_name, data in self.countries_data.items():
                country = Country(
                    country_name,
                    data['language'],
                    data['language_difficulty'],
                    data['python_jobs'],
                    data['culture_fit'],
                    data['living_cost'],
                    data['security'],
                    data['weather']
                )

                # محاسبه امتیاز
                country.immigration_score = (
                        calculate_age_score(age) +
                        calculate_experience_score(experience) +
                        calculate_education_score(education) +
                        calculate_bonus(country_name, age, education, english_level)
                )

                # دریافت دما
                lat, lon = data['coords']
                temp = get_current_weather(lat, lon)
                weather_score = calculate_weather_score(temp)

                # محاسبه امتیاز نهایی
                language_score = (10 - country.language_difficulty) * 2
                job_score = country.python_jobs * 2
                culture_score = country.culture_fit * 2
                cost_score = country.living_cost
                security_score = country.security
                immigration_normalized = (country.immigration_score / 100) * 10

                total = (language_score + job_score + culture_score +
                         cost_score + security_score + weather_score +
                         immigration_normalized)
                country.final_score = round(total, 1)

                countries.append(country)

            # پیدا کردن بهترین
            best_country = max(countries, key=lambda c: c.final_score)

            # نمایش نتایج
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f'📋 Results for {name}\n')
            self.results_text.insert(tk.END, '=' * 60 + '\n\n')

            for country in countries:
                self.results_text.insert(tk.END, f'🌍 {country.name.upper()}: {country.final_score} points\n')

            self.results_text.insert(tk.END, '\n' + '=' * 60 + '\n')
            self.results_text.insert(tk.END, f'🥇 Best Country: {best_country.name.upper()}\n')
            self.results_text.insert(tk.END, f'⭐ Score: {best_country.final_score}\n')

            # رسم نمودار
            self.draw_chart(countries)

            # ذخیره در تاریخچه
            self.save_to_history(name, age, education, experience, english_level,
                                 [c.to_dict() for c in countries], best_country.name)

            # سوییچ به تب نتایج
            self.notebook.select(1)

        except ValueError:
            messagebox.showerror('Error', 'Please enter valid numbers for age and experience!')
        except Exception as e:
            messagebox.showerror('Error', f'Error: {e}')

    def draw_chart(self, countries):
        """Draw comparison chart"""
        # پاک کردن نمودار قبلی
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # ساخت نمودار
        fig, ax = plt.subplots(figsize=(8, 3), dpi=80)

        names = [c.name.upper() for c in countries]
        scores = [c.final_score for c in countries]
        colors = ['#e74c3c', '#f39c12', '#9b59b6', '#3498db']

        bars = ax.bar(names, scores, color=colors)
        ax.set_ylabel('Score')
        ax.set_title('Country Comparison')
        ax.set_ylim(0, 100)

        # اضافه کردن اعداد روی میله‌ها
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height}', ha='center', va='bottom')

        # نمایش توی Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def save_to_history(self, name, age, education, experience, english_level, countries, best):
        """Save calculation to history"""
        entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'name': name,
            'age': age,
            'education': education,
            'experience': experience,
            'english_level': english_level,
            'best_country': best,
            'countries': countries
        }

        self.history.append(entry)

        try:
            with open('history.json', 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Error saving history: {e}')

        self.refresh_history()

    def load_history(self):
        """Load history from file"""
        try:
            with open('history.json', 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def refresh_history(self):
        """Refresh history display"""
        self.history_text.delete(1.0, tk.END)

        if not self.history:
            self.history_text.insert(tk.END, '📭 No history yet.\n')
            return

        for i, entry in enumerate(reversed(self.history), 1):
            self.history_text.insert(tk.END, f'#{i} - {entry["timestamp"]}\n')
            self.history_text.insert(tk.END, f'   👤 {entry["name"]} (Age: {entry["age"]})\n')
            self.history_text.insert(tk.END, f'   🎓 {entry["education"]} | 💼 {entry["experience"]} years\n')
            self.history_text.insert(tk.END, f'   🥇 Best: {entry["best_country"].upper()}\n')
            self.history_text.insert(tk.END, '-' * 60 + '\n')

    def clear_history(self):
        """Clear history"""
        if messagebox.askyesno('Confirm', 'Clear all history?'):
            self.history = []
            try:
                with open('history.json', 'w', encoding='utf-8') as f:
                    json.dump([], f)
            except:
                pass
            self.refresh_history()


# ==========================================
# 4. Run Application
# ==========================================

if __name__ == '__main__':
    root = tk.Tk()
    app = ImmigrationApp(root)
    root.mainloop()