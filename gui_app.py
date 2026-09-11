import tkinter as tk
from tkinter import messagebox

def calculate_immigration():
    """Calculate immigration score"""
    try:
        name = entry_name.get()
        age = int(entry_age.get())
        education = entry_education.get().lower()
        experience = int(entry_experience.get())
        english_level = entry_english.get()

        if not name:
            messagebox.showerror('Error', 'Please enter your name!')
            return

        countries_data = {
            'canada': {'language': 'English/French', 'language_difficulty': 3, 'python_jobs': 9, 'culture_fit': 8, 'living_cost': 7, 'security': 9, 'weather': 4, 'immigration_score': 0},
            'germany': {'language': 'German', 'language_difficulty': 7, 'python_jobs': 8, 'culture_fit': 6, 'living_cost': 6, 'security': 9, 'weather': 5, 'immigration_score': 0},
            'japan': {'language': 'Japanese', 'language_difficulty': 9, 'python_jobs': 7, 'culture_fit': 5, 'living_cost': 8, 'security': 10, 'weather': 6, 'immigration_score': 0},
            'australia': {'language': 'English', 'language_difficulty': 2, 'python_jobs': 8, 'culture_fit': 9, 'living_cost': 7, 'security': 9, 'weather': 9, 'immigration_score': 0}
        }

        for country in countries_data:
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

            if experience >= 10:
                exp_score = 30
            elif 5 <= experience < 10:
                exp_score = 20
            elif 3 <= experience < 5:
                exp_score = 10
            else:
                exp_score = 2

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

            bonus = 0
            if country == 'canada' and age >= 30:
                bonus = 6
            elif country == 'germany' and (education == 'master' or education == 'phd'):
                bonus = 8
            elif country == 'australia' and english_level == 'Advanced':
                bonus = 5

            immigration_score = age_score + exp_score + edu_score + bonus
            countries_data[country]['immigration_score'] = immigration_score

        final_scores = {}
        for country, data in countries_data.items():
            language_score = (10 - data['language_difficulty']) * 2
            job_score = data['python_jobs'] * 2
            culture_score = data['culture_fit'] * 2
            cost_score = data['living_cost']
            security_score = data['security']
            weather_score = data['weather']
            immigration_normalized = (data['immigration_score'] / 100) * 10

            total = (language_score + job_score + culture_score +
                     cost_score + security_score + weather_score +
                     immigration_normalized)
            final_scores[country] = round(total, 1)

        best_country = max(final_scores, key=final_scores.get)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f'Results for {name}:\n')
        result_text.insert(tk.END, '=' * 40 + '\n\n')

        for country, score in final_scores.items():
            result_text.insert(tk.END, f'{country.upper()}: {score} points\n')

        result_text.insert(tk.END, '\n' + '=' * 40 + '\n')
        result_text.insert(tk.END, f'Best Country: {best_country.upper()}\n')
        result_text.insert(tk.END, f'Final Score: {final_scores[best_country]}\n')

        with open('immigration_results.txt', 'w', encoding='utf-8') as file:
            file.write(f'Name: {name}\n')
            file.write(f'Age: {age}\n')
            file.write(f'Best Country: {best_country.upper()}\n')
            file.write(f'Score: {final_scores[best_country]}\n')

    except ValueError:
        messagebox.showerror('Error', 'Please enter age and experience as numbers!')
    except Exception as e:
        messagebox.showerror('Error', f'Something went wrong: {e}')


# --- Main Window ---
window = tk.Tk()
window.title('Smart Immigration Advisor')
window.geometry('600x700')
window.configure(bg='#f0f0f0')

# Title
title_label = tk.Label(window, text='Smart Immigration Advisor',
                        font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
title_label.pack(pady=15)

# Input Frame
input_frame = tk.Frame(window, bg='#f0f0f0')
input_frame.pack(pady=10)

# Name
tk.Label(input_frame, text='Full Name:', bg='#f0f0f0', font=('Arial', 11)).grid(row=0, column=0, sticky='w', pady=5)
entry_name = tk.Entry(input_frame, width=30, font=('Arial', 11))
entry_name.grid(row=0, column=1, pady=5)

# Age
tk.Label(input_frame, text='Age:', bg='#f0f0f0', font=('Arial', 11)).grid(row=1, column=0, sticky='w', pady=5)
entry_age = tk.Entry(input_frame, width=30, font=('Arial', 11))
entry_age.grid(row=1, column=1, pady=5)

# Education
tk.Label(input_frame, text='Education (phd/master/bachelor/associate):', bg='#f0f0f0', font=('Arial', 11)).grid(row=2, column=0, sticky='w', pady=5)
entry_education = tk.Entry(input_frame, width=30, font=('Arial', 11))
entry_education.grid(row=2, column=1, pady=5)

# Experience
tk.Label(input_frame, text='Years of Experience:', bg='#f0f0f0', font=('Arial', 11)).grid(row=3, column=0, sticky='w', pady=5)
entry_experience = tk.Entry(input_frame, width=30, font=('Arial', 11))
entry_experience.grid(row=3, column=1, pady=5)

# English Level
tk.Label(input_frame, text='English Level (Beginner/Intermediate/Advanced):', bg='#f0f0f0', font=('Arial', 11)).grid(row=4, column=0, sticky='w', pady=5)
entry_english = tk.Entry(input_frame, width=30, font=('Arial', 11))
entry_english.grid(row=4, column=1, pady=5)

# Calculate Button
calculate_btn = tk.Button(window, text='Calculate', command=calculate_immigration,
                          bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                          padx=20, pady=8, cursor='hand2')
calculate_btn.pack(pady=15)

# Results
result_text = tk.Text(window, height=15, width=60, font=('Arial', 11),
                       bg='#ffffff', fg='#2c3e50', relief='solid', bd=2)
result_text.pack(pady=10, padx=20)

window.mainloop()