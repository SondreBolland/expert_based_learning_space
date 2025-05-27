import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import utils.tooltip as tooltip

# Font sizes
button_font_size = 16
label_font_size = 14
prompt_font_size = 20
task_font_size = 20

class ExpertGUI:
    
    def __init__(self, master, failed_ids, target_id, task_dict, callback):
        self.master = master
        self.failed_ids = list(failed_ids)
        self.target_id = target_id
        self.task_dict = task_dict
        self.callback = callback

        self.master.title("Expert Query")
        # Dynamically set window height based on number of tasks
        total_tasks = len(self.failed_ids) + 1  # target task
        base_height = 650
        extra_height_per_task = 180
        window_height = base_height + total_tasks * extra_height_per_task

        # Cap the window height to avoid absurdly tall windows (you still have scrolling)
        max_height = 1200
        self.master.geometry(f"1100x{min(window_height, max_height)}")
        self.master.minsize(800, 600)
        self.center(self.master)

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TLabel", background="#f8f9fa", font=("Helvetica", label_font_size))
        style.configure("TButton", font=("Helvetica", button_font_size))

        # Scrollable canvas setup
        canvas = tk.Canvas(self.master, background="#f8f9fa")
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        # Mousewheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/macOS
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux


        # Create a frame to hold content
        scrollable_frame = ttk.Frame(canvas)

        # Make scrollable_frame stretch with canvas width
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def resize_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", resize_canvas)
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
                font=("Helvetica", prompt_font_size)).pack(pady=10)

        task_frame = ttk.Frame(scrollable_frame)
        task_frame.pack(fill="x")

        for idx, task_id in enumerate(self.failed_ids):
            self.add_task(task_frame, task_id, label=f"Problem {chr(97 + idx)})", row=0, col=idx, full_width=True)

        ttk.Label(scrollable_frame,
                text="Is it practically certain that this student will also fail:",
                font=("Helvetica", prompt_font_size)).pack(pady=10)

        self.add_task(scrollable_frame, self.target_id, label=f"Problem {chr(97 + len(self.failed_ids))})", full_width=True)

        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=30, fill="x", expand=True)

        for i, (text, val) in enumerate([("Yes", 1), ("No", 0), ("Uncertain", None)]):
            btn = ttk.Button(button_frame, text=text, command=lambda v=val: self.submit_answer(v))
            btn.grid(row=0, column=i, padx=10, sticky="ew")

        # Ensure buttons expand
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
            
        ttk.Label(scrollable_frame,
                text="Hover 🛈 to see a sample solution of the task",
                font=("Helvetica", prompt_font_size)).pack(pady=10)

    def add_task(self, parent, task_id, label="", row=0, col=0, full_width=False):
        task = self.task_dict[task_id]

        frame = ttk.Frame(parent, padding=10, relief="ridge")
        frame.pack(pady=5, fill="x", expand=True)  # Always use pack()

        # Header with label + tooltip
        header = ttk.Frame(frame)
        header.pack(fill="x")

        ttk.Label(header, text=label, font=("Helvetica", task_font_size, "bold")).pack(side="left")

        if 'solution' in task:
            tip_icon = tk.Label(header, text="🛈", bg="#f8f9fa", font=("Helvetica", task_font_size))
            tip_icon.pack(side="right")
            tooltip.ToolTip(tip_icon, task.get('solution', 'No solution available.'))

        # Task Text
        ttk.Label(frame, text=task['text'], wraplength=900, justify="left",
          font=("Helvetica", task_font_size)).pack(anchor="w", fill="x", expand=True, pady=(5, 3))


        if task['code']:
            # Count number of lines in the code (at least 1)
            code_lines = task['code'].count('\n') + 1
            max_lines = 12
            height = min(code_lines, max_lines)

            code_box = scrolledtext.ScrolledText(
                frame,
                height=height,
                width=65,
                wrap="none",
                font=("Courier", task_font_size),
                padx=5,
                pady=5
            )
            code_box.insert(tk.END, task['code'])
            code_box.config(state=tk.DISABLED)
            code_box.pack()

            
        try:
            option_text = ""
            for option in task['options']:
                option_text += f"- {option}\n"
            ttk.Label(frame, text=option_text, wraplength=900, justify="left", font=("Helvetica", task_font_size)).pack(anchor="w", fill="x", expand=True, pady=(5, 3))
        except:
            pass

    def submit_answer(self, value):
        self.callback(value)
        
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


def run_gui(failed_ids, target_id, task_dict):
    response = {'value': None}  # Use mutable dict to allow inner function to modify it

    def on_answer(value):
        response['value'] = value  # Store the expert’s answer
        root.quit()  # Stop the mainloop to allow return

    root = tk.Tk()
    app = ExpertGUI(root, failed_ids, target_id, task_dict, on_answer)
    root.mainloop()
    root.destroy()  # Cleanly close the GUI window

    return response['value']  # Will be 1 (yes), 0 (no), or -1 (I don’t know)
