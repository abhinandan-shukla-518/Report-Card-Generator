import tkinter as tk
from tkinter import ttk, messagebox


#CONFIGURATION & DATA STORAGE


ROLL_PREFIX = "BTAI26O1"

SUBJECTS = [
    "Digital Logic Design",
    "Software Design and Development",
    "AI Landscape and Tools",
    "Python Programming",
    "Linear Algebra",
]

COLORS = {
    "bg": "#F1F5F9",            
    "header_bg": "#1E293B",     
    "header_fg": "#FFFFFF",     
    "accent": "#38BDF8",       
    "card_bg": "#FFFFFF",       
    "card_border": "#CBD5E1",   
    "text_dark": "#0F172A",     
    "text_muted": "#475569",    
    "primary": "#2563EB",       
    "primary_hover": "#1D4ED8",
    "row_alt": "#F8FAFC",       
    "prefix_bg": "#E2E8F0",     
}


students = []


#CORE LOGIC FUNCTIONS


def calculate_grade(percentage, passed_all):
   
    if not passed_all:
        return "F"
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


def get_grade_colors(grade):
   
    palette = {
        "A+": ("#DCFCE7", "#166534"),
        "A":  ("#DCFCE7", "#166534"),
        "B":  ("#DBEAFE", "#1E40AF"),
        "C":  ("#E0E7FF", "#3730A3"),
        "D":  ("#FEF9C3", "#854D0E"),
        "F":  ("#FEE2E2", "#991B1B"),
    }
    return palette.get(grade, ("#E2E8F0", "#0F172A"))


def create_student_record(name, roll_suffix, marks):

    total = sum(marks.values())
    max_total = len(SUBJECTS) * 100
    percentage = (total / max_total) * 100
    passed_all = all(score >= 40 for score in marks.values())
    grade = calculate_grade(percentage, passed_all)
    status = "PASS" if passed_all else "FAIL"

    return {
        "name": name,
        "roll_no": f"{ROLL_PREFIX}{roll_suffix}",
        "marks": marks,
        "total": total,
        "max_total": max_total,
        "percentage": percentage,
        "grade": grade,
        "status": status,
    }


def format_report_text(student):

    lines = [
        "=" * 48,
        "              STUDENT REPORT CARD",
        "=" * 48,
        f"Name    : {student['name']}",
        f"Roll No : {student['roll_no']}",
        "-" * 48,
        f"{'Subject':<34} {'Marks':>12}",
        "-" * 48,
    ]
    for subject, score in student["marks"].items():
        lines.append(f"{subject:<34} {score:>6.1f} / 100")

    lines.extend([
        "-" * 48,
        f"Total Marks : {student['total']:.1f} / {student['max_total']}",
        f"Percentage  : {student['percentage']:.2f}%",
        f"Grade       : {student['grade']}",
        f"Result      : {student['status']}",
        "=" * 48,
    ])
    return "\n".join(lines)


def save_report_to_file(student):
   
    filename = f"report_{student['roll_no']}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(format_report_text(student))
    messagebox.showinfo("Report Saved", f"Saved report card as:\n{filename}")



#GUI FUNCTIONS (Single-Page Updates)

def build_report_card_widget(parent, student, card_number):
    """Draw one styled report card in the right-hand reports panel."""
    card = tk.Frame(
        parent,
        bg=COLORS["card_bg"],
        highlightbackground=COLORS["card_border"],
        highlightthickness=1,
    )
    card.pack(fill="x", padx=(0, 14), pady=(0, 16))

    top_bar = tk.Frame(card, bg=COLORS["header_bg"], padx=16, pady=10)
    top_bar.pack(fill="x")

    left_info = tk.Frame(top_bar, bg=COLORS["header_bg"])
    left_info.pack(side="left", fill="x", expand=True)

    tk.Label(
        left_info,
        text=f"#{card_number}  {student['name']}",
        font=("Helvetica", 13, "bold"),
        bg=COLORS["header_bg"],
        fg="white",
    ).pack(anchor="w")

    tk.Label(
        left_info,
        text=f"Roll No: {student['roll_no']}",
        font=("Helvetica", 10),
        bg=COLORS["header_bg"],
        fg=COLORS["accent"],
    ).pack(anchor="w", pady=(2, 0))

    badge_bg, badge_fg = get_grade_colors(student["grade"])
    tk.Label(
        top_bar,
        text=f"Grade {student['grade']}",
        font=("Helvetica", 10, "bold"),
        bg=badge_bg,
        fg=badge_fg,
        padx=10,
        pady=4,
    ).pack(side="right")

    table = tk.Frame(card, bg=COLORS["card_bg"], padx=16, pady=10)
    table.pack(fill="x")
    table.columnconfigure(0, weight=3)
    table.columnconfigure(1, weight=1)
    table.columnconfigure(2, weight=1)

    for col, title in enumerate(["Subject", "Marks", "Status"]):
        anchor = "w" if col == 0 else "center"
        tk.Label(
            table,
            text=title,
            font=("Helvetica", 9, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_muted"],
            anchor=anchor,
        ).grid(row=0, column=col, sticky="ew", pady=(0, 6))

    for row_idx, (subject, score) in enumerate(student["marks"].items(), start=1):
        row_bg = COLORS["row_alt"] if row_idx % 2 == 1 else COLORS["card_bg"]
        subj_pass = score >= 40
        subj_status = "Pass" if subj_pass else "Fail"
        status_fg = "#166534" if subj_pass else "#991B1B"

        tk.Label(
            table, text=subject, font=("Helvetica", 10),
            bg=row_bg, fg=COLORS["text_dark"], anchor="w", padx=6, pady=4,
        ).grid(row=row_idx, column=0, sticky="ew")

        tk.Label(
            table, text=f"{score:.1f} / 100", font=("Helvetica", 10, "bold"),
            bg=row_bg, fg=COLORS["text_dark"], anchor="center", padx=6, pady=4,
        ).grid(row=row_idx, column=1, sticky="ew")

        tk.Label(
            table, text=subj_status, font=("Helvetica", 10, "bold"),
            bg=row_bg, fg=status_fg, anchor="center", padx=6, pady=4,
        ).grid(row=row_idx, column=2, sticky="ew")

    footer = tk.Frame(card, bg=COLORS["row_alt"], padx=16, pady=9)
    footer.pack(fill="x")

    summary_text = (
        f"Total: {student['total']:.1f}/{student['max_total']}   |   "
        f"{student['percentage']:.2f}%   |   Result: {student['status']}"
    )
    result_color = "#166534" if student["status"] == "PASS" else "#991B1B"

    tk.Label(
        footer,
        text=summary_text,
        font=("Helvetica", 10, "bold"),
        bg=COLORS["row_alt"],
        fg=result_color,
    ).pack(side="left")

    ttk.Button(
        footer,
        text="Save .txt",
        style="Small.TButton",
        command=lambda s=student: save_report_to_file(s),
    ).pack(side="right")


def refresh_reports_panel():
  
    for widget in reports_list_frame.winfo_children():
        widget.destroy()

    reports_heading.config(text=f"Generated Report Cards ({len(students)})")

    if not students:
        empty_box = tk.Frame(
            reports_list_frame,
            bg=COLORS["card_bg"],
            highlightbackground=COLORS["card_border"],
            highlightthickness=1,
            padx=24,
            pady=40,
        )
        empty_box.pack(fill="x", padx=(0, 14))

        tk.Label(
            empty_box,
            text="No report cards generated yet.",
            font=("Helvetica", 12, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack()

        tk.Label(
            empty_box,
            text="Fill in a student's details on the left and click Submit.",
            font=("Helvetica", 10),
            bg=COLORS["card_bg"],
            fg=COLORS["text_muted"],
        ).pack(pady=(6, 0))
        return

    for idx, student in enumerate(students, start=1):
        build_report_card_widget(reports_list_frame, student, idx)

    # Scroll smoothly to the newest report card at the bottom
    reports_canvas.update_idletasks()
    reports_canvas.yview_moveto(1.0)


def clear_form():
    """Reset all input fields so another student can be entered right away."""
    name_entry.delete(0, tk.END)
    roll_suffix_entry.delete(0, tk.END)
    for entry in subject_entries.values():
        entry.delete(0, tk.END)
    name_entry.focus()


def handle_submit():
    """Validate inputs, store the new student dictionary, and update the reports panel."""
    name = name_entry.get().strip()
    roll_suffix = roll_suffix_entry.get().strip()

    if not name:
        messagebox.showerror("Missing Name", "Please enter the student's name.")
        return

    if not (roll_suffix.isdigit() and len(roll_suffix) == 3):
        messagebox.showerror(
            "Invalid Roll Number",
            f"Enter exactly 3 digits after {ROLL_PREFIX} (for example: 001).",
        )
        return

    full_roll = f"{ROLL_PREFIX}{roll_suffix}"
    if any(s["roll_no"] == full_roll for s in students):
        messagebox.showerror(
            "Duplicate Roll Number",
            f"A report card for {full_roll} already exists.",
        )
        return

    marks = {}
    for subject, entry in subject_entries.items():
        raw_val = entry.get().strip()
        try:
            score = float(raw_val)
        except ValueError:
            messagebox.showerror(
                "Invalid Marks",
                f"Please enter a valid number for {subject}.",
            )
            return

        if score < 0 or score > 100:
            messagebox.showerror(
                "Out of Range",
                f"Marks for {subject} must be between 0 and 100.",
            )
            return

        marks[subject] = score

    # Build dictionary structure, append to master list, refresh right panel, reset form
    record = create_student_record(name, roll_suffix, marks)
    students.append(record)
    refresh_reports_panel()
    clear_form()


# ==========================================
# 4. SINGLE-PAGE WINDOW LAYOUT & THEME
# ==========================================

root = tk.Tk()
root.title("Student Report Card Generator")
root.geometry("1120x680")
root.minsize(920, 580)
root.configure(bg=COLORS["bg"])

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Primary.TButton",
    background=COLORS["primary"],
    foreground="white",
    font=("Helvetica", 11, "bold"),
    padding=(16, 10),
    borderwidth=0,
)
style.map("Primary.TButton", background=[("active", COLORS["primary_hover"])])

style.configure(
    "Secondary.TButton",
    background="#E2E8F0",
    foreground=COLORS["text_dark"],
    font=("Helvetica", 10, "bold"),
    padding=(14, 10),
    borderwidth=0,
)
style.map("Secondary.TButton", background=[("active", "#CBD5E1")])

style.configure(
    "Small.TButton",
    background=COLORS["header_bg"],
    foreground="white",
    font=("Helvetica", 9, "bold"),
    padding=(10, 4),
    borderwidth=0,
)
style.map("Small.TButton", background=[("active", "#334155")])

# --- Top App Header ---
header = tk.Frame(root, bg=COLORS["header_bg"], padx=24, pady=14)
header.pack(fill="x")

tk.Label(
    header,
    text="Student Report Card Generator",
    font=("Helvetica", 18, "bold"),
    bg=COLORS["header_bg"],
    fg=COLORS["header_fg"],
).pack(anchor="w")

tk.Label(
    header,
    text="B.Tech AI  •  Batch BTAI26O1  •  Automated Grade & Report System",
    font=("Helvetica", 10),
    bg=COLORS["header_bg"],
    fg=COLORS["accent"],
).pack(anchor="w", pady=(2, 0))

# --- Main Split Area (Left: Form | Right: Reports) ---
content = tk.Frame(root, bg=COLORS["bg"], padx=20, pady=20)
content.pack(fill="both", expand=True)

# LEFT COLUMN: Fixed-width Input Form Card
form_card = tk.Frame(
    content,
    bg=COLORS["card_bg"],
    highlightbackground=COLORS["card_border"],
    highlightthickness=1,
    padx=22,
    pady=20,
    width=390,
)
form_card.pack(side="left", fill="y", padx=(0, 20))
form_card.pack_propagate(False)

tk.Label(
    form_card,
    text="Enter Student Details",
    font=("Helvetica", 15, "bold"),
    bg=COLORS["card_bg"],
    fg=COLORS["text_dark"],
).pack(anchor="w", pady=(0, 14))

# Student Name
tk.Label(
    form_card,
    text="Student Name",
    font=("Helvetica", 10, "bold"),
    bg=COLORS["card_bg"],
    fg=COLORS["text_dark"],
).pack(anchor="w")

name_entry = tk.Entry(
    form_card,
    font=("Helvetica", 11),
    bg="white",
    fg=COLORS["text_dark"],
    insertbackground=COLORS["text_dark"],
    relief="solid",
    bd=1,
)
name_entry.pack(fill="x", pady=(4, 12), ipady=4)
name_entry.focus()

# Roll Number (Fixed prefix + 3-digit box)
tk.Label(
    form_card,
    text="Roll Number",
    font=("Helvetica", 10, "bold"),
    bg=COLORS["card_bg"],
    fg=COLORS["text_dark"],
).pack(anchor="w")

roll_row = tk.Frame(form_card, bg=COLORS["card_bg"])
roll_row.pack(fill="x", pady=(4, 14))

tk.Label(
    roll_row,
    text=ROLL_PREFIX,
    font=("Helvetica", 11, "bold"),
    bg=COLORS["prefix_bg"],
    fg=COLORS["text_dark"],
    padx=8,
    pady=4,
    relief="solid",
    bd=1,
).pack(side="left")

roll_suffix_entry = tk.Entry(
    roll_row,
    font=("Helvetica", 11),
    bg="white",
    fg=COLORS["text_dark"],
    insertbackground=COLORS["text_dark"],
    relief="solid",
    bd=1,
    width=6,
)
roll_suffix_entry.pack(side="left", padx=(6, 8), ipady=4)

tk.Label(
    roll_row,
    text="(3 digits, e.g. 001)",
    font=("Helvetica", 9),
    bg=COLORS["card_bg"],
    fg=COLORS["text_muted"],
).pack(side="left")

ttk.Separator(form_card, orient="horizontal").pack(fill="x", pady=(0, 12))

tk.Label(
    form_card,
    text="Subject Marks (out of 100)",
    font=("Helvetica", 11, "bold"),
    bg=COLORS["card_bg"],
    fg=COLORS["primary"],
).pack(anchor="w", pady=(0, 8))

# 5 Subject Inputs inside a clean grid
marks_grid = tk.Frame(form_card, bg=COLORS["card_bg"])
marks_grid.pack(fill="x")
marks_grid.columnconfigure(0, weight=1)

subject_entries = {}
for idx, subject in enumerate(SUBJECTS):
    tk.Label(
        marks_grid,
        text=subject,
        font=("Helvetica", 10),
        bg=COLORS["card_bg"],
        fg=COLORS["text_dark"],
        anchor="w",
    ).grid(row=idx, column=0, sticky="w", pady=6)

    entry = tk.Entry(
        marks_grid,
        font=("Helvetica", 11),
        bg="white",
        fg=COLORS["text_dark"],
        insertbackground=COLORS["text_dark"],
        relief="solid",
        bd=1,
        width=8,
        justify="center",
    )
    entry.grid(row=idx, column=1, sticky="e", pady=6, padx=(10, 0), ipady=3)
    subject_entries[subject] = entry

# Form Action Buttons
btn_frame = tk.Frame(form_card, bg=COLORS["card_bg"])
btn_frame.pack(fill="x", pady=(20, 0))

ttk.Button(
    btn_frame,
    text="Add & Generate Report",
    style="Primary.TButton",
    command=handle_submit,
).pack(side="left", fill="x", expand=True)

ttk.Button(
    btn_frame,
    text="Clear",
    style="Secondary.TButton",
    command=clear_form,
).pack(side="right", padx=(8, 0))

# RIGHT COLUMN: Scrollable Reports Panel
right_panel = tk.Frame(content, bg=COLORS["bg"])
right_panel.pack(side="right", fill="both", expand=True)

reports_heading = tk.Label(
    right_panel,
    text="Generated Report Cards (0)",
    font=("Helvetica", 14, "bold"),
    bg=COLORS["bg"],
    fg=COLORS["text_dark"],
)
reports_heading.pack(anchor="w", pady=(0, 12))

canvas_holder = tk.Frame(right_panel, bg=COLORS["bg"])
canvas_holder.pack(fill="both", expand=True)

reports_canvas = tk.Canvas(canvas_holder, bg=COLORS["bg"], highlightthickness=0)
reports_scrollbar = ttk.Scrollbar(
    canvas_holder, orient="vertical", command=reports_canvas.yview
)
reports_list_frame = tk.Frame(reports_canvas, bg=COLORS["bg"])

canvas_window = reports_canvas.create_window(
    (0, 0), window=reports_list_frame, anchor="nw"
)
reports_canvas.configure(yscrollcommand=reports_scrollbar.set)

reports_canvas.pack(side="left", fill="both", expand=True)
reports_scrollbar.pack(side="right", fill="y")

reports_list_frame.bind(
    "<Configure>",
    lambda e: reports_canvas.configure(scrollregion=reports_canvas.bbox("all")),
)
reports_canvas.bind(
    "<Configure>",
    lambda e: reports_canvas.itemconfig(canvas_window, width=e.width),
)

def on_mousewheel(event):
    if abs(event.delta) >= 120:
        reports_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    elif event.delta != 0:
        reports_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

root.bind_all("<MouseWheel>", on_mousewheel)

# Draw initial empty state
refresh_reports_panel()
root.mainloop()