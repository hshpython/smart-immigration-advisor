# 🌟 Smart Immigration Advisor

A Python-based application that helps users compare countries for immigration based on multiple factors.

---

## ✨ Features

- Compares 4 countries (Canada, Germany, Japan, Australia)
- Evaluates based on 7 factors:
  - Age
  - Education
  - Experience
  - Language difficulty
  - Culture fit
  - Security
  - **Live weather from API**
- **Live weather data from Open-Meteo API**
- Beautiful GUI built with Tkinter
- Automatic report generation

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Requests** (for API calls)
- **Tkinter** (GUI)
- **Open-Meteo API** (live weather data)
- **Git & GitHub**

---

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/hshpython/smart-immigration-advisor.git
```

2. Navigate to the project folder:

```bash
cd smart-immigration-advisor
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the terminal version:

```bash
python main.py
```

Or run the GUI version:

```bash
python gui_app.py
```

---

## 🎯 My Projects

### 1. 🌟 Smart Immigration Advisor - Advanced (Main Project)
A comprehensive GUI application that compares 4 countries for immigration.

**Features**:
- 3 tabs (Input, Results, History)
- Live weather from Open-Meteo API
- Comparison chart with matplotlib
- History saved in JSON
- Object-oriented design

**Technologies**: Python, Tkinter, Requests, Matplotlib, JSON, OOP

### 2. 🧮 Advanced Calculator
A full-featured calculator like Google Play apps.

**Features**:
- Scientific functions (sin, cos, tan, log, sqrt)
- Memory operations (M+, M-, MR, MC)
- Calculation history
- Unit converter (Temperature, Length, Weight)

**Technologies**: Python, Tkinter, JSON, Math

### 3. 🎮 Number Guessing Game
A fun interactive game where the player guesses a random number.

**Technologies**: Python, random module

### 4. 🧮 Simple Calculator
A command-line calculator supporting basic operations.

**Technologies**: Python, function dictionary

### 5. 📞 Phone Book Application
A CRUD application with full validation.

**Features**:
- Regex validation for name, phone, email
- JSON storage
- Full CRUD operations

**Technologies**: Python, JSON, Regex

## 📊 How It Works

The application calculates an immigration score for each country based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Immigration Score | 10% | Based on age, education, experience |
| Language | 20% | Difficulty of learning the language |
| Job Market | 20% | Python job opportunities |
| Culture | 20% | Cultural compatibility |
| Cost of Living | 10% | Affordability |
| Security | 10% | Safety and stability |
| Weather | 10% | Climate compatibility (live API) |

The country with the highest final score is recommended.

---

## 📸 Screenshot

![Screenshot](ScreenShot.png)

---

## 👤 Author

**Hossein Shahabi**
- GitHub: [@hshpython](https://github.com/hshpython)

---

## 📄 License

This project is open-source and available for learning purposes.
