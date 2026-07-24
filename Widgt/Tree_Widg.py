# ***************************************************************************************
#                                        Tree_Widg.py                                   *
#     ----------------     The  class  for  Frame Scroll and Tree        -------------  *
# ***************************************************************************************

import tkinter as tk
from tkinter import ttk
from Common.Constants import *
class TheFrame(tk.LabelFrame):
    def __init__(self, Parent, PosX, PosY, Click_On_Tree):
        super().__init__(Parent)
        self.configure(background=BACKGND, foreground='white',)
        self.configure(width=1, height=1,)
        self.configure(text='  ', labelanchor='n', padx=4, pady=4,
                       font=('Arial', 12, 'bold'))
        self.PosX = PosX
        self.PosY = PosY
        self.Clk_On_Tree = Click_On_Tree

        self.place(x=XY_TO_HIDE, y=XY_TO_HIDE)
        self.Tree_Scroll = ttk.Scrollbar(self)

        self.Tree_Scroll.pack(side='right', fill='y')
        self.Dummy       = None
        self.Loaded_List = []
        self.iFocus      = NO_FOCUS
        self.iLast_Row   = 0

        self.Reply       = 0
        self.Nrows     = 1
        self.nColToVis = 1
        self.Headings  = []
        self.Anchor    = []
        self.Width     = []

        self.Tree = ttk.Treeview(self,
                                 yscrollcommand=self.Tree_Scroll.set, selectmode="browse",
                                 style="mystyle.Treeview")  # , height=1)
        self.Tree.pack()
        self.Tree_Scroll.config(command=self.Tree.yview)

        # ---------------------  Bind to Click on one row of Tree      ------------------
        # self.my_tree.bind('<Double-1>', self.DobClk_OnTree)
        self.Tree.bind('<ButtonRelease-1>', self.click_on_tree)

        # h = ttk.Scrollbar(self, orient='horizontal')
        # h.pack(side='bottom', fill='x')

    # -----------------------------------------------------------------------------------
    def Frame_PosXY(self, Xpos, Ypos):
        self.place(x=Xpos, y=Ypos)

    # -----------------------------------------------------------------------------------
    def Frame_Title(self, Title):
        self.configure(text=Title)
    # -------------------------------------------
    def Frame_View(self):
        self.place(x=self.PosX, y=self.PosY)
    # -------------------------------------------
    def Frame_Hide(self):
        self.place(x=XY_TO_HIDE, y=XY_TO_HIDE)
    # -------------------------------------------
    def click_on_tree(self, arg):
        self.Dummy = arg
        strId = self.Tree.focus()
        if strId:
            RowValues = self.Tree.item(strId, 'values')
            self.Clk_On_Tree(RowValues)

    # def Get_Index_Of_Click(self):
    #     strId = self.Tree.focus()
    #     if strId:
    #         return int(strId)
    #     return 0

    # -------------------  CHECKED on colunms number  ------------------------
    def Tree_Setup_Strech(self, Form_List, IdStretch_List):
        self.Delete_All_Rows()
        self.Nrows       = Form_List[IX_TREE_ROW]
        # self.nColToVis   = Form_List[IX_TREE_COLMN]  n.u.
        self.Headings    = Form_List[IX_TREE_HEAD]
        self.Anchor      = Form_List[IX_TREE_ANCHOR]
        self.Width       = Form_List[IX_TREE_WIDTH]
        self.Tree.configure(height=self.Nrows)

        self.nColToVis = len(self.Headings)
        if self.nColToVis != len(self.Anchor) or self.nColToVis != len(self.Width):
            return f"Columns mismacthing on \n\n{self.Headings}\n\n{self.Anchor}\n\n{self.Width}"
        self.Tree['columns'] = list(range(self.nColToVis))
        self.Tree.heading("#0", text="", anchor='w')
        self.Tree.column("#0", width=0, stretch=False)

        for IdStrech in IdStretch_List:
            nColumn = IdStrech[1:]
            if nColumn > self.nColToVis:
                return False, f"stretching out of coluns for:\n\n{self.Headings}{self.Anchor[IdStrech]}"
            self.Tree.heading(IdStrech, text="", anchor='w')
            self.Tree.column(IdStrech, width=0, stretch=False)

        for jj in range(1, self.nColToVis + 1):
            self.Tree.column(f'#{jj}', width=self.Width[jj], anchor=self.Anchor[jj])
            self.Tree.heading(f'#{jj}', text=self.Headings[jj], anchor=self.Anchor[jj])

        self.Tree.tag_configure("oddrow", background="white", )
        self.Tree.tag_configure("evenrow", background="lightblue", )
        return ''

    # -------------------  NOT  checked on colunms number  ------------------------
    def Tree_Setup(self, Form_List):
        self.Delete_All_Rows()
        self.Nrows   = Form_List[IX_TREE_ROW]
        # self.nColToVis = Form_List[IX_TREE_COLMN]
        self.Headings  = Form_List[IX_TREE_HEAD]
        self.Anchor    = Form_List[IX_TREE_ANCHOR]
        self.Width     = Form_List[IX_TREE_WIDTH]
        self.Tree.configure(height=self.Nrows)
        self.nColToVis = len(self.Headings)

        # 1. Nascondiamo del tutto la colonna '#0' dell'albero (Tree) che non usiamo
        self.Tree["show"] = "headings"  # <--- Questo elimina la colonna radice ed evita pasticci

        # 2. Definiamo i nomi delle colonne dati (es. ['col1', 'col2', 'col3'...])
        # Ignoriamo il primo elemento [0] se era riservato all'header '#0'
        # col_names = [f"col_{i}" for i in range(1, len(self.Headings))]
        col_names = [f"col_{i}" for i in range(1, self.nColToVis)]
        self.Tree['columns'] = col_names

        # 3. Ciclo di configurazione usando I NOMI DELLE COLONNE
        for jj, col_name in enumerate(col_names, start=1):
            # Configuriamo la colonna usando il suo nome 'col_name'
            self.Tree.column(
                col_name,
                width=self.Width[jj],
                anchor=self.Anchor[jj],
                stretch=False
            )
            self.Tree.heading(
                col_name,
                text=self.Headings[jj],
                anchor=self.Anchor[jj]
            )

        self.Tree.tag_configure("oddrow", background="white")
        self.Tree.tag_configure("evenrow", background="lightblue")
        return ''

    # ----------------------------------  Load Values of Rows  --------------------------
    #   VERY IMPORTANT  List MUST  BE  list of lists  [ [], []... ]
    def Load_Row_Values(self, List):
        # self.Tree_Scroll.pack(side='right', fill='y')
        self.Loaded_List = List
        self.Delete_All_Rows()
        if not List:
            return ''       # No row to be loaded
        if type(List[0]) is not list:   # List contains list for every row
            return  f"Load_Row_Values list NOT a list of list on\n\n{self.Headings}"
        List_len = len(List[0])
        # if List_len != self.nColToVis + 1:
        #     return f"Load_Row_Values list len {str(List_len)}\nNOT equal to nCol_ToViw  {self.nColToVis}   for\n\n{self.Headings}"

        count = 0
        for Row in List:
            TreeRow = []
            for i in range(0, List_len):  #self.nColToVis):
                Val = str(Row[i]).replace('\n', '', 5)
                if Val == 'None':
                    Val = ''
                TreeRow.append(Val)
            Tag = "evenrow"
            if count % 2:
                Tag = "oddrow"
            self.Tree.insert('', 'end', text='', iid=str(count),
                             values=TreeRow[0:], tags=Tag)
            count += 1
        if self.iFocus != NO_FOCUS:
            self.Set_Focus(self.iFocus)
        return ''

    # -----------------------------------  Update  Values  ------------------------------
    def Update_Tree_Values(self, Val_Rec_ToUpdate):
        strId = self.Tree.focus()
        if strId:
            self.iFocus = int(strId)
            # RowVal = self.Tree.item(strId, 'values')
            self.Loaded_List[self.iFocus] = Val_Rec_ToUpdate
            List   = self.Loaded_List
            List[self.iFocus] = Val_Rec_ToUpdate
            self.Load_Row_Values(List)
        else:
            pass

    # ----------------------------    Get / Set Focus    --------------------------------
    def Set_Focus(self, nRow):   # startig from #0
        self.Clear_Focus()
        AllRows = self.Tree.get_children()
        LenAll  = len(AllRows)
        if nRow > LenAll:
            nRow = LenAll - 1
        Id = AllRows[nRow]
        self.Tree.selection_set(Id)
        self.Tree.focus(str(Id))

    def Set_Selection(self, Sel):   # startig from #0
        self.Clear_Focus()
        self.Tree.selection_set(Sel)

    def Get_Selection(self):
        return self.Tree.selection()

    def Clear_Focus(self):
        Sel = self.Tree.selection()
        self.Tree.selection_remove(Sel)

    # -------------------------------------------------------------------------------
    def Set_List_For_Focus(self, Start):
        myStart = Start
        newList = []
        Len = len(self.Loaded_List)
        for Index in range(0, Len):
            Rec = self.Loaded_List[myStart]
            newList.append(Rec)
            myStart += 1
            if myStart >= Len:
                myStart = 0
        self.Load_Row_Values(newList)
        self.Set_Focus(0)

    # -----------------------------------  Delete ALL Rows    ---------------------------
    def Delete_All_Rows(self):
        AllRows = self.Tree.get_children()
        for Row in AllRows:
            self.Tree.delete(Row)
# =======================================================================================
