import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime


class Task:
    def __init__(self, description, due_date=None):
        self.description = description
        self.completed = False
        self.due_date = due_date

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "◻"
        if self.due_date:
            due_date = self.due_date.strftime('%d-%m-%Y')
            return f"{status} {self.description} (Due: {due_date})"
        else:
            return f"{status} {self.description}"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, due_date=None):
        task = Task(description, due_date)
        self.tasks.append(task)

    def complete_task(self, task_index):
        if task_index < len(self.tasks):
            task = self.tasks[task_index]
            task.mark_completed()
        else:
            messagebox.showerror("Error", "Invalid task index!")

    def remove_task(self, task_index):
        if task_index < len(self.tasks):
            del self.tasks[task_index]
        else:
            messagebox.showerror("Error", "Invalid task index!")

    def get_task_list(self):
        return self.tasks

    def save_tasks(self, filename):
        with open(filename, "w") as file:
            for task in self.tasks:
                file.write(f"{task.description}\n")
                file.write(f"{task.completed}\n")
                if task.due_date:
                    file.write(f"{task.due_date.strftime('%d-%m-%Y')}\n")
                else:
                    file.write("\n")

    def load_tasks(self, filename):
        self.tasks = []
        with open(filename, "r") as file:
            lines = file.readlines()
            description = None
            completed = False
            due_date = None
            for line in lines:
                line = line.strip()
                if not line:
                    if description is not None:
                        task = Task(description, due_date)
                        task.completed = completed
                        self.tasks.append(task)
                        description = None
                        completed = False
                        due_date = None
                elif description is None:
                    description = line
                elif line == "True":
                    completed = True
                elif line == "False":
                    completed = False
                else:
                    due_date = datetime.strptime(line, '%d-%m-%Y').date()


class TaskManagerApp:
    def __init__(self):
        self.task_manager = TaskManager()
        self.filename = "tasks.txt"

        self.window = tk.Tk()
        self.window.title("Планировщик задач")
        self.window.geometry("400x500")

        self.task_listbox = tk.Listbox(self.window, selectmode=tk.SINGLE, font=("Arial", 12))
        self.task_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.add_button = tk.Button(self.window, text="Добавить задачу", command=self.add_task, font=("Arial", 12))
        self.add_button.pack(pady=5)

        self.complete_button = tk.Button(self.window, text="Отметить как выполненную", command=self.complete_task, font=("Arial", 12))
        self.complete_button.pack(pady=5)

        self.remove_button = tk.Button(self.window, text="Удалить задачу", command=self.remove_task, font=("Arial", 12))
        self.remove_button.pack(pady=5)

        self.load_tasks()
        self.populate_task_list()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def populate_task_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_manager.get_task_list()
        for task in tasks:
            self.task_listbox.insert(tk.END, str(task))

    def add_task(self):
        description = simpledialog.askstring("Добавить задачу", "Введите описание задачи:", parent=self.window)
        if description:
            due_date_str = simpledialog.askstring("Добавить задачу", "Введите дату выполнения (ДД-ММ-ГГГГ) [Задачи с датами не сохраняются!]:", parent=self.window)
            due_date = None
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, '%d-%m-%Y').date()
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат даты. Задача будет добавлена без указания даты выполнения.")
            self.task_manager.add_task(description, due_date)
            self.populate_task_list()
            self.save_tasks()

    def complete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            self.task_manager.complete_task(task_index)
            self.populate_task_list()
            self.save_tasks()
        else:
            messagebox.showerror("Ошибка", "Задача не выбрана.")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            self.task_manager.remove_task(task_index)
            self.populate_task_list()
            self.save_tasks()
        else:
            messagebox.showerror("Ошибка", "Задача не выбрана.")

    def save_tasks(self):
        self.task_manager.save_tasks(self.filename)

    def load_tasks(self):
        self.task_manager.load_tasks(self.filename)

    def run(self):
        self.window.mainloop()

    def on_close(self):
        self.save_tasks()
        self.window.destroy()



from task_manager_app import TaskManagerApp

def run_app():
    app = TaskManagerApp()
    app.run()

if __name__ == "__main__":
    run_app()