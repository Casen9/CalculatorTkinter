import math
import os
import re
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


calculation = ""
lastErrorDetails = ""
ans = ""
calculation_history = []
addToCalcFlag = False

c = "3*10^8"  # m/s - predkosc swiatla
e = "1.602176634*10^-19"  # C - ladunek elementarny
G = "6.674*10^-11"  # N⋅m2/kg2 - stala grawitacji
me = "9.1093837*10^-31"  # kg - masa elektronu
mp = "1.67362192*10^-27"  # kg - masa protonu
mn = "1.67592749*10^-27"  # kg - masa neutronu
g = "9.81"  # m/s2 - przyspieszenie grawitacyjne na Ziemi
au = "1.495978707*10^11"  # m - jednostka astronomiczna
pc = "3.08567758149*10^16"  # m - parsek
ly = "0.946073*10^16"  # m - rok swietlny
Ms = "1.988*10^30"  # kg - masa Slonca
Mz = "5.972*10^24"  # kg - masa Ziemi
Rz = "6.378*10^6"  # m - promien rownikowy Ziemi
eV = "1.602176634*10^-19"  # J - elektronowolt
at = "101325"  # Pa - atmosfera

THEMES = {
    "blue": {
        "primary_bg": "#137FA6", "primary_fg": "white", "primary_active": "#106B8D",
        "secondary_bg": "#B9EDFF", "secondary_fg": "black", "secondary_active": "#A8DAEC"
    },
    "red": {
        "primary_bg": "#D93838", "primary_fg": "white", "primary_active": "#B82E2E",
        "secondary_bg": "#FFD1D1", "secondary_fg": "black", "secondary_active": "#ECA8A8"
    },
    "orange": {
        "primary_bg": "#E67E22", "primary_fg": "white", "primary_active": "#D35400",
        "secondary_bg": "#FFE5CC", "secondary_fg": "black", "secondary_active": "#FADBD8"
    },
    "green": {
        "primary_bg": "#27AE60", "primary_fg": "white", "primary_active": "#219653",
        "secondary_bg": "#D4EFDF", "secondary_fg": "black", "secondary_active": "#A9DFBF"
    },
    "purple": {
        "primary_bg": "#8E44AD", "primary_fg": "white", "primary_active": "#7D3C98",
        "secondary_bg": "#F5EEF8", "secondary_fg": "black", "secondary_active": "#E8DAEF"
    },
    "black": {
        "primary_bg": "#2C3E50", "primary_fg": "white", "primary_active": "#1A252F",
        "secondary_bg": "#E5E8E8", "secondary_fg": "black", "secondary_active": "#CCD1D1"
    },
    "twilight": {
        "primary_bg": "#54345F", "primary_fg": "white", "primary_active": "#472A51",
        "secondary_bg": "#C972AC", "secondary_fg": "white", "secondary_active": "#A95F90"
    },
    "frost": {
        "primary_bg": "#A9CCE3", "primary_fg": "black", "primary_active": "#7FB3D5",
        "secondary_bg": "#2E4053", "secondary_fg": "white", "secondary_active": "#243342"
    }
}


def applyTheme(*args):
    theme = themeVar.get()
    colors = THEMES.get(theme, THEMES["blue"])

    if 'btnEquals' in globals() and btnEquals and btnEquals.winfo_exists():
        btnEquals.config(bg=colors["primary_bg"], fg=colors["primary_fg"],
                         activebackground=colors["primary_active"], activeforeground=colors["primary_fg"])

    physics_buttons = [
        "btnPhysicsC", "btnPhysicsE", "btnPhysicsG", "btnPhysicsMe", "btnPhysicsMp",
        "btnPhysicsMn", "btnPhysicsGz", "btnPhysicsAu", "btnPhysicsPc", "btnPhysicsLy",
        "btnPhysicsMs", "btnPhysicsMz", "btnPhysicsRz", "btnPhysicsEv", "btnPhysicsAt"
    ]
    for btn_name in physics_buttons:
        if btn_name in globals():
            btn = globals()[btn_name]
            if btn and btn.winfo_exists():
                btn.config(bg=colors["secondary_bg"], fg=colors["secondary_fg"],
                           activebackground=colors["secondary_active"], activeforeground=colors["secondary_fg"])

    if 'btnExampleEquals' in globals() and btnExampleEquals and btnExampleEquals.winfo_exists():
        btnExampleEquals.config(bg=colors["primary_bg"], fg=colors["primary_fg"],
                                activebackground=colors["primary_active"], activeforeground=colors["primary_fg"])
    if 'btnExampleC' in globals() and btnExampleC and btnExampleC.winfo_exists():
        btnExampleC.config(bg=colors["secondary_bg"], fg=colors["secondary_fg"],
                           activebackground=colors["secondary_active"], activeforeground=colors["secondary_fg"])
    if 'btnExampleE' in globals() and btnExampleE and btnExampleE.winfo_exists():
        btnExampleE.config(bg=colors["secondary_bg"], fg=colors["secondary_fg"],
                           activebackground=colors["secondary_active"], activeforeground=colors["secondary_fg"])


def updateGeometry():
    width = 620 if physicsVar.get() == 1 else 350
    height = 550 if modeVar.get() == 0 else 400
    root.geometry(f"{width}x{height}")


def switchMode():
    if modeVar.get() == 0:
        buttonFrame.rowconfigure(8, weight=1)
        buttonFrame.rowconfigure(9, weight=1)

        btnMode.grid_remove()
        btnEquals.grid_remove()

        btnPower.grid(row=7, column=0, sticky="nsew")
        btnSqrt.grid(row=7, column=1, sticky="nsew")
        btnMod.grid(row=7, column=2, sticky="nsew")
        btnNewton.grid(row=7, column=3, sticky="nsew")
        btnPi.grid(row=8, column=0, sticky="nsew")
        btnSin.grid(row=8, column=1, sticky="nsew")
        btnCos.grid(row=8, column=2, sticky="nsew")
        btnTg.grid(row=8, column=3, sticky="nsew")
        btnMode.grid(row=9, column=0, columnspan=2, sticky="nsew")
        btnEquals.grid(row=9, column=3, sticky="nsew")
        btnAns.grid(row=9, column=2, sticky="nsew")

        btnMode.config(text="Basic mode")
    else:
        buttonFrame.rowconfigure(8, weight=0)
        buttonFrame.rowconfigure(9, weight=0)

        btnPower.grid_remove()
        btnSqrt.grid_remove()
        btnMod.grid_remove()
        btnNewton.grid_remove()
        btnPi.grid_remove()
        btnSin.grid_remove()
        btnCos.grid_remove()
        btnTg.grid_remove()
        btnMode.grid_remove()
        btnEquals.grid_remove()

        btnMode.grid(row=7, column=0, columnspan=2, sticky="nsew")
        btnEquals.grid(row=7, column=3, sticky="nsew")
        btnAns.grid(row=7, column=2, sticky="nsew")

        btnMode.config(text="Advanced mode")
    updateGeometry()


def switchPhysics():
    phys_buttons = [
        (btnPhysicsC, 2, 4), (btnPhysicsE, 2, 5), (btnPhysicsG, 2, 6),
        (btnPhysicsMe, 3, 4), (btnPhysicsMp, 3, 5), (btnPhysicsMn, 3, 6),
        (btnPhysicsGz, 4, 4), (btnPhysicsAu, 4, 5), (btnPhysicsPc, 4, 6),
        (btnPhysicsLy, 5, 4), (btnPhysicsMs, 5, 5), (btnPhysicsMz, 5, 6),
        (btnPhysicsRz, 6, 4), (btnPhysicsEv, 6, 5), (btnPhysicsAt, 6, 6)
    ]

    if physicsVar.get() == 1:
        for col in range(4, 7):
            buttonFrame.columnconfigure(col, weight=1)
        for btn, r, c_idx in phys_buttons:
            btn.grid(row=r, column=c_idx, sticky="nsew", padx=2, pady=2)
        textResult.grid(columnspan=7, row=1, column=0, sticky="nsew", padx=2, pady=2)
        historyFrame.grid(row=0, column=0, columnspan=7, sticky="ew", padx=5, pady=(5, 0))
    else:
        for col in range(4, 7):
            buttonFrame.columnconfigure(col, weight=0)
        for btn, _, _ in phys_buttons:
            btn.grid_remove()
        textResult.grid(columnspan=4, row=1, column=0, sticky="nsew", padx=2, pady=2)
        historyFrame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=(5, 0))

    updateGeometry()


def updateDisplay(text, errorInfo=None):
    global lastErrorDetails
    textResult.config(state="normal")
    textResult.delete(1.0, "end")

    if text in ["Error", "NameError", "SyntaxError", "MathError"]:
        textResult.config(fg="#DD0000")
        if errorInfo:
            lastErrorDetails = errorInfo
        if helpVar.get():
            btnHelp.place(in_=textResult, relx=1.0, rely=0.0, x=-3, y=3, anchor="ne")
    else:
        textResult.config(fg="#000000")
        btnHelp.place_forget()
    textResult.insert(1.0, text)
    textResult.config(state="disabled")


def addToCalculation(symbol):
    global calculation
    global addToCalcFlag
    ssymbol = str(symbol)
    if (not (addToCalcFlag and ssymbol=='.')): # dodac zmiane flagi na false po wpisaniu operatora jak + itd
        if (len(calculation)==0 or calculation.endswith('+') or calculation.endswith('-') or calculation.endswith('*') or calculation.endswith('/') or calculation.endswith('^') or calculation.endswith('√(') or calculation.endswith('mod') or calculation.endswith('sin(') or calculation.endswith('cos(') or calculation.endswith('tg(')):
            if (ssymbol == '.'):
                calculation += "0."
            else: calculation += ssymbol
            updateDisplay(calculation)
        elif not (ssymbol=='.' and calculation[len(calculation)-1]=='.'):
            calculation += ssymbol
            updateDisplay(calculation)
    if (ssymbol == '.'): addToCalcFlag = True
    elif (ssymbol=='+' or ssymbol=='-' or ssymbol=='*' or ssymbol=='/' or ssymbol=='^' or ssymbol=='√(' or ssymbol=='mod' or ssymbol=='sin(' or ssymbol=='cos(' or ssymbol=='tg('): addToCalcFlag = False
    if 'btnC' in globals() and btnC:
        btnC.config(text="C")


def evaluateCalculation():
    global calculation
    global ans
    if calculation != "":
        try:
            previous_calculation = calculation

            allowed_methods = {
                "pi": math.pi,
                "sin": lambda x: math.sin(math.radians(float(x))),
                "cos": lambda x: math.cos(math.radians(float(x))),
                "tg": lambda x: math.tan(math.radians(float(x))),
                "sqrt": lambda x: math.sqrt(float(x)),
                "factorial": lambda x: math.factorial(int(round(float(x)))),
            }
            eval_expr = calculation

            physics_constants = {
                "me": me, "mp": mp, "mn": mn, "Ms": Ms, "Mz": Mz, "Rz": Rz, "eV": eV,
                "au": au, "pc": pc, "ly": ly, "at": at, "c": c, "e": e, "G": G, "g": g
            }

            for const_name, const_val in physics_constants.items():
                eval_expr = re.sub(r'\b' + const_name + r'\b', f"({const_val})", eval_expr)

            open_brackets = eval_expr.count("(")
            close_brackets = eval_expr.count(")")
            if open_brackets > close_brackets:
                eval_expr += ")" * (open_brackets - close_brackets)
            eval_expr = eval_expr.replace("^", "**")
            eval_expr = eval_expr.replace("√(", "sqrt(")
            eval_expr = eval_expr.replace("%", "*0.01")
            eval_expr = eval_expr.replace("π", "pi")
            eval_expr = eval_expr.replace("mod", "%")
            eval_expr = eval_expr.replace("Ans", ans if ans else "0")
            eval_expr = re.sub(r'(\d+|\w+|\([^)]+\))!', r'factorial(\1)', eval_expr)

            result = eval(eval_expr, {"__builtins__": None}, allowed_methods)

            calculation = f"{result:.12g}"

            calculation_history.append((calculation, previous_calculation))

            ans = calculation
            if ans:
                lblAns.config(text=f"Ans = {ans}")
            else:
                lblAns.config(text="Ans = 0")
            lblCalc.config(text=previous_calculation)
            updateDisplay(calculation)

            # Po poprawnym obliczeniu wyniku, ustawiamy przycisk na "C"
            if 'btnC' in globals() and btnC:
                btnC.config(text="C")

        except Exception as err:
            errorName = type(err).__name__
            errorDesc = str(err)
            if errorName == "ZeroDivisionError":
                msg = "You cannot divide by 0!"
            elif errorName == "SyntaxError":
                msg = "Syntax is incorrect. Check brackets or symbols order."
            elif errorName == "NameError":
                msg = "Unknown symbol or function was used."
            else:
                msg = "Incorrect input data."
            fullDetails = f"{msg}\n\nTechnical settings:\nType: {errorName}\nDescription: {errorDesc}\n\nProvided equation:\n{calculation}"
            updateDisplay(errorName if errorName in ["SyntaxError", "NameError"] else "Error", errorInfo=fullDetails)


def handleClear():
    global calculation, ans, addToCalcFlag
    if 'btnC' in globals() and btnC and btnC.cget("text") == "C":
        # Pierwsze kliknięcie (jest "C") -> czyści tylko bieżący ekran
        calculation = ""
        updateDisplay(calculation)
        btnC.config(text="AC")
        addToCalcFlag = False
    else:
        calculation = ""
        ans = ""
        lblAns.config(text="Ans = 0")
        lblCalc.config(text="")
        updateDisplay(calculation)
        addToCalcFlag = False


def deleteLastSymbol():
    global calculation
    global addToCalcFlag
    if (calculation.endswith('.')): addToCalcFlag = False
    elif (calculation.endswith('+') or calculation.endswith('-') or calculation.endswith('*') or calculation.endswith('/') or calculation.endswith('^') or calculation.endswith('√(') or calculation.endswith('mod') or calculation.endswith('sin(') or calculation.endswith('cos(') or calculation.endswith('tg(')): addToCalcFlag = True
    calculation = calculation[:-1]
    updateDisplay(calculation)


def resetAns():
    global ans
    ans = ""
    lblAns.config(text="Ans = 0")


def showHelpWindow():
    messagebox.showerror("Error details", lastErrorDetails)


def handleKeyboard(event):
    if keybindsVar.get() == 1:
        if event.char in "0123456789+-*/()":
            addToCalculation(event.char)
        elif event.char == '=' or event.keysym == "Return":
            evaluateCalculation()
        elif event.keysym == "Escape":
            handleClear()
        elif event.char == '<' or event.keysym == "BackSpace":
            deleteLastSymbol()
        elif event.char.lower() == "s":
            addToCalculation("sin(")
        elif event.char.lower() == "c":
            addToCalculation("c" if physicsVar.get() == 1 else "cos(")
        elif event.char.lower() == "t":
            addToCalculation("tg(")
        elif event.char.lower() == "m":
            addToCalculation("mod")
        elif event.char == "%":
            addToCalculation("%")
        elif event.char.lower() == "v":
            addToCalculation("√(")
        elif event.char.lower() == "p":
            addToCalculation("π")
        elif event.char == "!":
            addToCalculation("!")
        elif event.char == "^":
            addToCalculation("^")
        elif event.char == ".":
            addToCalculation(".")
        elif event.char.lower() == "a":
            addToCalculation("Ans")
        elif event.char.lower() == "e" and physicsVar.get() == 1:
            addToCalculation("e")
        elif event.char == "g" and physicsVar.get() == 1:
            addToCalculation("g")
        elif event.char == "G" and physicsVar.get() == 1:
            addToCalculation("G")
        elif event.keysym == "Tab":
            modeVar.set(1 if modeVar.get() == 0 else 0)
            switchMode()
        elif event.char == "`":
            physicsVar.set(1 if physicsVar.get() == 0 else 0)
            switchPhysics()


def createScrollableTab(notebook, tab_text):
    tab_frame = ttk.Frame(notebook)
    notebook.add(tab_frame, text=tab_text)
    canvas = tk.Canvas(tab_frame, highlightthickness=0)
    scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = ttk.Frame(canvas)

    frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(frame_window, width=e.width))
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        bbox = canvas.bbox("all")
        if not bbox or canvas.winfo_height() >= bbox[3]: return
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
        else:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<Enter>", lambda e: [canvas.bind_all("<MouseWheel>", _on_mousewheel),
                                      canvas.bind_all("<Button-4>", _on_mousewheel),
                                      canvas.bind_all("<Button-5>", _on_mousewheel)])
    canvas.bind("<Leave>", lambda e: [canvas.unbind_all("<MouseWheel>"), canvas.unbind_all("<Button-4>"),
                                      canvas.unbind_all("<Button-5>")])
    return scrollable_frame


def openSettingsWindow():
    global btnExampleEquals, btnExampleC, btnExampleE
    settingsWin = tk.Toplevel(root)
    settingsWin.title("Settings")
    settingsWin.geometry("550x400")
    settingsWin.grab_set()
    settingsWin.minsize(400, 300)
    settingsWin.wm_iconphoto(False, settings_icon)

    btnClose = tk.Button(settingsWin, text="Close", command=settingsWin.destroy, font=("TkTextFont", 10), width=10)
    btnClose.pack(side="bottom", pady=10)

    notebook = ttk.Notebook(settingsWin)
    notebook.pack(fill='both', expand=True, padx=10, pady=5)

    scrollGeneral = createScrollableTab(notebook, "General")
    scrollAppearance = createScrollableTab(notebook, "Appearance")
    scrollKeybinds = createScrollableTab(notebook, "Keybinds")
    scrollHistory = createScrollableTab(notebook, "History")
    scrollPhysics = createScrollableTab(notebook, "Physics")

    tk.Checkbutton(scrollGeneral, text="Show help button when error occurred", variable=helpVar,
                   font=('TkTextFont', 10)).pack(anchor="w", padx=10, pady=15)
    # -----------------------
    tk.Label(scrollAppearance, text="Choose layout theme:", font=("TkTextFont", 10, 'bold')).pack(anchor="w", padx=10,
                                                                                                  pady=10)

    themeContainer = ttk.Frame(scrollAppearance)
    themeContainer.pack(fill="x", padx=10, pady=5)
    leftFrame = ttk.Frame(themeContainer)
    leftFrame.pack(side="left", anchor="n")

    tk.Radiobutton(leftFrame, text="Blue", variable=themeVar, value="blue", font=("TkTextFont", 10)).pack(anchor="w",
                                                                                                          padx=5,
                                                                                                          pady=2)
    tk.Radiobutton(leftFrame, text="Red", variable=themeVar, value="red", font=("TkTextFont", 10)).pack(anchor="w",
                                                                                                        padx=5, pady=2)
    tk.Radiobutton(leftFrame, text="Orange", variable=themeVar, value="orange", font=("TkTextFont", 10)).pack(
        anchor="w", padx=5, pady=2)
    tk.Radiobutton(leftFrame, text="Green", variable=themeVar, value="green", font=("TkTextFont", 10)).pack(anchor="w",
                                                                                                            padx=5,
                                                                                                            pady=2)
    tk.Radiobutton(leftFrame, text="Purple", variable=themeVar, value="purple", font=("TkTextFont", 10)).pack(
        anchor="w", padx=5, pady=2)
    tk.Radiobutton(leftFrame, text="Black", variable=themeVar, value="black", font=("TkTextFont", 10)).pack(anchor="w",
                                                                                                            padx=5,
                                                                                                            pady=2)
    tk.Radiobutton(leftFrame, text="Twilight", variable=themeVar, value="twilight", font=("TkTextFont", 10)).pack(
        anchor="w", padx=5, pady=2)
    tk.Radiobutton(leftFrame, text="Frost", variable=themeVar, value="frost", font=("TkTextFont", 10)).pack(anchor="w",
                                                                                                            padx=5,
                                                                                                            pady=2)

    rightFrame = ttk.Frame(themeContainer)
    rightFrame.pack(side="right", anchor="n", padx=(0, 20), pady=10)

    rightFrame.columnconfigure(0, weight=1, uniform="preview_buttons")
    rightFrame.columnconfigure(1, weight=1, uniform="preview_buttons")

    btnExampleEquals = tk.Button(rightFrame, text="=", font=("Arial", 11, "bold"), height=2, relief="raised")
    btnExampleEquals.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))

    btnExampleC = tk.Button(rightFrame, text="c", font=("Arial", 11, "bold"), width=6, height=2, relief="raised")
    btnExampleC.grid(row=1, column=0, sticky="ew", padx=(0, 4))

    btnExampleE = tk.Button(rightFrame, text="e", font=("Arial", 11, "bold"), width=6, height=2, relief="raised")
    btnExampleE.grid(row=1, column=1, sticky="ew", padx=(4, 0))

    applyTheme()
    # -----------------------
    tk.Checkbutton(scrollKeybinds, text="Enable keyboard shortcuts", variable=keybindsVar, font=('Arial', 10)).pack(
        anchor="w", padx=10, pady=15)

    keySeparator1 = ttk.Separator(scrollKeybinds, orient='horizontal')
    keySeparator1.pack(fill='x', padx=10, pady=5)

    tk.Label(scrollKeybinds, text="Keybinds:", font=("TkTextFont", 12, 'bold')).pack(anchor="w", padx=10, pady=10)

    raw_keybinds_text = (
        "- 1 - 1\n- 2 - 2\n- 3 - 3\n- 4 - 4\n- 5 - 5\n- 6 - 6\n- 7 - 7\n- 8 - 8\n- 9 - 9\n- 0 - 0\n"
        "- Esc - clear all\n- Backspace - erase last symbol\n- ( - open bracket\n- ) - close bracket\n"
        "- + - add\n- - - substrat\n- * - multiply\n- / - divide\n- s - sinus\n"
        "- c - cosinus (if Physics mode is on: speed of light)\n- t - tangens\n- a - answer\n"
        "- Tab - switch mode\n- ` - turn on/off Physics mode\n- . - point\n- % - percent\n"
        "- ^ - power\n- v - square root\n- m - modulo\n- ! - Newton\n- p - pi\n"
        "- e - elementary charge (if Physics mode is on)\n"
        "- g - Earth's gravitational acceleration (if Physics mode is on)\n"
        "- G - gravitational constant (if Physics mode is on)\n"
    )

    for line in raw_keybinds_text.strip().split("\n"):
        if " - " in line:
            parts = line[2:].split(" - ", 1)
            key_text = parts[0]
            description_text = parts[1]

            row = ttk.Frame(scrollKeybinds)
            row.pack(fill="x", padx=15, pady=3)

            tk.Label(row, text="- ", font=("TkTextFont", 10)).pack(side="left")

            key_label = tk.Label(
                row,
                text=key_text,
                font=("Arial", 10, "bold"),
                bg="#2d2d2d",
                fg="#ffffff",
                relief="raised",
                bd=1,
                padx=5,
                pady=1
            )
            key_label.pack(side="left")

            desc_label = tk.Label(row, text=f" - {description_text}", font=("TkTextFont", 10), justify="left",
                                  anchor="w")
            desc_label.pack(side="left", fill="x", expand=True, padx=2)

            row.bind("<Configure>", lambda event, lbl=desc_label: lbl.config(wraplength=max(50, event.width - 100)))
    # -----------------------
    columns = ("ans", "calculation")
    treeHistory = ttk.Treeview(scrollHistory, columns=columns, show="headings", height=12)

    treeHistory.heading("ans", text="Answer")
    treeHistory.heading("calculation", text="Calculation")

    treeHistory.column("ans", width=120, anchor="w")
    treeHistory.column("calculation", width=320, anchor="w")

    for res, calc in calculation_history:
        treeHistory.insert("", "end", values=(res, calc))

    treeHistory.pack(fill="both", expand=True, padx=10, pady=(10, 5))

    history_row = ttk.Frame(scrollHistory)
    history_row.pack(anchor="w", padx=10, pady=(5, 0))

    buttonEraseHistory = tk.Button(
        history_row, text="Delete history", font=("TkTextFont", 10), command=lambda: [
            calculation_history.clear(),
            treeHistory.delete(*treeHistory.get_children()),
            labelHistoryErased.pack(side="left", padx=10),
            root.after(3000, labelHistoryErased.pack_forget)
        ])
    buttonEraseHistory.pack(side="left")
    labelHistoryErased = tk.Label(history_row, text="History has been successfully deleted!", fg="green",
                                  font=("TkTextFont", 9))
    # -----------------------
    tk.Label(scrollPhysics, text="Modify physics constants:", font=("TkTextFont", 10, 'bold')).pack(anchor="w", padx=10,
                                                                                                    pady=10)

    physics_entries = {}

    constants_list = [
        ("c", "m/s"), ("e", "C"), ("G", "N⋅m²/kg²"),
        ("me", "kg"), ("mp", "kg"), ("mn", "kg"),
        ("g", "m/s²"), ("au", "m"), ("pc", "m"),
        ("ly", "m"), ("Ms", "kg"), ("Mz", "kg"),
        ("Rz", "m"), ("eV", "J"), ("at", "Pa")
    ]

    for name, unit in constants_list:
        row = ttk.Frame(scrollPhysics)
        row.pack(anchor="w", padx=15, pady=3)

        lbl_name = tk.Label(row, text=f"{name} = ", font=("TkTextFont", 10, "bold"), width=5, anchor="e")
        lbl_name.pack(side="left")

        entry = tk.Entry(row, font=("TkTextFont", 10), width=25)
        entry.insert(0, globals()[name])
        entry.pack(side="left", padx=5)
        physics_entries[name] = entry

        lbl_unit = tk.Label(row, text=unit, font=("TkTextFont", 10))
        lbl_unit.pack(side="left")

    action_row = ttk.Frame(scrollPhysics)
    action_row.pack(anchor="w", padx=15, pady=15)

    def save_physics_constants():
        for name, entry_widget in physics_entries.items():
            globals()[name] = entry_widget.get()
        labelPhysicsSaved.pack(side="left", padx=10)
        root.after(3000, labelPhysicsSaved.pack_forget)

    btnSavePhysics = tk.Button(action_row, text="Save changes", command=save_physics_constants, font=("TkTextFont", 10))
    btnSavePhysics.pack(side="left")
    labelPhysicsSaved = tk.Label(action_row, text="Physics constants have been successfully updated!", fg="green",
                                 font=("TkTextFont", 9))


root = tk.Tk()
root.title("Calculator")
root.geometry("350x400")
root.bind("<Key>", handleKeyboard)
root.minsize(350, 400)
calc_icon = tk.PhotoImage(file=resource_path("images\calculator.png"))
settings_icon_early = tk.PhotoImage(file=resource_path("images\settings.png"))
settings_icon = settings_icon_early.subsample(30, 30)
root.wm_iconphoto(True, calc_icon)

buttonFrame = tk.Frame(root)

for i in range(4):
    buttonFrame.columnconfigure(i, weight=1, uniform="cols")
for i in range(8):
    if i >= 2:
        buttonFrame.rowconfigure(i, weight=1, uniform="rows")
    else:
        buttonFrame.rowconfigure(i, weight=0)

textResult = tk.Text(buttonFrame, height=2, width=16, font=('Arial', 24), state="disabled")
textResult.grid(columnspan=4, row=1, column=0, sticky="nsew", padx=2, pady=2)

btnHelp = tk.Button(buttonFrame, text="?", command=showHelpWindow, font=('Arial', 8, 'bold'), fg="#DD0000",
                    bg="#C7C7C7", bd=0, padx=2, pady=2)

# Standardowe przyciski
btn1 = tk.Button(buttonFrame, text="1", command=lambda: addToCalculation(1), font=('Arial', 14)).grid(row=3, column=0,
                                                                                                      sticky="nsew")
btn2 = tk.Button(buttonFrame, text="2", command=lambda: addToCalculation(2), font=('Arial', 14)).grid(row=3, column=1,
                                                                                                      sticky="nsew")
btn3 = tk.Button(buttonFrame, text="3", command=lambda: addToCalculation(3), font=('Arial', 14)).grid(row=3, column=2,
                                                                                                      sticky="nsew")
btn4 = tk.Button(buttonFrame, text="4", command=lambda: addToCalculation(4), font=('Arial', 14)).grid(row=4, column=0,
                                                                                                      sticky="nsew")
btn5 = tk.Button(buttonFrame, text="5", command=lambda: addToCalculation(5), font=('Arial', 14)).grid(row=4, column=1,
                                                                                                      sticky="nsew")
btn6 = tk.Button(buttonFrame, text="6", command=lambda: addToCalculation(6), font=('Arial', 14)).grid(row=4, column=2,
                                                                                                      sticky="nsew")
btn7 = tk.Button(buttonFrame, text="7", command=lambda: addToCalculation(7), font=('Arial', 14)).grid(row=5, column=0,
                                                                                                      sticky="nsew")
btn8 = tk.Button(buttonFrame, text="8", command=lambda: addToCalculation(8), font=('Arial', 14)).grid(row=5, column=1,
                                                                                                      sticky="nsew")
btn9 = tk.Button(buttonFrame, text="9", command=lambda: addToCalculation(9), font=('Arial', 14)).grid(row=5, column=2,
                                                                                                      sticky="nsew")
btn0 = tk.Button(buttonFrame, text="0", command=lambda: addToCalculation(0), font=('Arial', 14)).grid(row=6, column=1,
                                                                                                      sticky="nsew")

btnOpen = tk.Button(buttonFrame, text="(", command=lambda: addToCalculation('('), font=('Arial', 14)).grid(row=2,
                                                                                                           column=2,
                                                                                                           sticky="nsew")
btnClose = tk.Button(buttonFrame, text=")", command=lambda: addToCalculation(')'), font=('Arial', 14)).grid(row=2,
                                                                                                            column=3,
                                                                                                            sticky="nsew")
btnPlus = tk.Button(buttonFrame, text="+", command=lambda: addToCalculation('+'), font=('Arial', 14),
                    bg="#CECECE").grid(row=3, column=3, sticky="nsew")
btnSub = tk.Button(buttonFrame, text="-", command=lambda: addToCalculation('-'), font=('Arial', 14), bg="#CECECE").grid(
    row=4, column=3, sticky="nsew")
btnMul = tk.Button(buttonFrame, text="*", command=lambda: addToCalculation('*'), font=('Arial', 14), bg="#CECECE").grid(
    row=5, column=3, sticky="nsew")
btnDiv = tk.Button(buttonFrame, text="/", command=lambda: addToCalculation('/'), font=('Arial', 14), bg="#CECECE").grid(
    row=6, column=3, sticky="nsew")

btnC = tk.Button(buttonFrame, text="AC", font=('Arial', 14), fg="#E00", bg="#FFECEC", command=handleClear)
btnC.grid(row=2, column=0, sticky="nsew")
btnBack = tk.Button(buttonFrame, text="<<", command=deleteLastSymbol, font=('Arial', 14), fg="#E9E919",
                    bg="#FFFFE8").grid(row=2, column=1, sticky="nsew")
btnPeriod = tk.Button(buttonFrame, text=".", command=lambda: addToCalculation('.'), font=('Arial', 14)).grid(row=6,
                                                                                                             column=2,
                                                                                                             sticky="nsew")
btnPercent = tk.Button(buttonFrame, text="%", command=lambda: addToCalculation("%"), font=('Arial', 14)).grid(row=6,
                                                                                                              column=0,
                                                                                                              sticky="nsew")

btnAns = tk.Button(buttonFrame, text="Ans", command=lambda: addToCalculation('Ans'), font=('Arial', 14))
btnAns.grid(row=7, column=2, sticky="nsew")
btnEquals = tk.Button(buttonFrame, text="=", command=evaluateCalculation, font=('Arial', 14), fg="white", bg="#137FA6",
                      activeforeground="white", activebackground="#106B8D")
btnEquals.grid(row=7, column=3, sticky="nsew")

btnMode = tk.Button(buttonFrame, text="Advanced mode",
                    command=lambda: [modeVar.set(1 if modeVar.get() == 0 else 0), switchMode()], font=('Arial', 14))
btnMode.grid(row=7, column=0, columnspan=2, sticky="nsew")

# Zaawansowane przyciski
btnPi = tk.Button(buttonFrame, text="π", command=lambda: addToCalculation("π"), font=('Arial', 14))
btnSin = tk.Button(buttonFrame, text="sin", command=lambda: addToCalculation("sin("), font=('Arial', 14))
btnCos = tk.Button(buttonFrame, text="cos", command=lambda: addToCalculation("cos("), font=('Arial', 14))
btnTg = tk.Button(buttonFrame, text="tg", command=lambda: addToCalculation("tg("), font=('Arial', 14))
btnPower = tk.Button(buttonFrame, text="x^", command=lambda: addToCalculation("^"), font=('Arial', 14))
btnSqrt = tk.Button(buttonFrame, text="√", command=lambda: addToCalculation("√("), font=('Arial', 14))
btnMod = tk.Button(buttonFrame, text="mod", command=lambda: addToCalculation("mod"), font=('Arial', 14))
btnNewton = tk.Button(buttonFrame, text="x!", command=lambda: addToCalculation("!"), font=('Arial', 14))

# Fizyczne przyciski
btnPhysicsC = tk.Button(buttonFrame, text="c", command=lambda: addToCalculation("c"), font=('Arial', 14), bg="#B9EDFF",
                        activebackground="#A8DAEC")
btnPhysicsE = tk.Button(buttonFrame, text="e", command=lambda: addToCalculation("e"), font=('Arial', 14), bg="#B9EDFF",
                        activebackground="#A8DAEC")
btnPhysicsG = tk.Button(buttonFrame, text="G", command=lambda: addToCalculation("G"), font=('Arial', 14), bg="#B9EDFF",
                        activebackground="#A8DAEC")
btnPhysicsMe = tk.Button(buttonFrame, text="me", command=lambda: addToCalculation("me"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsMp = tk.Button(buttonFrame, text="mp", command=lambda: addToCalculation("mp"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsMn = tk.Button(buttonFrame, text="mn", command=lambda: addToCalculation("mn"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsGz = tk.Button(buttonFrame, text="g", command=lambda: addToCalculation("g"), font=('Arial', 14), bg="#B9EDFF",
                         activebackground="#A8DAEC")
btnPhysicsAu = tk.Button(buttonFrame, text="1 au", command=lambda: addToCalculation("au"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsPc = tk.Button(buttonFrame, text="1 pc", command=lambda: addToCalculation("pc"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsLy = tk.Button(buttonFrame, text="1 ly", command=lambda: addToCalculation("ly"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsMs = tk.Button(buttonFrame, text="Ms", command=lambda: addToCalculation("Ms"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsMz = tk.Button(buttonFrame, text="Mz", command=lambda: addToCalculation("Mz"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsRz = tk.Button(buttonFrame, text="Rz", command=lambda: addToCalculation("Rz"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsEv = tk.Button(buttonFrame, text="1 eV", command=lambda: addToCalculation("eV"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")
btnPhysicsAt = tk.Button(buttonFrame, text="1 at", command=lambda: addToCalculation("at"), font=('Arial', 14),
                         bg="#B9EDFF", activebackground="#A8DAEC")

buttonFrame.pack(fill='both', padx=5, pady=2, expand=True)

historyFrame = tk.Frame(buttonFrame)
historyFrame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=(5, 0))

lblAns = tk.Label(historyFrame, text="Ans = 0", font=('Arial', 10), fg="grey")
lblAns.pack(side="left")
lblCalc = tk.Label(historyFrame, text="", font=('Arial', 10), fg="grey")
lblCalc.pack(side="right")

# MENUBAR
helpVar = tk.IntVar(value=1)
modeVar = tk.IntVar(value=1)
physicsVar = tk.IntVar(value=0)
keybindsVar = tk.IntVar(value=1)

themeVar = tk.StringVar(value="blue")
themeVar.trace_add("write", applyTheme)

menubar = tk.Menu(root)
calcbar = tk.Menu(menubar, tearoff=0)
insbar = tk.Menu(menubar, tearoff=0)
actionbar = tk.Menu(menubar, tearoff=0)
programbar = tk.Menu(menubar, tearoff=0)
numbar = tk.Menu(insbar, tearoff=0)
operbar = tk.Menu(insbar, tearoff=0)
symbar = tk.Menu(insbar, tearoff=0)
funbar = tk.Menu(insbar, tearoff=0)
psychbar = tk.Menu(insbar, tearoff=0)
infobar = tk.Menu(programbar, tearoff=0)

calcbar.add_radiobutton(label="Basic mode", command=switchMode, variable=modeVar, value=1)
calcbar.add_radiobutton(label="Advanced mode", command=switchMode, variable=modeVar, value=0)
calcbar.add_separator()
calcbar.add_checkbutton(label="Physics mode", command=switchPhysics, variable=physicsVar)
calcbar.add_separator()
calcbar.add_command(label="Settings...", command=openSettingsWindow, image=settings_icon, compound='left')

insbar.add_cascade(label="Numbers", menu=numbar)
insbar.add_cascade(label="Operations", menu=operbar)
insbar.add_cascade(label="Symbols", menu=symbar)
insbar.add_cascade(label="Functions", menu=funbar)
insbar.add_cascade(label="Physics", menu=psychbar)
insbar.add_separator()
insbar.add_command(label="π (pi)", command=lambda: addToCalculation('π'))
insbar.add_command(label="Ans (answer)", command=lambda: addToCalculation('Ans'))

actionbar.add_command(label="= (evaluate)", command=evaluateCalculation)
actionbar.add_separator()
actionbar.add_command(label="C / AC (clear / clear all)", command=handleClear)
actionbar.add_command(label="<< (erase last symbol)", command=deleteLastSymbol)
actionbar.add_command(label="Ans=0 (clear Ans variable)", command=resetAns)

numbar.add_command(label="0 (zero)", command=lambda: addToCalculation(0))
numbar.add_command(label="1 (one)", command=lambda: addToCalculation(1))
numbar.add_command(label="2 (two)", command=lambda: addToCalculation(2))
numbar.add_command(label="3 (three)", command=lambda: addToCalculation(3))
numbar.add_command(label="4 (four)", command=lambda: addToCalculation(4))

numbar.add_command(label="5 (five)", command=lambda: addToCalculation(5))
numbar.add_command(label="6 (six)", command=lambda: addToCalculation(6))
numbar.add_command(label="7 (seven)", command=lambda: addToCalculation(7))
numbar.add_command(label="8 (eight)", command=lambda: addToCalculation(8))
numbar.add_command(label="9 (nine)", command=lambda: addToCalculation(9))

operbar.add_command(label="+ (addition)", command=lambda: addToCalculation('+'))
operbar.add_command(label="- (substraction)", command=lambda: addToCalculation('-'))
operbar.add_command(label="* (multiplication)", command=lambda: addToCalculation('*'))
operbar.add_command(label="/ (division)", command=lambda: addToCalculation('/'))
operbar.add_command(label="x^ (power)", command=lambda: addToCalculation('^'))
operbar.add_command(label="√ (square root)", command=lambda: addToCalculation('√('))
operbar.add_command(label="mod (modulo)", command=lambda: addToCalculation('mod'))

symbar.add_command(label=". (point)", command=lambda: addToCalculation('.'))
symbar.add_command(label="% (percent)", command=lambda: addToCalculation('%'))
symbar.add_command(label="( (opening bracket)", command=lambda: addToCalculation('('))
symbar.add_command(label=") (closing bracket)", command=lambda: addToCalculation(')'))

funbar.add_command(label="sin (sinus)", command=lambda: addToCalculation('sin('))
funbar.add_command(label="cos (cosinus)", command=lambda: addToCalculation('cos('))
funbar.add_command(label="tg (tangens)", command=lambda: addToCalculation('tg('))
funbar.add_command(label="x! (Newton)", command=lambda: addToCalculation('!'))

psychbar.add_command(label="c (light speed) [m/s]", command=lambda: addToCalculation('c'))
psychbar.add_command(label="e (elementary charge) [C]", command=lambda: addToCalculation('e'))
psychbar.add_command(label="G (gravitational constant) [N⋅m2/kg^2]", command=lambda: addToCalculation('G'))
psychbar.add_command(label="me (electron mass) [kg]", command=lambda: addToCalculation('me'))
psychbar.add_command(label="mp (proton mass) [kg]", command=lambda: addToCalculation('mp'))
psychbar.add_command(label="mn (neutron mass) [kg]", command=lambda: addToCalculation('mn'))
psychbar.add_command(label="g (Earth's gravitational acceleration) [m/s^2]", command=lambda: addToCalculation('g'))
psychbar.add_command(label="1 au (1 astronomical unit) [m]", command=lambda: addToCalculation('au'))
psychbar.add_command(label="1 pc (1 parsec) [m]", command=lambda: addToCalculation('pc'))
psychbar.add_command(label="1 ly (1 light year) [m]", command=lambda: addToCalculation('ly'))
psychbar.add_command(label="Ms (Sun's mass) [kg]", command=lambda: addToCalculation('Ms'))
psychbar.add_command(label="Mz (Earth's mass) [kg]", command=lambda: addToCalculation('Mz'))
psychbar.add_command(label="Rz (Earth's equatorial radius) [kg]", command=lambda: addToCalculation('Rz'))
psychbar.add_command(label="1 eV (1 electronovolt) [J]", command=lambda: addToCalculation('eV'))
psychbar.add_command(label="1 at (1 atmosphere) [Pa]", command=lambda: addToCalculation('at'))

programbar.add_command(label="Info", command=lambda: messagebox.showinfo("Program info","Calculator v. 0.2.\n© Casen\n\nRelease date: 3rd June 2026\nUpdate date: 5th November 2026"))
programbar.add_cascade(label="Versions", menu=infobar)
infobar.add_command(label="Version 0.2 [current]", command=lambda: messagebox.showinfo("Version 0.2 [current]","VERSION 0.2\nRelease date: 5th November 2026\n\nFeatures:\n- added comma's ('.') new functionality based on what has been already written in calculator blocking repeated or wrong usage of comma and added autofill with '0.' when clicking comma button without any number behind it."))
infobar.add_command(label="Version 0.1", command=lambda: messagebox.showinfo("Version 0.1","VERSION 0.1\nRelease date: 3rd June 2026\n\nFeatures:\n- createdd the whole application with menus, buttons, functionality, advanced and physics modes."))
programbar.add_command(label="Quit", command=root.destroy)

menubar.add_cascade(menu=calcbar, label="Calculator")
menubar.add_cascade(menu=insbar, label="Insert")
menubar.add_cascade(menu=actionbar, label="Action")
menubar.add_cascade(menu=programbar, label="Program")
root.config(menu=menubar)

applyTheme()

root.mainloop()
