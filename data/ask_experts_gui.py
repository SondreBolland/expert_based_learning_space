import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import utils.tooltip as tooltip

class ExpertGUI:
    def __init__(self, master, failed_ids, target_id, task_dict, callback):
        self.master = master
        self.failed_ids = list(failed_ids)
        self.target_id = target_id
        self.task_dict = task_dict
        self.callback = callback

        self.master.title("Expert Query")
        self.master.geometry("900x700")
        self.master.minsize(900, 700)
        #self.master.eval('tk::PlaceWindow . center')
        self.center(self.master)

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TLabel", background="#f8f9fa", font=("Helvetica", 14))
        style.configure("TButton", font=("Helvetica", 14))

        # Scrollable canvas setup
        canvas = tk.Canvas(self.master, background="#f8f9fa")
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.master.protocol('WM_DELETE_WINDOW', self.exit_button_function)

        # Now use scrollable_frame instead of container
        ttk.Label(scrollable_frame,
                text="Suppose that a student has failed the following problem(s):",
                font=("Helvetica", 18, "bold")).pack(anchor="w", pady=(0, 10))

        task_frame = ttk.Frame(scrollable_frame)
        task_frame.pack(fill="x")

        for idx, task_id in enumerate(self.failed_ids):
            self.add_task(task_frame, task_id, label=f"Problem {chr(97 + idx)})", row=0, col=idx, full_width=True)

        ttk.Label(scrollable_frame,
                text="Is it practically certain that this student will also fail:",
                font=("Helvetica", 16)).pack(pady=10)

        self.add_task(scrollable_frame, self.target_id, label=f"Problem {chr(97 + len(self.failed_ids))})", full_width=True)

        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=30)

        ttk.Button(button_frame, text="Yes", command=lambda: self.submit_answer(1), width=12).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="No", command=lambda: self.submit_answer(0), width=12).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Uncertain", command=lambda: self.submit_answer(None), width=12).grid(row=0, column=2, padx=10)

    def add_task(self, parent, task_id, label="", row=0, col=0, full_width=False):
        task = self.task_dict[task_id]

        frame = ttk.Frame(parent, padding=10, relief="ridge")
        if full_width:
            frame.pack(pady=5, fill="x", expand=True)
        else:
            frame.grid(row=row, column=col, padx=10, pady=5, sticky="n")

        # Header with label + tooltip
        header = ttk.Frame(frame)
        header.pack(fill="x")

        ttk.Label(header, text=label, font=("Helvetica", 16, "bold")).pack(side="left")

        if 'solution' in task:
            tip_icon = tk.Label(header, text="🛈", bg="#f8f9fa", font=("Helvetica", 16))
            tip_icon.pack(side="right")
            tooltip.ToolTip(tip_icon, task.get('solution', 'No solution available.'))

        # Task Text
        ttk.Label(frame, text=task['text'], wraplength=820, justify="left",
                  font=("Helvetica", 14)).pack(anchor="w", pady=(5, 3))

        # Code, if present
        if task['code']:
            code_box = scrolledtext.ScrolledText(
                frame, height=5, width=90, wrap="none",
                font=("Courier", 14), padx=5, pady=5
            )
            code_box.insert(tk.END, task['code'])
            code_box.config(state=tk.DISABLED)
            code_box.pack()

    def submit_answer(self, value):
        self.callback(value)
        self.master.destroy()
        
    def exit_button_function(self):   # function that will be called when user pressed no button
        self.master.destroy()
        exit()
        
    def center(self, window):
        """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        window.update_idletasks()
        width = window.winfo_width()
        frm_width = window.winfo_rootx() - window.winfo_x()
        win_width = width + 2 * frm_width
        height = window.winfo_height()
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = window.winfo_screenwidth() // 2 - win_width // 2
        y = window.winfo_screenheight() // 2 - win_height // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.deiconify()


# Example usage
def run_gui(failed_ids, target_id, task_dict):
    def on_answer(response):
        print(f"Expert answered: {response}")  # Replace with recording logic

    root = tk.Tk()
    app = ExpertGUI(root, failed_ids, target_id, task_dict, on_answer)
    root.mainloop()