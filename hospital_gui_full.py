import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

DB_NAME = 'hospital.db'


# ==========================================
# Helper Functions
# ==========================================

def get_connection():
    return sqlite3.connect(DB_NAME)


def is_valid_name(name):
    pattern = r'^[A-Za-z\s\u0600-\u06FF]+$'
    return bool(re.match(pattern, name))


def is_valid_phone(phone):
    pattern = r'^09\d{9}$'
    return bool(re.match(pattern, phone))


def is_valid_national_id(nid):
    return nid.isdigit() and len(nid) == 10


def is_valid_email(email):
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM patients')
    patients = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM doctors')
    doctors = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'Scheduled'")
    scheduled = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'Completed'")
    completed = cursor.fetchone()[0]
    conn.close()
    return {'patients': patients, 'doctors': doctors,
            'scheduled': scheduled, 'completed': completed}


# ==========================================
# Main Application Class
# ==========================================

class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title('🏥 Hospital Management System')
        self.root.geometry('1100x750')
        self.root.configure(bg='#f0f0f0')
        self.create_widgets()

    # ==========================================
    # Main Layout
    # ==========================================

    def create_widgets(self):
        title = tk.Label(self.root, text='🏥 Hospital Management System',
                         font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=15)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.dashboard_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.dashboard_tab, text='🏠 Dashboard')
        self.create_dashboard()

        self.patients_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.patients_tab, text='👥 Patients')
        self.create_patients_tab()

        self.doctors_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.doctors_tab, text='👨‍⚕️ Doctors')
        self.create_doctors_tab()

        self.appointments_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.appointments_tab, text='📅 Appointments')
        self.create_appointments_tab()

    # ==========================================
    # Dashboard Tab
    # ==========================================

    def create_dashboard(self):
        stats = get_stats()

        stats_frame = tk.Frame(self.dashboard_tab, bg='#f0f0f0')
        stats_frame.pack(pady=30)

        cards = [
            ('👥 Patients', stats['patients'], '#3498db'),
            ('👨‍⚕️ Doctors', stats['doctors'], '#9b59b6'),
            ('📅 Scheduled', stats['scheduled'], '#f39c12'),
            ('✅ Completed', stats['completed'], '#2ecc71'),
        ]

        for i, (label, value, color) in enumerate(cards):
            card = tk.Frame(stats_frame, bg=color, width=180, height=120)
            card.grid(row=0, column=i, padx=10, pady=10)
            card.pack_propagate(False)
            tk.Label(card, text=label, bg=color, fg='white',
                     font=('Arial', 12, 'bold')).pack(pady=10)
            tk.Label(card, text=str(value), bg=color, fg='white',
                     font=('Arial', 28, 'bold')).pack()

        tk.Button(self.dashboard_tab, text='🔄 Refresh',
                  command=self.refresh_dashboard,
                  bg='#2ecc71', fg='white',
                  font=('Arial', 12, 'bold'),
                  padx=20, pady=8, cursor='hand2').pack(pady=20)

    def refresh_dashboard(self):
        for widget in self.dashboard_tab.winfo_children():
            widget.destroy()
        self.create_dashboard()

    # ==========================================
    # Patients Tab
    # ==========================================

    def create_patients_tab(self):
        tk.Label(self.patients_tab, text='👥 Patient Management',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)

        btn_frame = tk.Frame(self.patients_tab, bg='#f0f0f0')
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text='➕ Add', bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.add_patient_window, cursor='hand2').pack(side='left', padx=5)

        tk.Button(btn_frame, text='👁️ Refresh', bg='#3498db', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.load_patients, cursor='hand2').pack(side='left', padx=5)

        tk.Button(btn_frame, text='🗑️ Delete', bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.delete_patient, cursor='hand2').pack(side='left', padx=5)

        columns = ('ID', 'Name', 'Age', 'Gender', 'Phone', 'Blood')
        self.patients_tree = ttk.Treeview(self.patients_tab, columns=columns,
                                          show='headings', height=15)
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=140, anchor='center')
        self.patients_tree.pack(pady=10, padx=20, fill='both', expand=True)
        self.load_patients()

    def load_patients(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name, last_name, age, gender, phone, blood_type FROM patients ORDER BY id')
        patients = cursor.fetchall()
        conn.close()

        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)

        for index, p in enumerate(patients, 1):
            real_id = p[0]
            self.patients_tree.insert(
                '', 'end',
                values=(index, f'{p[1]} {p[2]}', p[3], p[4], p[5], p[6]),
                tags=(str(real_id),)
            )

    def add_patient_window(self):
        win = tk.Toplevel(self.root)
        win.title('➕ Add New Patient')
        win.geometry('550x700')
        win.configure(bg='#f0f0f0')
        win.resizable(False, False)

        tk.Label(win, text='➕ Add New Patient',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0',
                 fg='#2c3e50').pack(pady=10)

        form_frame = tk.Frame(win, bg='#f0f0f0')
        form_frame.pack(pady=10, padx=20)

        fields = {}
        labels = [
            ('National ID *', 'national_id', '10 digits'),
            ('First Name *', 'first_name', 'Letters only'),
            ('Last Name *', 'last_name', 'Letters only'),
            ('Age *', 'age', 'Number (1-119)'),
            ('Gender *', 'gender', 'Male or Female'),
            ('Phone *', 'phone', '09xxxxxxxxx'),
            ('Email (Optional)', 'email', 'user@domain.com'),
            ('Address (Optional)', 'address', 'Full address'),
            ('Blood Type *', 'blood_type', 'A+, A-, B+, B-, AB+, AB-, O+, O-'),
        ]

        for i, (label, key, hint) in enumerate(labels):
            tk.Label(form_frame, text=label, bg='#f0f0f0',
                     font=('Arial', 10, 'bold'), anchor='w').grid(
                row=i * 2, column=0, sticky='w', pady=(5, 0), padx=5)
            entry = tk.Entry(form_frame, width=30, font=('Arial', 10))
            entry.grid(row=i * 2 + 1, column=0, pady=(0, 5), padx=5)
            fields[key] = entry
            tk.Label(form_frame, text=f'💡 {hint}', bg='#f0f0f0',
                     font=('Arial', 8), fg='#7f8c8d', anchor='w').grid(
                row=i * 2 + 1, column=1, sticky='w', padx=5)

        def save():
            try:
                nid = fields['national_id'].get().strip()
                if not is_valid_national_id(nid):
                    messagebox.showerror('Error', '❌ National ID must be exactly 10 digits!')
                    return

                first = fields['first_name'].get().strip()
                if not is_valid_name(first):
                    messagebox.showerror('Error', '❌ First Name must contain only letters!')
                    return

                last = fields['last_name'].get().strip()
                if not is_valid_name(last):
                    messagebox.showerror('Error', '❌ Last Name must contain only letters!')
                    return

                age_str = fields['age'].get().strip()
                try:
                    age = int(age_str)
                except ValueError:
                    messagebox.showerror('Error', f'❌ Age must be a number!')
                    return
                if not (0 < age < 120):
                    messagebox.showerror('Error', '❌ Age must be between 1-119!')
                    return

                gender = fields['gender'].get().strip().capitalize()
                if gender not in ['Male', 'Female']:
                    messagebox.showerror('Error', '❌ Gender must be "Male" or "Female"!')
                    return

                phone = fields['phone'].get().strip()
                if not is_valid_phone(phone):
                    messagebox.showerror('Error', '❌ Phone must start with 09 (11 digits)!')
                    return

                email = fields['email'].get().strip()
                if email and not is_valid_email(email):
                    messagebox.showerror('Error', '❌ Invalid email format!')
                    return

                address = fields['address'].get().strip()

                blood = fields['blood_type'].get().strip().upper()
                if blood not in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']:
                    messagebox.showerror('Error', '❌ Invalid blood type! Use: A+, A-, B+, B-, AB+, AB-, O+, O-')
                    return

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO patients (national_id, first_name, last_name, age, gender, phone, email, address, blood_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (nid, first, last, age, gender, phone, email, address, blood))
                conn.commit()
                conn.close()

                messagebox.showinfo('Success', f'✅ Patient "{first} {last}" added!')
                win.destroy()
                self.load_patients()
                self.refresh_dashboard()

            except sqlite3.IntegrityError:
                messagebox.showerror('Error', '❌ National ID already exists!')
            except Exception as e:
                messagebox.showerror('Error', f'❌ Error: {e}')

        tk.Button(win, text='💾 Save', command=save, bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold'), padx=25, pady=8, cursor='hand2').pack(pady=15)

        tk.Button(win, text='❌ Cancel', command=win.destroy, bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold'), padx=25, pady=8, cursor='hand2').pack(pady=5)

        fields['national_id'].focus()

    def delete_patient(self):
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Please select a patient first!')
            return

        real_id = self.patients_tree.item(selected[0])['tags'][0]
        values = self.patients_tree.item(selected[0])['values']
        name = values[1]

        if messagebox.askyesno('Confirm', f'Delete "{name}"?'):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM patients WHERE id = ?', (real_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', f'✅ Patient "{name}" deleted!')
            self.load_patients()
            self.refresh_dashboard()

    # ==========================================
    # Doctors Tab
    # ==========================================

    def create_doctors_tab(self):
        tk.Label(self.doctors_tab, text='👨‍⚕️ Doctor Management',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)

        btn_frame = tk.Frame(self.doctors_tab, bg='#f0f0f0')
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text='➕ Add', bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.add_doctor_window, cursor='hand2').pack(side='left', padx=5)

        tk.Button(btn_frame, text='👁️ Refresh', bg='#3498db', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.load_doctors, cursor='hand2').pack(side='left', padx=5)

        tk.Button(btn_frame, text='🗑️ Delete', bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.delete_doctor, cursor='hand2').pack(side='left', padx=5)

        columns = ('ID', 'Name', 'Specialty', 'Phone', 'Fee')
        self.doctors_tree = ttk.Treeview(self.doctors_tab, columns=columns,
                                         show='headings', height=15)
        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=170, anchor='center')
        self.doctors_tree.pack(pady=10, padx=20, fill='both', expand=True)
        self.load_doctors()

    def load_doctors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name, last_name, specialty, phone, consultation_fee FROM doctors ORDER BY id')
        doctors = cursor.fetchall()
        conn.close()

        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)

        for index, d in enumerate(doctors, 1):
            real_id = d[0]
            first_name = d[1].replace('Dr.', '').replace('dr.', '').strip()
            full_name = f'Dr. {first_name} {d[2]}'

            self.doctors_tree.insert(
                '', 'end',
                values=(index, full_name, d[3], d[4], f'{d[5]:,.0f}'),
                tags=(str(real_id),)
            )

    def add_doctor_window(self):
        win = tk.Toplevel(self.root)
        win.title('➕ Add New Doctor')
        win.geometry('550x650')
        win.configure(bg='#f0f0f0')
        win.resizable(False, False)

        tk.Label(win, text='➕ Add New Doctor',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0',
                 fg='#2c3e50').pack(pady=10)

        form_frame = tk.Frame(win, bg='#f0f0f0')
        form_frame.pack(pady=10, padx=20)

        fields = {}
        labels = [
            ('National ID *', 'national_id', '10 digits'),
            ('First Name *', 'first_name', 'Without Dr.'),
            ('Last Name *', 'last_name', 'Letters only'),
            ('Phone *', 'phone', '09xxxxxxxxx'),
            ('Email (Optional)', 'email', 'user@domain.com'),
            ('Available Days *', 'available_days', 'e.g., Mon,Wed,Fri'),
            ('Consultation Fee *', 'fee', 'e.g., 500000'),
        ]

        for i, (label, key, hint) in enumerate(labels):
            tk.Label(form_frame, text=label, bg='#f0f0f0',
                     font=('Arial', 10, 'bold'), anchor='w').grid(
                row=i * 2, column=0, sticky='w', pady=(5, 0), padx=5)
            entry = tk.Entry(form_frame, width=30, font=('Arial', 10))
            entry.grid(row=i * 2 + 1, column=0, pady=(0, 5), padx=5)
            fields[key] = entry
            tk.Label(form_frame, text=f'💡 {hint}', bg='#f0f0f0',
                     font=('Arial', 8), fg='#7f8c8d', anchor='w').grid(
                row=i * 2 + 1, column=1, sticky='w', padx=5)

        tk.Label(form_frame, text='Specialty *', bg='#f0f0f0',
                 font=('Arial', 10, 'bold'), anchor='w').grid(
            row=len(labels) * 2, column=0, sticky='w', pady=(5, 0), padx=5)

        specialties = ['Cardiology', 'Pediatrics', 'Orthopedics', 'Neurology',
                       'Dermatology', 'Internal Medicine', 'Surgery', 'Radiology']
        specialty_var = tk.StringVar(value=specialties[0])
        specialty_combo = ttk.Combobox(form_frame, textvariable=specialty_var,
                                       values=specialties, width=28, state='readonly')
        specialty_combo.grid(row=len(labels) * 2 + 1, column=0, pady=(0, 5), padx=5)

        def save():
            try:
                nid = fields['national_id'].get().strip()
                if not is_valid_national_id(nid):
                    messagebox.showerror('Error', '❌ National ID must be 10 digits!')
                    return

                first = fields['first_name'].get().strip()
                last = fields['last_name'].get().strip()
                if not is_valid_name(first) or not is_valid_name(last):
                    messagebox.showerror('Error', '❌ Name must contain only letters!')
                    return

                phone = fields['phone'].get().strip()
                if not is_valid_phone(phone):
                    messagebox.showerror('Error', '❌ Phone must start with 09!')
                    return

                email = fields['email'].get().strip()
                if email and not is_valid_email(email):
                    messagebox.showerror('Error', '❌ Invalid email format!')
                    return

                days = fields['available_days'].get().strip()
                if not days:
                    messagebox.showerror('Error', '❌ Available days is empty!')
                    return

                try:
                    fee = float(fields['fee'].get().strip())
                    if fee < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror('Error', '❌ Fee must be a positive number!')
                    return

                specialty = specialty_var.get()

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO doctors (national_id, first_name, last_name, specialty, phone, email, available_days, consultation_fee)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (nid, first, last, specialty, phone, email, days, fee))
                conn.commit()
                conn.close()

                messagebox.showinfo('Success', f'✅ Doctor "Dr. {first} {last}" added!')
                win.destroy()
                self.load_doctors()
                self.refresh_dashboard()

            except sqlite3.IntegrityError:
                messagebox.showerror('Error', '❌ National ID already exists!')
            except Exception as e:
                messagebox.showerror('Error', f'❌ Error: {e}')

        tk.Button(win, text='💾 Save', command=save, bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold'), padx=25, pady=8, cursor='hand2').pack(pady=15)

        tk.Button(win, text='❌ Cancel', command=win.destroy, bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold'), padx=25, pady=8, cursor='hand2').pack(pady=5)

    def delete_doctor(self):
        selected = self.doctors_tree.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Please select a doctor first!')
            return

        real_id = self.doctors_tree.item(selected[0])['tags'][0]
        values = self.doctors_tree.item(selected[0])['values']
        name = values[1]

        if messagebox.askyesno('Confirm', f'Delete "{name}"?'):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM doctors WHERE id = ?', (real_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', f'✅ Doctor "{name}" deleted!')
            self.load_doctors()
            self.refresh_dashboard()

    # ==========================================
    # Appointments Tab
    # ==========================================

    def create_appointments_tab(self):
        tk.Label(self.appointments_tab, text='📅 Appointment Management',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)

        btn_frame = tk.Frame(self.appointments_tab, bg='#f0f0f0')
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text='➕ New', bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.add_appointment_window, cursor='hand2').pack(side='left', padx=5)

        tk.Button(btn_frame, text='👁️ Refresh', bg='#3498db', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.load_appointments, cursor='hand2').pack(side='left', padx=5)

        tk.Button(btn_frame, text='✏️ Update', bg='#f39c12', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.update_appointment_status, cursor='hand2').pack(side='left', padx=5)

        tk.Button(btn_frame, text='🗑️ Delete', bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold'), padx=15, pady=8, width=12,
                  command=self.delete_appointment, cursor='hand2').pack(side='left', padx=5)

        columns = ('ID', 'Date', 'Time', 'Patient', 'Doctor', 'Status')
        self.appointments_tree = ttk.Treeview(self.appointments_tab, columns=columns,
                                              show='headings', height=15)
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=150, anchor='center')
        self.appointments_tree.pack(pady=10, padx=20, fill='both', expand=True)
        self.load_appointments()

    def load_appointments(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                a.id, a.appointment_date, a.appointment_time, a.status,
                p.first_name || ' ' || p.last_name,
                d.first_name || ' ' || d.last_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        ''')
        appointments = cursor.fetchall()
        conn.close()

        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)

        for index, a in enumerate(appointments, 1):
            real_id = a[0]
            doctor_name = a[5].replace('Dr.', '').replace('dr.', '').strip()
            status_icon = '✅' if a[3] == 'Scheduled' else '✔️' if a[3] == 'Completed' else '❌'

            self.appointments_tree.insert(
                '', 'end',
                values=(index, a[1], a[2], a[4], f'Dr. {doctor_name}', f'{status_icon} {a[3]}'),
                tags=(str(real_id),)
            )

    def add_appointment_window(self):
        win = tk.Toplevel(self.root)
        win.title('➕ New Appointment')
        win.geometry('550x600')
        win.configure(bg='#f0f0f0')
        win.resizable(False, False)

        tk.Label(win, text='➕ New Appointment',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0',
                 fg='#2c3e50').pack(pady=10)

        form_frame = tk.Frame(win, bg='#f0f0f0')
        form_frame.pack(pady=10, padx=20)

        # Patient selection
        tk.Label(form_frame, text='Patient *', bg='#f0f0f0',
                 font=('Arial', 10, 'bold'), anchor='w').grid(
            row=0, column=0, sticky='w', pady=(5, 0), padx=5)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name, last_name FROM patients ORDER BY last_name')
        patients = cursor.fetchall()
        conn.close()

        if not patients:
            messagebox.showerror('Error', '❌ No patients in database!')
            win.destroy()
            return

        patient_options = [f'{p[0]} - {p[1]} {p[2]}' for p in patients]
        patient_var = tk.StringVar(value=patient_options[0])
        patient_combo = ttk.Combobox(form_frame, textvariable=patient_var,
                                     values=patient_options, width=33, state='readonly')
        patient_combo.grid(row=1, column=0, pady=(0, 10), padx=5)

        # Doctor selection
        tk.Label(form_frame, text='Doctor *', bg='#f0f0f0',
                 font=('Arial', 10, 'bold'), anchor='w').grid(
            row=2, column=0, sticky='w', pady=(5, 0), padx=5)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name, last_name, specialty FROM doctors ORDER BY last_name')
        doctors = cursor.fetchall()
        conn.close()

        if not doctors:
            messagebox.showerror('Error', '❌ No doctors in database!')
            win.destroy()
            return

        doctor_options = [f'{d[0]} - Dr. {d[1]} {d[2]} ({d[3]})' for d in doctors]
        doctor_var = tk.StringVar(value=doctor_options[0])
        doctor_combo = ttk.Combobox(form_frame, textvariable=doctor_var,
                                    values=doctor_options, width=33, state='readonly')
        doctor_combo.grid(row=3, column=0, pady=(0, 10), padx=5)

        # Date
        tk.Label(form_frame, text='Date * (YYYY-MM-DD)', bg='#f0f0f0',
                 font=('Arial', 10, 'bold'), anchor='w').grid(
            row=4, column=0, sticky='w', pady=(5, 0), padx=5)
        date_entry = tk.Entry(form_frame, width=30, font=('Arial', 10))
        date_entry.grid(row=5, column=0, pady=(0, 5), padx=5)
        date_entry.insert(0, '2026-10-15')
        tk.Label(form_frame, text='💡 Example: 2026-10-15', bg='#f0f0f0',
                 font=('Arial', 8), fg='#7f8c8d', anchor='w').grid(
            row=5, column=1, sticky='w', padx=5)

        # Time
        tk.Label(form_frame, text='Time * (HH:MM)', bg='#f0f0f0',
                 font=('Arial', 10, 'bold'), anchor='w').grid(
            row=6, column=0, sticky='w', pady=(5, 0), padx=5)
        time_entry = tk.Entry(form_frame, width=30, font=('Arial', 10))
        time_entry.grid(row=7, column=0, pady=(0, 5), padx=5)
        time_entry.insert(0, '10:30')
        tk.Label(form_frame, text='💡 Example: 10:30', bg='#f0f0f0',
                 font=('Arial', 8), fg='#7f8c8d', anchor='w').grid(
            row=7, column=1, sticky='w', padx=5)

        # Notes
        tk.Label(form_frame, text='Notes (Optional)', bg='#f0f0f0',
                 font=('Arial', 10, 'bold'), anchor='w').grid(
            row=8, column=0, sticky='w', pady=(5, 0), padx=5)
        notes_entry = tk.Entry(form_frame, width=30, font=('Arial', 10))
        notes_entry.grid(row=9, column=0, pady=(0, 5), padx=5)

        def save():
            try:
                patient_id = int(patient_var.get().split(' - ')[0])
                doctor_id = int(doctor_var.get().split(' - ')[0])

                date_str = date_entry.get().strip()
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                    messagebox.showerror('Error', '❌ Invalid date format! Use YYYY-MM-DD')
                    return

                time_str = time_entry.get().strip()
                if not re.match(r'^\d{2}:\d{2}$', time_str):
                    messagebox.showerror('Error', '❌ Invalid time format! Use HH:MM')
                    return

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*) FROM appointments 
                    WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ?
                    AND status = 'Scheduled'
                ''', (doctor_id, date_str, time_str))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror('Error', '❌ This time slot is already taken!')
                    conn.close()
                    return

                notes = notes_entry.get().strip()

                cursor.execute('''
                    INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
                    VALUES (?, ?, ?, ?, 'Scheduled', ?)
                ''', (patient_id, doctor_id, date_str, time_str, notes))
                conn.commit()
                conn.close()

                messagebox.showinfo('Success', f'✅ Appointment created for {date_str} at {time_str}!')
                win.destroy()
                self.load_appointments()
                self.refresh_dashboard()

            except Exception as e:
                messagebox.showerror('Error', f'❌ Error: {e}')

        tk.Button(win, text='💾 Save', command=save, bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold'), padx=25, pady=8, cursor='hand2').pack(pady=15)

        tk.Button(win, text='❌ Cancel', command=win.destroy, bg='#e74c3c', fg='white',
                  font=('Arial', 11, 'bold'), padx=25, pady=8, cursor='hand2').pack(pady=5)

    def update_appointment_status(self):
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Please select an appointment first!')
            return

        real_id = self.appointments_tree.item(selected[0])['tags'][0]
        values = self.appointments_tree.item(selected[0])['values']

        win = tk.Toplevel(self.root)
        win.title('✏️ Update Status')
        win.geometry('350x300')
        win.configure(bg='#f0f0f0')
        win.resizable(False, False)

        tk.Label(win, text=f'Appointment #{values[0]}',
                 font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=10)
        tk.Label(win, text=f'Patient: {values[3]}',
                 font=('Arial', 10), bg='#f0f0f0').pack()
        tk.Label(win, text=f'Current: {values[5]}',
                 font=('Arial', 10), bg='#f0f0f0').pack(pady=10)

        tk.Label(win, text='New Status:',
                 font=('Arial', 11, 'bold'), bg='#f0f0f0').pack(pady=5)

        status_var = tk.StringVar(value='Scheduled')
        for status in ['Scheduled', 'Completed', 'Cancelled']:
            tk.Radiobutton(win, text=status, variable=status_var,
                           value=status, bg='#f0f0f0',
                           font=('Arial', 10)).pack()

        def apply():
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE appointments SET status = ? WHERE id = ?',
                           (status_var.get(), real_id))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', f'✅ Status updated to "{status_var.get()}"')
            win.destroy()
            self.load_appointments()
            self.refresh_dashboard()

        tk.Button(win, text='💾 Apply', command=apply, bg='#2ecc71', fg='white',
                  font=('Arial', 11, 'bold'), padx=20, pady=8, cursor='hand2').pack(pady=15)

    def delete_appointment(self):
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Please select an appointment first!')
            return

        real_id = self.appointments_tree.item(selected[0])['tags'][0]
        values = self.appointments_tree.item(selected[0])['values']

        if messagebox.askyesno('Confirm',
                               f'Delete Appointment #{values[0]}?\n'
                               f'Patient: {values[3]}\n'
                               f'Date: {values[1]} at {values[2]}'):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM appointments WHERE id = ?', (real_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', '✅ Appointment deleted!')
            self.load_appointments()
            self.refresh_dashboard()


# ==========================================
# Run Application
# ==========================================

if __name__ == '__main__':
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()