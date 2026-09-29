import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
from datetime import datetime


class AdvancedCalculator:
    """Advanced Calculator Application"""

    def __init__(self, root):
        self.root = root
        self.root.title('🧮 Advanced Calculator')
        self.root.geometry('500x700')
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        # متغیرها
        self.current_input = ''
        self.memory = 0
        self.history = []
        self.load_history()

        # ساخت UI
        self.create_widgets()

    def create_widgets(self):
        """Create all widgets"""
        # عنوان
        title = tk.Label(self.root, text='🧮 Advanced Calculator',
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=10)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # تب ۱: ماشین‌حساب
        self.calc_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.calc_tab, text='🧮 Calculator')
        self.create_calc_tab()

        # تب ۲: تاریخچه
        self.history_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.history_tab, text='📜 History')
        self.create_history_tab()

        # تب ۳: تبدیل واحد
        self.convert_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.convert_tab, text='🔄 Converter')
        self.create_convert_tab()

    def create_calc_tab(self):
        """Create calculator tab"""
        # نمایشگر
        display_frame = tk.Frame(self.calc_tab, bg='#f0f0f0')
        display_frame.pack(pady=10, padx=10, fill='x')

        self.display = tk.Entry(display_frame, font=('Arial', 24, 'bold'),
                                justify='right', bg='white', fg='#2c3e50',
                                relief='solid', bd=2)
        self.display.pack(fill='x', ipady=15)

        # نشانگر حافظه
        self.memory_label = tk.Label(display_frame, text='', font=('Arial', 10),
                                     bg='#f0f0f0', fg='#e74c3c')
        self.memory_label.pack(anchor='w')

        # دکمه‌های حافظه
        memory_frame = tk.Frame(self.calc_tab, bg='#f0f0f0')
        memory_frame.pack(pady=5)

        memory_buttons = [
            ('MC', lambda: self.memory_clear(), '#e74c3c'),
            ('MR', lambda: self.memory_recall(), '#e74c3c'),
            ('M+', lambda: self.memory_add(), '#e74c3c'),
            ('M-', lambda: self.memory_subtract(), '#e74c3c'),
        ]

        for text, command, color in memory_buttons:
            btn = tk.Button(memory_frame, text=text, command=command,
                            bg=color, fg='white', font=('Arial', 10, 'bold'),
                            width=6, height=2)
            btn.pack(side='left', padx=2)

        # دکمه‌های علمی
        scientific_frame = tk.Frame(self.calc_tab, bg='#f0f0f0')
        scientific_frame.pack(pady=5)

        scientific_buttons = [
            ('sin', lambda: self.scientific('sin'), '#3498db'),
            ('cos', lambda: self.scientific('cos'), '#3498db'),
            ('tan', lambda: self.scientific('tan'), '#3498db'),
            ('log', lambda: self.scientific('log'), '#3498db'),
            ('√', lambda: self.scientific('sqrt'), '#3498db'),
            ('x²', lambda: self.scientific('square'), '#3498db'),
        ]

        for text, command, color in scientific_buttons:
            btn = tk.Button(scientific_frame, text=text, command=command,
                            bg=color, fg='white', font=('Arial', 10, 'bold'),
                            width=6, height=2)
            btn.pack(side='left', padx=2)

        # دکمه‌های اصلی
        buttons_frame = tk.Frame(self.calc_tab, bg='#f0f0f0')
        buttons_frame.pack(pady=10)

        buttons = [
            ['C', 'CE', '⌫', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '='],
            ['%', '(', ')', 'x^y'],
        ]

        for row in buttons:
            row_frame = tk.Frame(buttons_frame, bg='#f0f0f0')
            row_frame.pack()

            for btn_text in row:
                if btn_text == '=':
                    color = '#2ecc71'
                elif btn_text in ['C', 'CE', '⌫']:
                    color = '#e74c3c'
                elif btn_text in ['/', '*', '-', '+', '%', '(', ')', 'x^y']:
                    color = '#f39c12'
                elif btn_text == '+/-':
                    color = '#9b59b6'
                else:
                    color = '#34495e'

                btn = tk.Button(row_frame, text=btn_text, width=6, height=2,
                                bg=color, fg='white', font=('Arial', 14, 'bold'),
                                command=lambda t=btn_text: self.button_click(t))
                btn.pack(side='left', padx=2, pady=2)

    def create_history_tab(self):
        """Create history tab"""
        self.history_text = tk.Text(self.history_tab, height=20, width=50,
                                    font=('Arial', 11), bg='white', relief='solid', bd=2)
        self.history_text.pack(pady=10, padx=10, fill='both', expand=True)

        # دکمه‌ها
        btn_frame = tk.Frame(self.history_tab, bg='#f0f0f0')
        btn_frame.pack(pady=5)

        clear_btn = tk.Button(btn_frame, text='🗑️ Clear', command=self.clear_history,
                              bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                              padx=15, pady=5)
        clear_btn.pack(side='left', padx=5)

        refresh_btn = tk.Button(btn_frame, text='🔄 Refresh', command=self.refresh_history,
                                bg='#2ecc71', fg='white', font=('Arial', 10, 'bold'),
                                padx=15, pady=5)
        refresh_btn.pack(side='left', padx=5)

        self.refresh_history()

    def create_convert_tab(self):
        """Create unit converter tab"""
        tk.Label(self.convert_tab, text='🔄 Unit Converter',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)

        # انتخاب نوع تبدیل
        self.convert_type = ttk.Combobox(self.convert_tab,
                                         values=['Temperature', 'Length', 'Weight'],
                                         font=('Arial', 11), state='readonly')
        self.convert_type.pack(pady=10)
        self.convert_type.bind('<<ComboboxSelected>>', self.update_converter)

        # فریم تبدیل
        self.convert_frame = tk.Frame(self.convert_tab, bg='#f0f0f0')
        self.convert_frame.pack(pady=10)

        # مقدار ورودی
        tk.Label(self.convert_frame, text='From:', bg='#f0f0f0',
                 font=('Arial', 11)).grid(row=0, column=0, pady=5)

        self.convert_input = tk.Entry(self.convert_frame, font=('Arial', 11), width=15)
        self.convert_input.grid(row=0, column=1, pady=5, padx=5)

        self.convert_from = ttk.Combobox(self.convert_frame, font=('Arial', 11),
                                         state='readonly', width=10)
        self.convert_from.grid(row=0, column=2, pady=5, padx=5)

        # مقدار خروجی
        tk.Label(self.convert_frame, text='To:', bg='#f0f0f0',
                 font=('Arial', 11)).grid(row=1, column=0, pady=5)

        self.convert_output = tk.Entry(self.convert_frame, font=('Arial', 11),
                                       width=15, state='readonly')
        self.convert_output.grid(row=1, column=1, pady=5, padx=5)

        self.convert_to = ttk.Combobox(self.convert_frame, font=('Arial', 11),
                                       state='readonly', width=10)
        self.convert_to.grid(row=1, column=2, pady=5, padx=5)

        # دکمه تبدیل
        convert_btn = tk.Button(self.convert_tab, text='🔄 Convert',
                                command=self.do_convert,
                                bg='#3498db', fg='white',
                                font=('Arial', 12, 'bold'),
                                padx=20, pady=8)
        convert_btn.pack(pady=20)

        # راه‌اندازی اولیه
        self.convert_type.current(0)
        self.update_converter()

    def update_converter(self, event=None):
        """Update converter options based on type"""
        convert_type = self.convert_type.get()

        if convert_type == 'Temperature':
            units = ['Celsius', 'Fahrenheit', 'Kelvin']
        elif convert_type == 'Length':
            units = ['Meter', 'Kilometer', 'Centimeter', 'Mile', 'Foot', 'Inch']
        elif convert_type == 'Weight':
            units = ['Kilogram', 'Gram', 'Pound', 'Ounce']
        else:
            units = []

        self.convert_from['values'] = units
        self.convert_to['values'] = units

        if units:
            self.convert_from.current(0)
            self.convert_to.current(1 if len(units) > 1 else 0)

    def do_convert(self):
        """Perform conversion"""
        try:
            value = float(self.convert_input.get())
            from_unit = self.convert_from.get()
            to_unit = self.convert_to.get()
            convert_type = self.convert_type.get()

            if convert_type == 'Temperature':
                result = self.convert_temperature(value, from_unit, to_unit)
            elif convert_type == 'Length':
                result = self.convert_length(value, from_unit, to_unit)
            elif convert_type == 'Weight':
                result = self.convert_weight(value, from_unit, to_unit)
            else:
                return

            self.convert_output.config(state='normal')
            self.convert_output.delete(0, tk.END)
            self.convert_output.insert(0, f'{result:.4f}')
            self.convert_output.config(state='readonly')

        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid number!')

    def convert_temperature(self, value, from_unit, to_unit):
        """Convert temperature"""
        # تبدیل به سلسیوس
        if from_unit == 'Celsius':
            celsius = value
        elif from_unit == 'Fahrenheit':
            celsius = (value - 32) * 5 / 9
        elif from_unit == 'Kelvin':
            celsius = value - 273.15

        # تبدیل از سلسیوس
        if to_unit == 'Celsius':
            return celsius
        elif to_unit == 'Fahrenheit':
            return celsius * 9 / 5 + 32
        elif to_unit == 'Kelvin':
            return celsius + 273.15

    def convert_length(self, value, from_unit, to_unit):
        """Convert length"""
        # تبدیل به متر
        to_meter = {
            'Meter': 1, 'Kilometer': 1000, 'Centimeter': 0.01,
            'Mile': 1609.34, 'Foot': 0.3048, 'Inch': 0.0254
        }
        meters = value * to_meter[from_unit]
        return meters / to_meter[to_unit]

    def convert_weight(self, value, from_unit, to_unit):
        """Convert weight"""
        # تبدیل به کیلوگرم
        to_kg = {
            'Kilogram': 1, 'Gram': 0.001, 'Pound': 0.453592, 'Ounce': 0.0283495
        }
        kg = value * to_kg[from_unit]
        return kg / to_kg[to_unit]

    def button_click(self, value):
        """Handle button click"""
        if value == 'C':
            self.current_input = ''
            self.display.delete(0, tk.END)
        elif value == 'CE':
            self.display.delete(0, tk.END)
            self.current_input = ''
        elif value == '⌫':
            self.current_input = self.current_input[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_input)
        elif value == '=':
            self.calculate()
        elif value == '+/-':
            if self.current_input and self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_input)
        elif value == 'x^y':
            self.current_input += '**'
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_input)
        else:
            self.current_input += value
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_input)

    def calculate(self):
        """Perform calculation"""
        try:
            # جایگزینی علامت‌ها
            expression = self.current_input.replace('^', '**')

            # محاسبه
            result = eval(expression)

            # نمایش نتیجه
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))

            # ذخیره در تاریخچه
            self.add_to_history(f'{self.current_input} = {result}')

            self.current_input = str(result)

        except ZeroDivisionError:
            messagebox.showerror('Error', 'Division by zero!')
        except Exception as e:
            messagebox.showerror('Error', f'Invalid expression: {e}')

    def scientific(self, operation):
        """Handle scientific operations"""
        try:
            value = float(self.display.get() or 0)

            if operation == 'sin':
                result = math.sin(math.radians(value))
            elif operation == 'cos':
                result = math.cos(math.radians(value))
            elif operation == 'tan':
                result = math.tan(math.radians(value))
            elif operation == 'log':
                result = math.log10(value)
            elif operation == 'sqrt':
                result = math.sqrt(value)
            elif operation == 'square':
                result = value ** 2
            else:
                return

            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.current_input = str(result)

            self.add_to_history(f'{operation}({value}) = {result}')

        except Exception as e:
            messagebox.showerror('Error', f'Error: {e}')

    # حافظه
    def memory_clear(self):
        self.memory = 0
        self.memory_label.config(text='')
        messagebox.showinfo('Memory', 'Memory cleared!')

    def memory_recall(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, str(self.memory))
        self.current_input = str(self.memory)

    def memory_add(self):
        try:
            self.memory += float(self.display.get() or 0)
            self.memory_label.config(text=f'M: {self.memory}')
        except ValueError:
            pass

    def memory_subtract(self):
        try:
            self.memory -= float(self.display.get() or 0)
            self.memory_label.config(text=f'M: {self.memory}')
        except ValueError:
            pass

    # تاریخچه
    def add_to_history(self, entry):
        """Add entry to history"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.history.append(f'[{timestamp}] {entry}')

        try:
            with open('calculator_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except:
            pass

        self.refresh_history()

    def load_history(self):
        """Load history"""
        try:
            with open('calculator_history.json', 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def refresh_history(self):
        """Refresh history display"""
        if hasattr(self, 'history_text'):
            self.history_text.delete(1.0, tk.END)

            if not self.history:
                self.history_text.insert(tk.END, '📭 No history yet.\n')
                return

            for entry in reversed(self.history):
                self.history_text.insert(tk.END, f'{entry}\n')

    def clear_history(self):
        """Clear history"""
        if messagebox.askyesno('Confirm', 'Clear all history?'):
            self.history = []
            try:
                with open('calculator_history.json', 'w', encoding='utf-8') as f:
                    json.dump([], f)
            except:
                pass
            self.refresh_history()


# ==========================================
# Run Application
# ==========================================

if __name__ == '__main__':
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()