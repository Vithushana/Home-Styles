import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
import threading
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ModernPythonUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python Analytics Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Color scheme
        self.colors = {
            'bg': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#3b82f6',
            'text': '#ffffff',
            'text_secondary': '#9ca3af',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444'
        }
        
        # Data storage
        self.data = {
            'projects': [],
            'tasks': [],
            'analytics': {'lines': 0, 'files': 0, 'commits': 0}
        }
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=(10, 0))
        
        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=self.colors['secondary'], 
                       foreground=self.colors['text'], padding=[12, 8])
        style.map('TNotebook.Tab', background=[('selected', self.colors['accent'])])
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_projects_tab()
        self.create_analytics_tab()
        self.create_tools_tab()
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg'], height=60)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, text="🐍 Python Analytics Dashboard", 
                              font=('Arial', 20, 'bold'), 
                              fg=self.colors['accent'], bg=self.colors['bg'])
        title_label.pack(side='left', pady=15)
        
        # Status indicators
        status_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        status_frame.pack(side='right', pady=15)
        
        self.status_label = tk.Label(status_frame, text="● Online", 
                                   fg=self.colors['success'], bg=self.colors['bg'])
        self.status_label.pack(side='right', padx=10)
        
        time_label = tk.Label(status_frame, text=datetime.now().strftime("%H:%M:%S"), 
                             fg=self.colors['text_secondary'], bg=self.colors['bg'])
        time_label.pack(side='right', padx=10)
        
        # Update time every second
        def update_time():
            time_label.config(text=datetime.now().strftime("%H:%M:%S"))
            self.root.after(1000, update_time)
        update_time()
        
    def create_dashboard_tab(self):
        dashboard_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Stats cards
        stats_frame = tk.Frame(dashboard_frame, bg=self.colors['bg'])
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        stats = [
            ("Lines of Code", self.data['analytics']['lines'], self.colors['accent']),
            ("Python Files", self.data['analytics']['files'], self.colors['success']),
            ("Git Commits", self.data['analytics']['commits'], self.colors['warning']),
            ("Active Projects", len(self.data['projects']), self.colors['error'])
        ]
        
        for i, (label, value, color) in enumerate(stats):
            self.create_stat_card(stats_frame, label, value, color, i)
            
        # Recent activity
        activity_frame = tk.LabelFrame(dashboard_frame, text="Recent Activity", 
                                     bg=self.colors['secondary'], fg=self.colors['text'],
                                     font=('Arial', 12, 'bold'))
        activity_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.activity_text = tk.Text(activity_frame, bg=self.colors['bg'], 
                                   fg=self.colors['text'], height=10, 
                                   font=('Consolas', 10))
        scrollbar = tk.Scrollbar(activity_frame, orient='vertical', command=self.activity_text.yview)
        self.activity_text.configure(yscrollcommand=scrollbar.set)
        self.activity_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        self.log_activity("Dashboard initialized")
        
    def create_stat_card(self, parent, label, value, color, index):
        card_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='raised', bd=1)
        card_frame.grid(row=0, column=index, padx=5, pady=5, sticky='ew')
        parent.grid_columnconfigure(index, weight=1)
        
        value_label = tk.Label(card_frame, text=str(value), font=('Arial', 24, 'bold'),
                              fg=color, bg=self.colors['secondary'])
        value_label.pack(pady=(10, 0))
        
        label_label = tk.Label(card_frame, text=label, font=('Arial', 10),
                              fg=self.colors['text_secondary'], bg=self.colors['secondary'])
        label_label.pack(pady=(0, 10))
        
    def create_projects_tab(self):
        projects_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(projects_frame, text="Projects")
        
        # Project controls
        controls_frame = tk.Frame(projects_frame, bg=self.colors['bg'])
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(controls_frame, text="➕ New Project", 
                 command=self.add_project, bg=self.colors['accent'], fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', padx=20).pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="📁 Import", 
                 command=self.import_project, bg=self.colors['success'], fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', padx=20).pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="🗑️ Delete", 
                 command=self.delete_project, bg=self.colors['error'], fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', padx=20).pack(side='left', padx=5)
        
        # Projects list
        list_frame = tk.Frame(projects_frame, bg=self.colors['bg'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for projects
        columns = ('Name', 'Type', 'Status', 'Last Modified')
        self.projects_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.projects_tree.heading(col, text=col)
            self.projects_tree.column(col, width=200)
            
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.projects_tree.yview)
        self.projects_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        tree_scroll.pack(side='right', fill='y')
        
        self.refresh_projects_list()
        
    def create_analytics_tab(self):
        analytics_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(analytics_frame, text="Analytics")
        
        # Chart frame
        chart_frame = tk.Frame(analytics_frame, bg=self.colors['bg'])
        chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 6))
        self.fig.patch.set_facecolor(self.colors['bg'])
        
        # Configure subplots
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor(self.colors['secondary'])
            ax.tick_params(colors=self.colors['text'])
            ax.spines['bottom'].set_color(self.colors['text'])
            ax.spines['top'].set_color(self.colors['text'])
            ax.spines['left'].set_color(self.colors['text'])
            ax.spines['right'].set_color(self.colors['text'])
        
        # Embed matplotlib in tkinter
        self.canvas = FigureCanvasTkinter(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Control buttons
        btn_frame = tk.Frame(analytics_frame, bg=self.colors['bg'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="📊 Generate Report", 
                 command=self.generate_analytics, bg=self.colors['accent'], fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', padx=20).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🔄 Refresh Data", 
                 command=self.refresh_analytics, bg=self.colors['success'], fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', padx=20).pack(side='left', padx=5)
        
        self.generate_sample_charts()
        
    def create_tools_tab(self):
        tools_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tools_frame, text="Tools")
        
        # Code formatter
        formatter_frame = tk.LabelFrame(tools_frame, text="Code Formatter", 
                                      bg=self.colors['secondary'], fg=self.colors['text'],
                                      font=('Arial', 12, 'bold'))
        formatter_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Text editor
        self.code_text = tk.Text(formatter_frame, bg=self.colors['bg'], 
                               fg=self.colors['text'], font=('Consolas', 11),
                               wrap='word')
        code_scroll = tk.Scrollbar(formatter_frame, orient='vertical', command=self.code_text.yview)
        self.code_text.configure(yscrollcommand=code_scroll.set)
        
        self.code_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        code_scroll.pack(side='right', fill='y')
        
        # Tool buttons
        tools_btn_frame = tk.Frame(tools_frame, bg=self.colors['bg'])
        tools_btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(tools_btn_frame, text="🔧 Format Code", 
                 command=self.format_code, bg=self.colors['accent'], fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(tools_btn_frame, text="📋 Clear", 
                 command=lambda: self.code_text.delete(1.0, tk.END), 
                 bg=self.colors['warning'], fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', padx=15).pack(side='left', padx=5)
        
        tk.Button(tools_btn_frame, text="💾 Save", 
                 command=self.save_code, bg=self.colors['success'], fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', padx=15).pack(side='left', padx=5)
        
        # Add sample code
        sample_code = """# Sample Python Code
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Generate fibonacci sequence
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
"""
        self.code_text.insert(1.0, sample_code)
        
    def add_project(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Project")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 400, self.root.winfo_rooty() + 200))
        
        # Form fields
        tk.Label(dialog, text="Project Name:", bg=self.colors['bg'], 
                fg=self.colors['text']).pack(pady=5)
        name_entry = tk.Entry(dialog, font=('Arial', 11), width=30)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Project Type:", bg=self.colors['bg'], 
                fg=self.colors['text']).pack(pady=5)
        type_var = tk.StringVar(value="Web App")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, 
                                 values=["Web App", "Desktop App", "Data Science", "AI/ML", "API"])
        type_combo.pack(pady=5)
        
        tk.Label(dialog, text="Description:", bg=self.colors['bg'], 
                fg=self.colors['text']).pack(pady=5)
        desc_text = tk.Text(dialog, height=4, width=40, font=('Arial', 10))
        desc_text.pack(pady=5)
        
        def save_project():
            project = {
                'name': name_entry.get(),
                'type': type_var.get(),
                'description': desc_text.get(1.0, tk.END).strip(),
                'status': 'Active',
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if project['name']:
                self.data['projects'].append(project)
                self.save_data()
                self.refresh_projects_list()
                self.log_activity(f"Created new project: {project['name']}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Project name is required!")
        
        tk.Button(dialog, text="Create Project", command=save_project,
                 bg=self.colors['accent'], fg='white', font=('Arial', 10, 'bold'),
                 relief='flat', padx=20).pack(pady=20)
        
        name_entry.focus()
        
    def import_project(self):
        folder = filedialog.askdirectory(title="Select Project Folder")
        if folder:
            project_name = os.path.basename(folder)
            project = {
                'name': project_name,
                'type': 'Imported',
                'description': f'Imported from {folder}',
                'status': 'Active',
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'path': folder
            }
            self.data['projects'].append(project)
            self.save_data()
            self.refresh_projects_list()
            self.log_activity(f"Imported project: {project_name}")
            
    def delete_project(self):
        selection = self.projects_tree.selection()
        if selection:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this project?"):
                item = self.projects_tree.item(selection[0])
                project_name = item['values'][0]
                self.data['projects'] = [p for p in self.data['projects'] if p['name'] != project_name]
                self.save_data()
                self.refresh_projects_list()
                self.log_activity(f"Deleted project: {project_name}")
        else:
            messagebox.showwarning("No Selection", "Please select a project to delete.")
            
    def refresh_projects_list(self):
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
            
        for project in self.data['projects']:
            self.projects_tree.insert('', 'end', values=(
                project['name'], 
                project['type'], 
                project['status'], 
                project['created']
            ))
            
    def generate_sample_charts(self):
        # Sample data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        commits = [12, 19, 15, 28, 22, 31]
        languages = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
        usage = [45, 25, 15, 10, 5]
        
        # Commits chart
        self.ax1.clear()
        self.ax1.bar(months, commits, color=self.colors['accent'], alpha=0.7)
        self.ax1.set_title('Monthly Commits', color=self.colors['text'], fontsize=14)
        self.ax1.set_ylabel('Commits', color=self.colors['text'])
        
        # Language usage pie chart
        self.ax2.clear()
        colors = [self.colors['accent'], self.colors['success'], self.colors['warning'], 
                 self.colors['error'], self.colors['text_secondary']]
        self.ax2.pie(usage, labels=languages, colors=colors, autopct='%1.1f%%', startangle=90)
        self.ax2.set_title('Language Usage', color=self.colors['text'], fontsize=14)
        
        self.canvas.draw()
        
    def generate_analytics(self):
        # Simulate analytics generation
        def generate():
            self.log_activity("Generating analytics report...")
            time.sleep(2)  # Simulate processing time
            
            # Update stats with random data
            self.data['analytics']['lines'] = random.randint(1000, 5000)
            self.data['analytics']['files'] = random.randint(50, 200)
            self.data['analytics']['commits'] = random.randint(100, 500)
            
            self.log_activity("Analytics report generated successfully!")
            
            # Refresh dashboard
            self.root.after(0, self.refresh_dashboard)
            
        threading.Thread(target=generate, daemon=True).start()
        
    def refresh_analytics(self):
        self.generate_sample_charts()
        self.log_activity("Analytics data refreshed")
        
    def refresh_dashboard(self):
        # This would refresh the dashboard stats
        self.log_activity("Dashboard refreshed")
        
    def format_code(self):
        code = self.code_text.get(1.0, tk.END)
        # Simple formatting (in real app, you'd use autopep8 or black)
        formatted = code.replace('\t', '    ')  # Replace tabs with 4 spaces
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(1.0, formatted)
        self.log_activity("Code formatted")
        
    def save_code(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.code_text.get(1.0, tk.END))
            self.log_activity(f"Code saved to {os.path.basename(file_path)}")
            
    def log_activity(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.activity_text.insert(tk.END, log_entry)
        self.activity_text.see(tk.END)
        
    def save_data(self):
        try:
            with open('dashboard_data.json', 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            self.log_activity(f"Error saving data: {str(e)}")
            
    def load_data(self):
        try:
            if os.path.exists('dashboard_data.json'):
                with open('dashboard_data.json', 'r') as f:
                    self.data = json.load(f)
        except Exception as e:
            self.log_activity(f"Error loading data: {str(e)}")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernPythonUI()
    app.run()