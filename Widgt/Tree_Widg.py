# ***************************************************************************************
#                                        Tree_Widg.py                                   *
#     ----------------     The  class  for  Frame Scroll and Tree        -------------  *
# ***************************************************************************************

import tkinter as tk
from tkinter import ttk
from Common.Constants import *
from Widgt.Dialogs import Message_Dlg

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

    def Get_Index_Of_Click(self):
        strId = self.Tree.focus()
        if strId:
            return int(strId)
        return 0

    # -------------------------------------------
    def Tree_Setup_Strech(self, Form_List, IdStretch_List):
        self.Delete_All_Rows()
        self.Nrows       = Form_List[IX_TREE_ROW]
        self.nColToVis   = Form_List[IX_TREE_COLMN]
        self.Headings    = Form_List[IX_TREE_HEAD]
        self.Anchor      = Form_List[IX_TREE_ANCHOR]
        self.Width       = Form_List[IX_TREE_WIDTH]
        self.Tree.configure(height=self.Nrows)

        tot_col = self.nColToVis + 1
        if len(self.Headings) != tot_col or len(self.Anchor) != tot_col or len(self.Anchor) != tot_col or len(self.Width) != tot_col:
            return 'Mismathing on number of columns '
        str_last_col = IdStretch_List[0]
        last_stretch = int(str_last_col[1:])
        if (tot_col-1) != last_stretch:
            return f"Mismathing on getting {IdStretch_List}  tot column= {tot_col} "
        pass

        self.Tree['columns'] = list(range(self.nColToVis))
        self.Tree.heading("#0", text="", anchor='w')
        self.Tree.column("#0", width=0, stretch=False)

        for IdStrech in IdStretch_List:
            self.Tree.heading(IdStrech, text="", anchor='w')
            self.Tree.column(IdStrech, width=0, stretch=False)

        for jj in range(1, self.nColToVis + 1):
            self.Tree.column(f'#{jj}', width=self.Width[jj], anchor=self.Anchor[jj])
            self.Tree.heading(f'#{jj}', text=self.Headings[jj], anchor=self.Anchor[jj])

        self.Tree.tag_configure("oddrow", background="white", )
        self.Tree.tag_configure("evenrow", background="lightblue", )
        return ''

    # -------------------------------------------
    def Tree_Setup(self, Form_List):
        self.Delete_All_Rows()
        self.Nrows       = Form_List[IX_TREE_ROW]
        self.nColToVis   = Form_List[IX_TREE_COLMN]
        self.Headings    = Form_List[IX_TREE_HEAD]
        self.Anchor      = Form_List[IX_TREE_ANCHOR]
        self.Width       = Form_List[IX_TREE_WIDTH]
        self.Tree.configure(height=self.Nrows)

        self.Tree['columns'] = list(range(self.nColToVis))
        self.Tree.heading("#0", text="", anchor='w')
        self.Tree.column("#0", width=0, stretch=False)
        for jj in range(1, self.nColToVis + 1):
            self.Tree.column(f'#{jj}', width=self.Width[jj], anchor=self.Anchor[jj])
            self.Tree.heading(f'#{jj}', text=self.Headings[jj], anchor=self.Anchor[jj])

        self.Tree.tag_configure("oddrow", background="white", )
        self.Tree.tag_configure("evenrow", background="lightblue", )
        pass

    # ----------------------------------  Load Values of Rows  --------------------------
    #   VERY IMPORTANT  List MUST  ME  list of lists  [ [], []... ]
    def Load_Row_Values(self, List):
        # self.Tree_Scroll.pack(side='right', fill='y')
        self.Loaded_List = List
        self.Delete_All_Rows()
        inner_list = List[0]
        if type(inner_list) is not list:
            return  'Load_Row_Values list NOT a List of list'
        count = 0
        List_len = len(List[0])
        if List_len != self.nColToVis:
            return 'Load_Row_Values list len NOT equal nCol_TovVis'
        for Row in List:
            TreeRow = []
            for i in range(0, self.nColToVis):
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

    # -------------------------------  Delete Last Row on Tree    -----------------------
    def Delete_Tree_Last_Row(self):
        List = []
        Len = len(self.Loaded_List)
        Last_Index = Len-1
        # LastRec = self.Loaded_List[Last_Index]

        for i in range(0, Last_Index):
            List.append(self.Loaded_List[i])
        self.iFocus    = Last_Index-1
        self.Load_Row_Values(List)
    #
    # -----------------------------  Inseert Record  on End   ---------------------------
    def Add_ToEnd_Tree_Values(self, Row_Rec):
        List = self.Loaded_List
        Len = len(self.Loaded_List)
        Last_Index = Len
        List.append(Row_Rec)

        iLast_Row = len(List) -1
        self.iFocus    = iLast_Row
        self.Load_Row_Values(List)
        Mess = 'Added Codes Record:\nTR Code: ' + str(Last_Index)  + '\n'
        for Val in Row_Rec:
            Mess += str(Val)
            Mess += '\n'
        Msg_Dlg = Message_Dlg(MSG_BOX_INFO, Mess)
        Msg_Dlg.wait_window()

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
