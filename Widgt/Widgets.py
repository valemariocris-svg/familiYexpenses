# ***************************************************************************************
#                                          Widgets.py                                   *
#     -------------------          WIDGETS  CLASSES     231003        ---------------   *
# ***************************************************************************************

from Common.Constants import *
from tkinter import ttk
import tkinter as tk

# =======================================================================================
# *****                      S T Y L E S                                            *****
# *****         Stand alone object: The styles are global                           *****
# =======================================================================================
class Widgets_Styles:
    def __init__(self):
        self.style = ttk.Style()

        # ====================   Default Style  TheButton   green    ====================
        self.style.map("DEF.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'white'), ('active', 'white'),
                        ('disabled', '#f66151')], )
        self.style.configure(style="DEF.TButton", background="#00A671",
                             foreground="white", borderwidth=1, font=("Arial", 12),
                             padding=6, relief="raised")

        # =====================  Colored  Style   TheButton  brown ======================
        self.style.map("COL.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'white'), ('active', 'white'),
                        ('disabled', '#f66151')], )
        self.style.configure(style="COL.TButton", background="#F1E638",         # "#9141ac",
                             foreground="red", borderwidth=1, font=("Arial", 12),
                             padding=6, relief="raised")

        # ======================   Bold Style  TheButton   ==============================
        self.style.map("BOL.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'white'), ('active', 'white')], )
        self.style.configure(style="BOL.TButton", background='#0eaa64',
                             foreground=FORGND,
                             borderwidth=3, font=("Arial", 13, 'bold'),
                             padding=7, relief="raised")

        # ====================   Default Style for Messages    =========================
        self.style.map("MSG.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'white'), ('active', 'white')], )
        self.style.configure(style="MSG.TButton", background='#gray',   #  "#00A671",
                             foreground='white',
                             borderwidth=1, font=("Arial", 12,),
                             padding=10, relief="raised")

        # ====================      Default Style  TheLable      ========================
        self.style.configure(style='INFO.TLabel', background=BACKGND, foreground='white',
                             font=('Arial', 13), padding=2, anchor='c',
                             relief='flat', borderwidth=3)
        self.style.configure(style='ERR.TLabel', background='#CFD956', foreground='red',
                             font=('Arial', 13, 'bold'), padding=4, anchor='c',
                             relief='sunken', borderwidth=3)

        # ========================   Style   TheTreeView       ==========================
        self.style.configure("mystyle.Treeview", highlightthickness=0,
                             bd=0, font=('Calibri', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 10, 'bold'))
        # Remove the borders ----------------------
        # self.style.layout("mystyle.Treeview",
        #                   [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])



# =======================================================================================
# =====================                 W I D G T E S                       =============
# =======================================================================================


# ==============================       T K      T E X T     =============================
class TheTextPoints(tk.Text):
    def __init__(self, Parent, Style, PosX, PosY, Nchar, Nrows, Texto, Points):
        super().__init__(Parent)
        self.Texto = Texto
        if Style == TXT_DISAB:
            self.configure(background="#559CC2", fg='#E1E2FF', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "disabled"
        elif Style == TXT_DIS_BLACK:
            self.configure(background="#559CC2", fg='black', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        elif Style == TXT_ENAB:    # Enabled to Insert data
            self.configure(background=COL_MUSTARD, fg='black', relief="sunken")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        elif Style == TXT_MSG_WHITE:
            self.configure(background=BACKGND, fg='white', relief="sunken")
            self.configure(padx=4, pady=4, font=('Courier', Points))
            self.State = "normal"
        elif Style == TXT_MSG_ERR:
            self.configure(background='gray', fg='yellow', relief="sunken")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        else:
            self.configure(background="#559CC2", fg='#E1E2FF', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "disabled"
            self.Texto = 'Text Code NOT found'

        self.Set_Text(self.Texto)
        # self.configure(padx=2,
        self.config(width=Nchar, height=Nrows)
        self.place(x=PosX, y=PosY)

    def Clear_Text(self):
        self.configure(state="normal")
        self.delete("1.0", "end")
        if self.State != "normal":
            self.configure(state='disabled')
    # ----------------------------------------------
    def Set_Text(self, myText):
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.insert('end', myText)
        if self.State != "normal":
            self.configure(state='disabled')
    # ----------------------------------------------
    def Get_Text(self, Type):
        Texto = self.get('1.0', 'end')
        if Type == INTEGER:
            if Texto == '\n' or not self.Test_Dec(Texto):
                return 0
            else:
                intTxt = Texto.replace('\n', '', 5)
            return int(intTxt)
        else:
            return Texto
    @classmethod
    def Test_Dec(cls, Texto):
        for Digit in Texto:
            if '0' <= Digit <= '9' or Digit == '\n':
                pass
            else:
                return False
        return True

# ----------------------------------------------------------------------------------------
class TheText(tk.Text):
    def __init__(self, Parent, Style, PosX, PosY, Nchar, Nrows, Texto):
        super().__init__(Parent)
        if Style == ANY:
            self.configure(state='disabled')
            self.config(width=1, height=1)
            self.place(x=XY_TO_HIDE, y=XY_TO_HIDE)
            return

        self.Pos_X  = PosX
        self.Pos_Y  = PosY
        self.Texto = Texto
        Points     = 12
        if Style == TXT_DISAB:
            self.configure(background="#0000FF", fg='#FFFFFF', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "disabled"
        elif Style == TXT_DIS_BLACK:
            self.configure(background="#559CC2", fg='black', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "disabled"

        elif Style == TXT_ENAB:    # Enabled to Insert data
            self.configure(background=COL_MUSTARD, fg='black', relief="sunken")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        elif Style == TXT_MSG_WHITE:
            self.configure(background=COL_MUSTARD, fg='white', relief="sunken")
            self.configure(padx=4, pady=4, font=('Courier', Points))
            self.State = "normal"
        elif Style == TXT_MSG_ERR:
            self.configure(background='gray', fg='yellow', relief="sunken")
            self.configure(padx=4, pady=4, font=('Courier', Points))
            self.State = "normal"
        else:
            self.configure(background="#559CC2", fg='#E1E2FF', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "disabled"
            self.Texto = 'Text Code NOT found'

        self.Set_Text(self.Texto)
        self.config(width=Nchar, height=Nrows)
        self.place(x=self.Pos_X, y=self.Pos_Y)
        self.Text_Enab_Disab(self.State)

    def Clear_Text(self):
        self.configure(state="normal")
        self.delete("1.0", "end")
        if self.State != "normal":
            self.configure(state='disabled')
    # ----------------------------------------------
    def Set_Text(self, myText):
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.insert('end', myText)
        if self.State != "normal":
            self.configure(state='disabled')
    # ----------------------------------------------
    def Get_Text(self, Type):
        Texto = self.get('1.0', 'end')
        if Type == INTEGER:
            if Texto == '\n' or not self.Test_Dec(Texto):
                return 0
            else:
                intTxt = Texto.replace('\n', '', 5)
            return int(intTxt)
        else:
            CleanTexto = Texto.replace('\n', '', 5)
            return CleanTexto

    @classmethod
    def Test_Dec(cls, Texto):
        for Digit in Texto:
            if '0' <= Digit <= '9' or Digit == '\n':
                pass
            else:
                return False
        return True

    def PosX(self, Position_X):
        self.place(x=Position_X)

    def PosXY(self, PosX, PosY):
        self.place(x=PosX, y=PosY)

    def Text_View(self):
        self.place(x=self.Pos_X, y=self.Pos_Y)
    # -------------------------------------------
    def Text_Hide(self):
        self.place(x=XY_TO_HIDE, y=XY_TO_HIDE)

    def Text_Enab_Disab(self, State):
        if State == "disabled":
            self.configure(state="disabled")
        else:
            self.configure(state="normal")


# ============================    T T K     L A B E L     ===============================
class TheLable(ttk.Label):
    def __init__(self, Parent, Style, PosX, PosY, nChar, Title):
        super().__init__(Parent)
        if Style == LAB_BLUE:
            self.configure(style='INFO.TLabel')
        elif Style == LAB_FILE_SEL:
            pass
        elif Style == LAB_ERR:
            self.configure(style='ERR.TLabel')
        self.place(x=PosX, y=PosY)
        self.configure(width=nChar, text=Title)
    def Set_Title(self, newTitle):
        self.configure(text=newTitle)


# ===============================     T T K      B U T T O N S     ======================
class TheButton(ttk.Button):
    def __init__(self, Parent, Style, PosX, PosY, Nchar, Name, Command):
        super().__init__(Parent)
        self.PosX = PosX
        self.PosY = PosY
        self.Btn_Text = ''
        if Style == BTN_DEF_DIS or Style == BTN_DEF_EN:
            self.config(style="DEF.TButton")
        elif Style == BTN_COL_DIS or Style == BTN_COL_EN:
            self.config(style="COL.TButton")
        elif Style == BTN_BOL_DIS or Style == BTN_BOL_EN:
            self.config(style="BOL.TButton")
        elif Style == BTN_MSG:
            self.configure(style='TButton')
        else:
            pass

        if Style == BTN_DEF_DIS or Style == BTN_COL_DIS or Style == BTN_BOL_DIS:
            self.configure(state='disabled')
        else:
            self.configure(state='normal')

        self.Btn_Text = Name
        self.configure(text=Name, command=Command, width=Nchar)
        self.place(x=PosX, y=PosY)

    def Btn_Enable(self):
        self.configure(style="COL.DEF.TButton")
        self.configure(state='normal')

    def Btn_Disable(self):
        self.configure(state='disabled')

    def Btn_Set_Status(self, Enable):
        if Enable:
            self.configure(state='normal')
        else:
            self.configure(state='disabled')

    def Btn_Ready_To_Click(self):
        self.configure(style="COL.TButton")                     #background="#559CC2", fg='#E1E2FF')

    def Place(self, toPlace):
        if not toPlace:
            self.place(x=XY_TO_HIDE, y=XY_TO_HIDE)
        else:
            self.place(x=self.PosX, y=self.PosY)
    def SetX(self, Posx):
        self.place(x=Posx)

    def Get_Text(self):
        return self.Btn_Text

    def Set_Text(self, Name):
        self.Btn_Text = Name
        self.configure(text=Name)

# ==============================     T T K     C O M B O      ===========================
# class TheCombo(ttk.Combobox):
#     def __init__(self, Parent, StrVar, PosX, PosY, Heigth, Nchar, List, strText, clk_Call):
#         super().__init__(Parent)
#         self.Dummy = 0
#         self.clk_Call = clk_Call
#         style = ttk.Style()
#         style.theme_settings("default", {
#         "TCombobox": {
#             "configure": {"padding": 3, "borderwidth": 3},
#             "map": {
#                 "background":      [("active", "white"),       # down arrow
#                                     ("readonly", "green")],
#                 "fieldbackground": [("readonly", "#559CC2")],  # Inside the combo
#                 "foreground":      [("focus", "black"),
#                                     ("readonly", "black")]
#             }
#         }},)
#
#         self.configure(style='TCombobox', textvariable=StrVar)
#         self.configure(state="readonly", values=List)
#         self.configure(font=("Arial", 11), height=Heigth, width=Nchar)
#         self.bind('<<ComboboxSelected>>', self.clk_Combo)
#         self.SetSelText(strText)
#         self.place(x=PosX, y=PosY)
#         self.Dummy = 0
#
#     def clk_Combo(self, *arg):
#         self.Dummy = arg
#         SelectedVal = self.get()
#         self.SetSelText(SelectedVal)
#         self.clk_Call(SelectedVal)
#
#     def PosX(self, PosX):
#         self.place(x=PosX)
#
#     def SetSelText(self, Val1):
#         self.set("")
#         self.set(Val1)
#
#     def SetValues(self, Values):
#         self.configure(values=[' '])
#         self.configure(values=Values)
#
#     def GetValue(self):
#         return self.get()
# =======================================================================================
# ==============================     T T K     C O M B O      ===========================
class TheCombo(ttk.Combobox):
    def __init__(self, Parent, StrVar, PosX, PosY, Heigth, Nchar, List, strText, clk_Call):
        super().__init__(Parent)
        self.Dummy = 0
        self.clk_Call = clk_Call

        # --- CONFIGURAZIONE STILE PERSONALIZZATO ---
        style = ttk.Style()
        # Usiamo un nome unico come 'Custom.TCombobox' invece di quello globale
        style.configure("Custom.TCombobox", padding=3, borderwidth=3)
        style.map("Custom.TCombobox",
                  background=[("active", "white"), ("readonly", "green")],
                  fieldbackground=[("readonly", "#559CC2")],
                  foreground=[("focus", "black"), ("readonly", "black")]
                  )
        # -------------------------------------------

        # Applichiamo lo stile personalizzato 'Custom.TCombobox'
        self.configure(style='Custom.TCombobox', textvariable=StrVar)
        self.configure(state="readonly", values=List)
        self.configure(font=("Arial", 11), height=Heigth, width=Nchar)
        self.bind('<<ComboboxSelected>>', self.clk_Combo)
        self.SetSelText(strText)
        self.place(x=PosX, y=PosY)
        self.Dummy = 0

    def clk_Combo(self, *arg):
        self.Dummy = arg
        SelectedVal = self.get()
        self.SetSelText(SelectedVal)
        self.clk_Call(SelectedVal)

    def PosX(self, PosX):
        self.place(x=PosX)

    def SetSelText(self, Val1):
        self.set("")
        self.set(Val1)

    def SetValues(self, Values):
        self.configure(values=[' '])
        self.configure(values=Values)

    def GetValue(self):
        return self.get()
