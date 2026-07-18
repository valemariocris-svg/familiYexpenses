# ***************************************************************************************
#                                        Tree_Widg.py                                   *
#     ----------------     The  class  for  Frame Scroll and Tree        -------------  *
# ***************************************************************************************

import tkinter as tk

from Common.Constants import BACKGND


# -------------------------------------------------------------------------------------------------
class CreateCanvas(tk.Canvas):
    def __init__(self, Parent, PosX, PosY, Width, Heigth):
        super().__init__(Parent)
        self.configure(background=BACKGND, selectforeground="white")
        self.configure(border=20, width=Width, height=Heigth,)

        self.PosX = PosX
        self.PosY = PosY
        self.place(x=PosX, y=PosY)

# -------------------------------------------------------------------------------------------------
class FrameOnly(tk.LabelFrame):
    def __init__(self, Parent, PosX, PosY, Width, Heigth):
        super().__init__(Parent)
        self.configure(background="lightblue", foreground='black',)
        self.configure(width=Width, height=Heigth,)
        # self.configure(text='  ', labelanchor='n', padx=4, pady=4,
        #                font=('Arial', 12, 'bold'))
        self.PosX = PosX
        self.PosY = PosY

        self.place(x=PosX, y=PosX)

        # self.place(x=XY_TO_HIDE, y=XY_TO_HIDE)
        # self.Tree_Scroll = ttk.Scrollbar(self)
        # posXY =self.Tree_Scroll.xy()

        # self.Tree_Scroll.pack(side='right', fill='y')

        self.Dummy       = None
        # self.Loaded_List = []
        # self.iFocus      = -1
        # self.iLast_Row   = 0
        #
        # self.Reply       = 0
        # self.Nrows     = 1
        # self.nColToVis = 1
        # self.Headings  = []
        # self.Anchor    = []
        # self.Width     = []
        #
        # self.Tree = ttk.Treeview(self,
        #                          yscrollcommand=self.Tree_Scroll.set, selectmode="browse",
        #                          style="mystyle.Treeview")  # , height=1)
        # self.Tree.pack()
        # self.Tree_Scroll.config(command=self.Tree.yview)
        #
        # # ---------------------  Bind to Click on one row of Tree      ------------------
        # # self.my_tree.bind('<Double-1>', self.DobClk_OnTree)
        # self.Tree.bind('<ButtonRelease-1>', self.click_on_tree)


# ===============================================================================================
