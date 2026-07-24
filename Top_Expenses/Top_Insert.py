# ------------------------------------------------------------------------------------- #
#                      *****     Top_Insert.py     *****                                #
#                  Insert Transactions on Transactions database                         #
#                                                                                       #
# ------------------------------------------------------------------------------------- #

# import os
import tkinter as tk
from enum import CONTINUOUS

from Top_Expenses.Modules_Manager import Modul_Mngr
from Chat import Ms_Chat
from Common.Common_Functions import *
from Data_Classes.Transact_DB import Data_Manager

from Widgt.Dialogs import Print_Received_Message
from Widgt.Dialogs import Message_Dlg
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheText
from Widgt.Widgets import TheCombo

# ==================================================================================================== #
#  --------------------        class Top_Insert(tk.Toplevel)        --------------------------------   #
# ==================================================================================================== #
class Top_Insert(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data_Manager
        self.Mod_Mngr = Modul_Mngr
        self.List     = List

        self.Chat.Attach([self, TOP_INS])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
        self.resizable(False, False)
        self.configure(background=BACKGND)
        self.title('*****     Insertion  of Transactions on Database     *****')
        self.geometry(TOP_INSERT_GEOMETRY)
        self.Dummy       = 0
        self.Files_Ident = self.Data.Get_Full_Xlsx_Transact_Ident()
        self.Conto       = self.Files_Ident[IX_XLSX_CONTO]
        self.intYear     = self.Files_Ident[IX_XLSX_YEAR]
        self.intMonth    = self.Files_Ident[IX_XLSX_MONTH]
        self.Full_Month  = ''

        self.Tree_Transact_Title      = ''
        self.Transact_InDatabase_List = []
        self.Full_Filename_For_Insert = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)

        self.Txt_TransactName = TheText(self, TXT_DISAB,  20,  20, 18,  1, '')
        self.Txt_Xlsx_Name    = TheText(self, TXT_DISAB, 200,  20, 19,  1, '')
        self.Txt_Conto        = TheText(self, TXT_DISAB, 370,  20, 12,  1, '')
        self.Txt_Xlsx_Year    = TheText(self, TXT_DISAB, 484,  20, 11,  1, '')
        self.Txt_Xlsx_Month   = TheText(self, TXT_DISAB, 590,  20, 11,  1, '')

        #  ------------------------------------  B U T T O N s  ---------------------------------------
        self.ViewXlsx     = TheButton(self, BTN_DEF_DIS,       20, 860, 23, 'Show Rows on Xlsx', self.Clk_View_Xlsx)
        self.ViewTransact = TheButton(self, BTN_DEF_DIS,       20, 900, 23, 'Show Transactions on Db',
                                      self.Clk_View_Transact)
        self.nRows_Default = '4'
        self.Continue      = self.Data.Get_sel_dictionary_value(TRANSACT_INSERT_MODE)
        self.StrVar_Conto  = tk.StringVar
        self.OptMenu_Cont  = TheCombo(self, self.StrVar_Conto, 260, 820, 15, 24, CONTINUE_LIST,
                                      self.Continue, self.Clk_Continue)
        self.Ins_Btn      = TheButton(self, BTN_DEF_DIS,       260, 860, 23, 'Insert Transaction on Db', self.Clk_Insert)
        # self.Btn_Clear_Db = TheButton(self, BTN_DEF_EN,        260, 900, 23, '',          self.Clk_Clear_Transactions_Db)

        self.Check_Verify = TheButton(self, BTN_DEF_EN,       500, 860, 23, 'check xlsx / transact.', self.Clk_Verify)
        self.nTotRows_Text= TheText(self, TXT_ENAB,            490, 820,  5,  1, self.nRows_Default)
        self.Exit         = TheButton(self, BTN_DEF_EN,        500, 900, 23, '  E X I T  ',  self.Call_OnClose)

        self.Total             = []
        self.Tot_WithoutCode   = 0
        self.Xlsx_Filename     = ''
        self.Xlsx_Year         = 0
        self.WithList          = []
        self.Rows_WithCod_List = []

        self.Records_ToIns_List= []
        self.List_ToInsert_OK  = False
        self.Remain_List       = []
        self.TotTransact_ToBeInserted = 0
        self.Transact_Filename        = ''
        self.Transact_Year            = 0

        # --------------------------  T R E E     Transactions to insert   ----------------------------
        self.Frame_Transact = TheFrame(self, 20, 60, self.Clk_Ontree_View)
        self.Frame_Transact_Setup()
        self.Frame_Transact.Frame_View()
        self.Set_Frame_Rows()
        self.Set_Texts()
        self.Set_Buttons()

    # -------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_INS)
        self.destroy()

    # -------------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:               # Close
            self.Call_OnClose()

    # -------------------------------------------------------------------------------------------------
    def Set_Buttons(self):
        Xlsx_Filename = self.Data.Get_sel_dictionary_value(XLSX_FILENAME)     # self.Data.Get_Selections_Member(IX_XLSX_FILE)
        if Xlsx_Filename != UNKNOWN:
            if self.Mod_Mngr.Cek_Xlsx_Name(Xlsx_Filename):
                self.ViewXlsx.Btn_Enable()
        Transact_Filename = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)
        if Transact_Filename != UNKNOWN:
            if Gl_Cek_Transactions_Name(Transact_Filename):
                self.ViewTransact.Btn_Enable()
        self.Ins_Btn.Btn_Enable()

    # -------------------------------------------------------------------------------------------------
    def Set_Frame_Rows(self):
        # self.Rows_WithCod_List  = self.Data.Get_Rows_WithCod_List()
        pass
        self.Records_ToIns_List = self.Data.Get_Records_ToInsert_List()
        self.Load_Tree(self.Records_ToIns_List)

    # -------------------------------------------------------------------------------------------------
    # def Set_Data(self):
    #     # IX_TOT_ROWS_OK, IX_TOT_ROWS_WITH_CODE, IX_TOT_ROWS_WITHOUT_CODE
    #     self.Total             = self.Data.Get_Total_Rows()
    #     self.Xlsx_Filename     = self.Data.Get_sel_dictionary_value(XLSX_FILENAME)
    #     self.Transact_Filename = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)
    #
    #     self.Transact_Year     = self.Data.Get_TransacYear()

    # --------------------------------------------------------------------------------------------------
    def Purge_FulDesc(self, All, Full_Desc):
        self.Dummy = 0
        ToCheck = Full_Desc
        if All:
           ToCheck = Full_Desc[21:]
        Purged = ''
        for Char in ToCheck:
            if Char == '\n':
                pass
            else:
                Purged += Char
        return Purged

    # ---------------------------------------------------------------------------------------------------
    def Ask_For_RecToInsert(self, RecToIns):
        TrCode  = str(RecToIns[IX_TRANSACT_TR_CODE])
        Contab  = RecToIns[IX_TRANSACT_CONTAB]
        Valuta  = RecToIns[IX_TRANSACT_VALUTA]
        Accred  = str(RecToIns[IX_TRANSACT_ACCRED])
        Addeb   = str(RecToIns[IX_TRANSACT_ADDEB])
        TRdesc  = self.Data.Get_TrDesc_FromCode(TrCode)
        TRfull  = RecToIns[IX_TRANSACT_FULL_DESC]
        Purged  = self.Purge_FulDesc(False, TRfull)

        # Message  = "Confirm to insert record:\n\n"
        # Message += Contab + "   " + Valuta + "\n"
        # Message += TRdesc + "\n"
        # Message += Accred + "   " + Addeb +"\n\n"
        # Message += Purged

        Message =  "Confirm to insert record:\n\nCode=" + TrCode + "    Desc=" + TRdesc+ "\n"
        Message += "Contab=" + Contab + "    Valuta=" + Valuta + "\n"
        Message += "Accred=" + Accred + "    Addeb=" + Addeb + "\n\n"
        Message += "Full desc: " + Purged
        pass

        Msg_Dlg = Message_Dlg(MSG_BOX_ASK, Message)
        Msg_Dlg.wait_window()
        Reply = Msg_Dlg.data
        return Reply

    # -------------------------------------------------------------------------------------------------
    def Clk_Continue(self, Value):
        self.Continue = Value
        self.Data.Update_Selections(Value, TRANSACT_INSERT_MODE)
        nRows = self.nTotRows_Text.Get_Text(INTEGER)
        if nRows <= 1:
            self.nTotRows_Text.Set_Text(self.nRows_Default)
        else:
            if self.Continue == NREC:
                self.nRows_Default = self.nTotRows_Text.Get_Text(STRING)

    # -------------------------------------------------------------------------------------------------
    def Check_For_Record_ToInsert(self, RecToInsert):
        if self.Continue == STEP:
            Reply = self.Ask_For_RecToInsert(RecToInsert)
            if Reply == YES:
                return True
            return False
        elif self.Continue == CONTINUOUS:
            return True
        else:
            nRows = self.nTotRows_Text.Get_Text(INTEGER)
            nRows -= 1
            if nRows < 0:
                self.nTotRows_Text.Set_Text(self.nRows_Default)
                return False
            else:
                self.nTotRows_Text.Set_Text(str(nRows))
                return True

    # -------------------------------------------------------------------------------------------------
    def Clk_Insert(self):
        self.Ins_Btn.Btn_Disable()
        IndexEnd          = len(self.Records_ToIns_List)
        self.Remain_List  = self.Records_ToIns_List.copy()
        # for Index in range(0, IndexEnd):
        #     RecToIns    = self.Records_ToIns_List[Index]
        #     if self.Check_For_Record_ToInsert(RecToIns):
        #         Result = self.Data.Insert_Transact_Record(RecToIns)     # it opens also Db
        #         if Result != OK:
        #             Msg_Dlg = Message_Dlg(MSG_BOX_ERR, Result)
        #             Msg_Dlg.wait_window()
        #             return
        #         del self.Remain_List[0]
        #         self.Load_Tree(self.Remain_List)
        #     else:
        #         break

        # Reload Rows etc for Insert --------------------
        # self.Records_ToIns_List = self.Remain_List
        # self.Set_Data()
        # self.Set_Texts()
        # self.Mod_Mngr.Initialize_codes_xlsx_transact(TOP_INS)
        # self.Set_Frame_Rows()
        # self.Ins_Btn.Btn_Enable()

    # -------------------------------------------------------------------------------------------------
    def Set_Texts(self):
        self.Files_Ident = self.Data.Get_Full_Xlsx_Transact_Ident()
        self.Conto       = self.Files_Ident[IX_XLSX_CONTO]
        self.intYear     = self.Files_Ident[IX_XLSX_YEAR]
        self.intMonth    = self.Files_Ident[IX_XLSX_MONTH]
        # Texto = 'Clear Transactions  ' + str(self.intYear)
        # self.Btn_Clear_Db.Set_Text(Texto)

        Full_Transact_Name = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)
        Transact_Name      = Get_File_Name(Full_Transact_Name)
        self.Txt_TransactName.Set_Text(Transact_Name)

        Full_Xlsx_Filename = self.Data.Get_sel_dictionary_value(XLSX_FILENAME)
        self.Xlsx_Filename = Get_File_Name(Full_Xlsx_Filename)
        self.Txt_Xlsx_Name.Set_Text(self.Xlsx_Filename)

        Conto = 'Conto: ' + self.Conto
        self.Txt_Conto.Set_Text(Conto)
        Year = 'Anno: ' + str(self.intYear)
        self.Txt_Xlsx_Year.Set_Text(Year)

        self.Full_Month    = Get_Xlsx_FullMonth(Full_Xlsx_Filename)
        Month = 'Mese: ' + str(self.Full_Month)
        self.Txt_Xlsx_Month.Set_Text(Month)

    # ---------------------------------------------------------------------------------------------------
    def Fill_rows_on_tree(self):
        pass      # on startup only
        # formatted_records = []
        # for rec in self.records_to_insert_list:
        #     form_rec = convert_rcord_toView(self.template, rec)
        #     formatted_records.append(form_rec)
        # self.Frame_Transact.Load_Row_Values(formatted_records)
        # self.set_titles()

    # ---------------------------------------------------------------------------------------------------
    def Load_Tree(self, ListToInsert):
        TotNoCode = self.Data.Get_Total_Rows()[IX_TOT_ROWS_WITHOUT_CODE]
        TotInserted = self.Data.Get_Len_Transact_Table()
        Frame_Title  = "        inserted = " + str(TotInserted) + '      to insert = ' + str(len(ListToInsert))
        Frame_Title += "      without code = " + str(TotNoCode) + "        "
        self.Frame_Transact.Load_Row_Values(ListToInsert)
        self.Frame_Transact.Frame_Title(Frame_Title)

      # -------------------------------------------------------------------------------------------------
    def Frame_Transact_Setup(self):
        Nrows     = 35
        nColToVis = 8
        # Headings  = ['#0', 'row','Conto ','Contab  ','Valuta  ','Description ','Credits  ','Debits  ','Code']
        # Anchor    = ['c',  'c',  'c',     'c',       'c',       'w',           'e',       'e',        'c']
        # Width     = [ 0,    40,   70,      90,        90,        170,           75,        75,         60]
        Headings  = ['#0', 'row','Conto ','Contab  ','Valuta  ','Credits ', 'Debits  ', 'Description  ','Code']
        Anchor    = ['c',  'c',  'c',     'c',       'c',       'w',           'e',       'w',        'c']
        Width     = [ 0,    40,   70,      90,        90,        75,            75,        170,        60]
        Form_List_Rows = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Transact.Tree_Setup(Form_List_Rows)

    # -------------------------------------------------------------------------------------------------
    def Clk_View_Xlsx(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_INS, [])

    # -------------------------------------------------------------------------------------------------
    def Clk_View_Transact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_INS, [])

    # -------------------------------------------------------------------------------------------------------
    def Clk_Verify(self):
        self.Mod_Mngr.Top_Launcher(TOP_TRANSACT_VERIFY, TOP_CODES_MNGR, [])

    # -------------------------------------------------------------------------------------------------
    def Clk_Ontree_View(self, Values):
        pass
    # =================================================================================================




