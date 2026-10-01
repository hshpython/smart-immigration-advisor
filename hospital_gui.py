import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = 'hospital.db'


def get_connection():
    return sqlite3.connect(DB_NAME)


def get_stats():
    """Get dashboard statistics"""
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

    return {
        'patients': patients,
        'doctors': doctors,
        'scheduled': scheduled,
        'completed': completed
    }


class HospitalApp:
    """Hospital Management System - GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title('🏥 Hospital Management System')
        self.root.geometry('1000x700')
        self.root.configure(bg='#f0f0f0')

        # ساخت UI
        self.create_widgets()

    def create_widgets(self):
        """Create all widgets"""
        # عنوان
        title = tk.Label(self.root, text='🏥 Hospital Management System',
                         font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=15)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # تب ۱: Dashboard
        self.dashboard_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.dashboard_tab, text='🏠 Dashboard')
        self.create_dashboard()

        # تب ۲: Patients
        self.patients_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.patients_tab, text='👥 Patients')
        self.create_patients_tab()

        # تب ۳: Doctors
        self.doctors_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.doctors_tab, text='👨‍⚕️ Doctors')
        self.create_doctors_tab()

        # تب ۴: Appointments
        self.appointments_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.appointments_tab, text='📅 Appointments')
        self.create_appointments_tab()

        # تب ۵: Reports
        self.reports_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.reports_tab, text='📊 Reports')
        self.create_reports_tab()

    def create_dashboard(self):
        """Create dashboard tab"""
        stats = get_stats()

        # فریم آمار
        stats_frame = tk.Frame(self.dashboard_tab, bg='#f0f0f0')
        stats_frame.pack(pady=30)

        # کارت‌های آمار
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

        # دکمه‌ی به‌روزرسانی
        refresh_btn = tk.Button(self.dashboard_tab, text='🔄 Refresh',
                                command=self.refresh_dashboard,
                                bg='#2ecc71', fg='white',
                                font=('Arial', 12, 'bold'),
                                padx=20, pady=8)
        refresh_btn.pack(pady=20)

        # اطلاعات سیستم
        info_frame = tk.LabelFrame(self.dashboard_tab, text='ℹ️ System Info',
                                   bg='#f0f0f0', font=('Arial', 11, 'bold'))
        info_frame.pack(pady=20, padx=20, fill='x')

        tk.Label(info_frame, text='Database: hospital.db', bg='#f0f0f0',
                 font=('Arial', 10)).pack(anchor='w', padx=10, pady=5)
        tk.Label(info_frame, text='System: Hospital Management v1.0', bg='#f0f0f0',
                 font=('Arial', 10)).pack(anchor='w', padx=10, pady=5)
        tk.Label(info_frame, text='Author: Hossein Shahabi', bg='#f0f0f0',
                 font=('Arial', 10)).pack(anchor='w', padx=10, pady=5)

    def refresh_dashboard(self):
        """Refresh dashboard stats"""
        for widget in self.dashboard_tab.winfo_children():
            widget.destroy()
        self.create_dashboard()
        messagebox.showinfo('Success', 'Dashboard refreshed!')

    def create_patients_tab(self):
        """Create patients tab"""
        tk.Label(self.patients_tab, text='👥 Patient Management',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)

        # فریم دکمه‌ها
        btn_frame = tk.Frame(self.patients_tab, bg='#f0f0f0')
        btn_frame.pack(pady=10)

        buttons = [
            ('➕ Add', '#2ecc71'),
            ('👁️ View All', '#3498db'),
            ('🔍 Search', '#f39c12'),
            ('✏️ Edit', '#9b59b6'),
            ('🗑️ Delete', '#e74c3c'),
        ]

        for text, color in buttons:
            btn = tk.Button(btn_frame, text=text, bg=color, fg='white',
                            font=('Arial', 11, 'bold'), padx=15, pady=8, width=12)
            btn.pack(side='left', padx=5)

        # جدول نمایش بیماران
        columns = ('ID', 'Name', 'Age', 'Gender', 'Phone', 'Blood')
        self.patients_tree = ttk.Treeview(self.patients_tab, columns=columns,
                                          show='headings', height=15)

        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=120)

        self.patients_tree.pack(pady=10, padx=20, fill='both', expand=True)

        # بارگذاری داده‌ها
        self.load_patients()

    def load_patients(self):
        """Load patients into treeview"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name, last_name, age, gender, phone, blood_type FROM patients')
        patients = cursor.fetchall()
        conn.close()

        # پاک کردن قبلی‌ها
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)

        # اضافه کردن جدیدها
        for p in patients:
            self.patients_tree.insert('', 'end', values=(
                p[0], f'{p[1]} {p[2]}', p[3], p[4], p[5], p[6]
            ))

    def create_doctors_tab(self):
        """Create doctors tab"""
        tk.Label(self.doctors_tab, text='👨‍⚕️ Doctor Management',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)

        btn_frame = tk.Frame(self.doctors_tab, bg='#f0f0f0')
        btn_frame.pack(pady=10)

        buttons = [
            ('➕ Add', '#2ecc71'),
            ('👁️ View All', '#3498db'),
            ('🔍 Search', '#f39c12'),
            ('✏️ Edit', '#9b59b6'),
            ('🗑️ Delete', '#e74c3c'),
        ]

        for text, color in buttons:
            btn = tk.Button(btn_frame, text=text, bg=color, fg='white',
                            font=('Arial', 11, 'bold'), padx=15, pady=8, width=12)
            btn.pack(side='left', padx=5)

        # جدول پزشکان
        columns = ('ID', 'Name', 'Specialty', 'Phone', 'Fee')
        self.doctors_tree = ttk.Treeview(self.doctors_tab, columns=columns,
                                         show='headings', height=15)

        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=150)

        self.doctors_tree.pack(pady=10, padx=20, fill='both', expand=True)

        self.load_doctors()

    def load_doctors(self):
        """Load doctors into treeview"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name, last_name, specialty, phone, consultation_fee FROM doctors')
        doctors = cursor.fetchall()
        conn.close()

        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)

        for d in doctors:
            self.doctors_tree.insert('', 'end', values=(
                d[0], f'{d[1]} {d[2]}', d[3], d[4], f'{d[5]:,.0f}'
            ))

    def create_appointments_tab(self):
        """Create appointments tab"""
        tk.Label(self.appointments_tab, text='📅 Appointment Management',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)

        btn_frame = tk.Frame(self.appointments_tab, bg='#f0f0f0')
        btn_frame.pack(pady=10)

        buttons = [
            ('➕ New', '#2ecc71'),
            ('👁️ View All', '#3498db'),
            ('📅 By Date', '#f39c12'),
            ('✏️ Update', '#9b59b6'),
            ('❌ Cancel', '#e74c3c'),
        ]

        for text, color in buttons:
            btn = tk.Button(btn_frame, text=text, bg=color, fg='white',
                            font=('Arial', 11, 'bold'), padx=15, pady=8, width=12)
            btn.pack(side='left', padx=5)

        # جدول نوبت‌ها
        columns = ('ID', 'Date', 'Time', 'Patient', 'Doctor', 'Status')
        self.appointments_tree = ttk.Treeview(self.appointments_tab, columns=columns,
                                              show='headings', height=15)

        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=140)

        self.appointments_tree.pack(pady=10, padx=20, fill='both', expand=True)

        self.load_appointments()

    def load_appointments(self):
        """Load appointments into treeview"""
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
            ORDER BY a.appointment_date DESC
        ''')
        appointments = cursor.fetchall()
        conn.close()

        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)

        for a in appointments:
            self.appointments_tree.insert('', 'end', values=(
                a[0], a[1], a[2], a[4], f'Dr. {a[5]}', a[3]
            ))

    def create_reports_tab(self):
        """Create reports tab"""
        tk.Label(self.reports_tab, text='📊 Reports & Analytics',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=20)

        tk.Label(self.reports_tab, text='Coming soon...',
                 font=('Arial', 12), bg='#f0f0f0', fg='gray').pack(pady=50)


if __name__ == '__main__':
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()