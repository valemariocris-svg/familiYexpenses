# ---------------------------------------------------------------------------------- #
#               *****     Super_Top_Queries.py     *****                             #
#      the parent of Top_Queries contains:                                           #
#         Combos and Buttons, while the child Top_Queries contains:                  #
#             The Frames for viewing data and relatives clicks                       #
#  the method  Load_All_Data() and  Create_Transact_List_perMonth are overridden     #
#  in the child Top_Queries  that contains the full functionality                    #
#                                                                                    #
# ---------------------------------------------------------------------------------- #

from Top_Expenses.Modules_Manager import Modul_Mngr
from Widgt.Dialogs import *

# =================================================================================================================
class Super_Top_Queries(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data_Manager
        self.Mod_Mngr = Modul_Mngr
        # 1. NASCONDI SUBITO LA FINESTRA PRINCIPALE
        # self.withdraw()  ma mi ciula un file in FIDEU e TRANSACTIONS

        self.Dummy    = 0
        self.geometry('15x15+900+490')
        self.resizable(True, True)
        self.configure(background=BACKGND)
        self.Chat.Attach([self, TOP_QUERY])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
        self.title('    ')

        self.nFrames        = 0
        self.Widgtes_PosX   = []
        self.Widg_PosX      = XY_TO_HIDE
        self.Months_on_Tree = 0
        self.iStart_Month   = 0
        self.iTot_Months    = 0
        self.iEnd_Month     = 0

        # ----- this piece of code is used only once when Selections are not yet created -------------- #
        Transact_Filename = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)                       #
                                                                                                        #
        if Transact_Filename is UNKNOWN:                                                                #
            Msg_Dlg = Message_Dlg(MSG_BOX_INFO, 'Please select a Transactions db file')                 #
            Msg_Dlg.wait_window()                                                                       #
            File_Dlg = File_Dialog(TRANSACT_FILENAME)                                                       #
            Full_Filename = File_Dlg.FileName                                                           #
            if not Full_Filename:                                                                       #
                Msg_Dlg = Message_Dlg(MSG_BOX_ERR, 'queries are impossible')                           #
                Msg_Dlg.wait_window()                                                                   #
                self.Call_OnClose()                                                                     #
            else:                                                                                       #
                self.Data.Update_key_dictionary(TRANSACT_FILENAME, Full_Filename)
                self.Setup_Year_Conto_Month_Tot_Date()                                                  #
        # --------------------------------------------------------------------------------------------- #

        self.OneYear_Transact_List = self.Data.Get_Transact_Table()

        # This list is created on startup or at each Selection
        # based on Year, Conto (ValDate/AccDate) TR GR CA for each month
        self.Transact_xMonth_List = [[]] * 12
        self.Tot_Transact_xMonth  = [0]  * 12
        self.DateCount_PerMonth   = [0]  * 12

        # [Credits, Debits]  for   Frame1, Frame2, Frame3
        self.Tot_CredDeb_xTree  = [[0, 0], [0, 0], [0, 0]]

        self.Transact_Years_List = []  # The years of transactions contained on TRANSATCION directory
        self.Tot_List    = [ONE_MONTH,TWO_MONTHS,FOUR_MONTHS,SIX_MONTHS,TWELVE_MONTHS]
        self.Date_List   = [VAL_DATE, CONTAB_DATE]
        self.Files_Ident = []   # self.Data.Get_Full_Xlsx_Transact_Ident()

        self.iYear_Selected = 0
        self.Conto_Selected = ''
        self.Month_Selected = ''
        self.Tot_MonSelected= ''
        self.Date_Selected  = ''  # default is Valuta, can be changed through OptMenu_Date
        self.TRselected     = ALL_CODES
        self.GRselected     = ALL_GROUPS
        self.CAselected     = ALL_CAT
        self.Excl_Selected  = EXTRAORD_EXCL

        self.Total_Rows  = 0    # Total rows of selected Transactions
        self.TR_List     = []   # Codes on Year Transactions Table
        self.GR_List     = []   # same per GR
        self.CA_List     = []   # same per CA

        # ------------------    C O M B O s       ---------------------------------------------------
        self.StrVar_Year = tk.StringVar()
        self.OptMenu_Year = TheCombo(self, self.StrVar_Year, self.Widg_PosX, 20, 15, 16, [2026, 2025, 2924],
                                     str(self.iYear_Selected), self.Clk_ComboYear)

        self.StrVar_Conto  = tk.StringVar()
        self.OptMenu_Conto = TheCombo(self, self.StrVar_Conto, self.Widg_PosX, 55, 15, 16, CONTO_LIST,
                                      FIDEU, self.Clk_Conto)

        self.StrVar_Start  = tk.StringVar()
        self.OptMenu_Start = TheCombo(self, self.StrVar_Start, self.Widg_PosX, 90, 21, 16,  MONTHS_NAMES,
                                      JAN, self.Clk_Month)

        self.StrVar_Tot   = tk.StringVar()
        self.OptMenu_Tot  = TheCombo(self,  self.StrVar_Tot,   self.Widg_PosX, 125, 21, 16,  self.Tot_List,
                                     ONE_MONTH, self.Clk_Tot)

        self.StrVar_Date  = tk.StringVar()
        self.OptMenu_Date = TheCombo(self,  self.StrVar_Date,  self.Widg_PosX, 160, 21, 16,  self.Date_List,
                                     self.Date_Selected , self.Clk_Date)

        self.StrVar_TR  = tk.StringVar
        self.OptMenu_TR = TheCombo(self, self.StrVar_TR,      self.Widg_PosX, 210, 41, 16, self.TR_List,
                                    '', self.Clk_TRsel)
        self.StrVar_GR  = tk.StringVar
        self.OptMenu_GR = TheCombo(self, self.StrVar_GR,     self.Widg_PosX,  245, 41, 16,  self.GR_List,
                                   '', self.Clk_GRsel)
        self.StrVar_CA  = tk.StringVar
        self.OptMenu_CA = TheCombo(self,  self.StrVar_CA,    self.Widg_PosX,  280, 21, 16,  self.CA_List,
                                   '', self.Clk_CAsel)
        self.Excl_List   = [EXTRAORD_EXCL, EXTRAORD_INCL]
        self.Str_Exclude = tk.StringVar
        self.OptExclude  = TheCombo(self,  self.Str_Exclude, self.Widg_PosX,  315, 21, 16,  self.Excl_List,
                                   '', self.Clk_Excl)
        self.Extraord_Text = TheText(self,TXT_DIS_BLACK, self.Widg_PosX, 355, 18, 1, "straord = 16")

        # ---------------------------------    Buttons   ----------------------------------------------------------
        # Remenber:   self.Set_Widgets_PosX()    for Buttons etc. positioning
        self.Btn_DB_View = TheButton(self, BTN_DEF_EN,self.Widg_PosX,550,15, 'Mostra i movimenti',self.Clk_ViewTransact)
        self.Btn_Check   = TheButton(self, BTN_DEF_EN,self.Widg_PosX,590,15, 'Chek xlsx / movim.',self.Clk_Check)
        self.Btn_xlsx_View = TheButton(self,BTN_DEF_EN,self.Widg_PosX,510,15, 'Mostra file Xlsx', self.Clk_XlsxView)
        self.Btn_Exit      = TheButton(self,BTN_BOL_EN,self.Widg_PosX,936,13, '  E S C I  ',      self.Call_OnClose)

        # self.deiconify()
        self.Set_All_Select()
        pass

    # ----- This  function  is  overridden on Top_Queries  ---------------- #
    def Load_All_Data(self):                                                #
        pass                                                                #
    # --------------------------------------------------------------------- #


    # ------ Fill Combos List   and previous selections saved on  Files_Names  ------------------------------
    def Set_All_Selections(self):
        TRdescr_List = []
        GR_List      = []
        CA_List      = []
        self.TR_List = []   # only descriptions
        self.GR_List = []   # only descriptions
        self.CA_List = []   # only descriptions
        for Rec in self.OneYear_Transact_List:
            TRcode = int(Rec[IX_TRANSACT_TR_CODE])
            TRdescr = self.Data.Get_TrDesc_FromCode(TRcode)
            if TRdescr not in TRdescr_List:
                TRdescr_List.append(TRdescr)
                pass
        try:
            TRdescr_List.sort()
        except Exception as e:
            PRINT('Error sorting TRdescr_List\n' + str(e))
            pass
        finally:
            pass

        for TRdesc in TRdescr_List:      # List of codes groups categories used in transactions
            GRCAdesc = self.Data.Get_GR_CA_desc_From_TRdesc(TRdesc)
            GRdesc = GRCAdesc[0]
            CAdesc = GRCAdesc[1]
            if GRdesc not in GR_List:
                GR_List.append(GRdesc)
            if CAdesc not in CA_List:
                CA_List.append(CAdesc)
        GR_List.sort()
        CA_List.sort()

        self.TR_List = [ALL_CODES]          # Put All Transac
        for Item in TRdescr_List:
            self.TR_List.append(Item)

        self.GR_List = [ALL_GROUPS]
        for Item in GR_List:
            self.GR_List.append(Item)

        self.CA_List = [ALL_CAT]
        for Item in CA_List:
            self.CA_List.append(Item)
        self.Setup_Year_Conto_Month_Tot_Date()
        pass

    # -------------------------------------------------------------------------------------------------------------
    def Setup_Year_Conto_Month_Tot_Date(self):
        Transact_Filename = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)
        Years_List = Get_Transactions_Years(Transact_Filename)

        self.OptMenu_Year.SetValues(Years_List)
        self.iYear_Selected = Get_Transactions_Year(Transact_Filename)
        pass

        self.Conto_Selected = self.Data.Get_sel_dictionary_value(QUERY_CONTO)
        self.Month_Selected = self.Data.Get_sel_dictionary_value(QUERY_START_MONTH)
        self.Tot_MonSelected= self.Data.Get_sel_dictionary_value(QUERY_TOT_MONTHS)
        self.Date_Selected  = self.Data.Get_sel_dictionary_value(QUERY_VAL_CONT_DATE)
        self.TRselected     = self.Data.Get_sel_dictionary_value(QUERY_CODE_SEL)
        self.GRselected     = self.Data.Get_sel_dictionary_value(QUERY_GROUP_SEL)
        self.CAselected     = self.Data.Get_sel_dictionary_value(QUERY_CATEGORY_SEL)

    # -------------------------------------------------------------------------------------------------------------
    def Setup_TR_GR_CA_OptMenu(self):
        self.OptMenu_TR.SetValues([ALL_CODES, SELTR])
        self.OptMenu_GR.SetValues(self.GR_List)
        self.OptMenu_CA.SetValues(self.CA_List)
        self.OptExclude.SetValues(self.Excl_List)

        self.OptMenu_TR.SetSelText(self.TRselected)
        self.OptMenu_GR.SetSelText(self.GRselected)
        self.OptMenu_CA.SetSelText(self.CAselected)
        self.OptExclude.SetSelText(self.Excl_Selected)

    # -------------------------------------------------------------------------------------------------------------
    def Update_Sel_onTxt(self):

        self.Data.Update_key_dictionary(QUERY_CONTO, self.Conto_Selected)
        self.Data.Update_key_dictionary(QUERY_START_MONTH, self.Month_Selected)
        self.Data.Update_key_dictionary(QUERY_TOT_MONTHS, self.Tot_MonSelected)
        self.Data.Update_key_dictionary(QUERY_VAL_CONT_DATE, self.Date_Selected)

        self.Data.Update_key_dictionary(QUERY_CODE_SEL, self.TRselected)
        self.Data.Update_key_dictionary(QUERY_GROUP_SEL, self.GRselected)
        self.Data.Update_key_dictionary(QUERY_CATEGORY_SEL, self.CAselected)

        self.Chat.Tx_Request([TOP_QUERY, [MAIN_WIND], VIEW_SELECTIONS, []])

    # -------------------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_QUERY)
        self.destroy()

    # -------------------------------------------------------------------------------------------------------------
    def Set_OnTxt_TR_GR_Sel(self):
        self.Data.Update_key_dictionary(QUERY_CODE_SEL, self.TRselected)
        self.Data.Update_key_dictionary(QUERY_GROUP_SEL, self.GRselected)
        self.Data.Update_key_dictionary(QUERY_CATEGORY_SEL, self.CAselected)

        self.Chat.Tx_Request([TOP_QUERY, [MAIN_WIND], VIEW_SELECTIONS, []])

    # -------------------------------------------------------------------------------------------------------------
    def Set_All_Select(self):
        self.TRselected = ALL_CODES                 # IMPORTANT for setups inside the module
        self.OptMenu_TR.SetSelText(ALL_CODES)
        self.GRselected = ALL_GROUPS
        self.OptMenu_GR.SetSelText(ALL_GROUPS)
        self.CAselected = ALL_CAT
        self.OptMenu_CA.SetSelText(ALL_CAT)
        self.Excl_Selected = EXTRAORD_EXCL
        self.OptExclude.SetSelText(EXTRAORD_EXCL)
        self.Set_OnTxt_TR_GR_Sel()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_ComboYear(self, Value):
        self.Dummy = 0
        newTransact_Filename = 'Transact_' + Value + '.db'
        Dir_Name = Get_Dir_Name(self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME))
        Full_Filename = Dir_Name + newTransact_Filename

        if not Gl_Cek_Transactions_Name(Full_Filename):
            self.OptMenu_Year.SetValues(str(self.iYear_Selected))
            return
        self.Update_Sel_onTxt()
        self.Set_All_Select()

        self.Data.Update_key_dictionary(QUERY_CODE_SEL, self.TRselected)

        self.Chat.Tx_Request([TOP_QUERY, [MAIN_WIND], VIEW_SELECTIONS, []])
        #
        if self.Mod_Mngr.Load_Transact_Mngr(TOP_QUERY):
            transact_filename = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)
            Reply = self.Data.Load_Transact_Table(transact_filename)
            if Reply == OK:
                self.OneYear_Transact_List = self.Data.Get_Transact_Table()
                self.Load_All_Data()
            else:
                self.Call_OnClose()
                pass
            # self.OneYear_Transact_List = self.Data.Get_Transact_Table()
            # self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Conto(self, Value):
        self.Conto_Selected = Value
        self.Update_Sel_onTxt()
        self.Load_All_Data()
        self.Set_All_Select()

    def Clk_Month(self, Value):
        self.Month_Selected = Value
        self.Tot_List       = QUERIES_TOT_DICT[self.Month_Selected]
        self.OptMenu_Tot.SetValues(self.Tot_List)
        self.OptMenu_Tot.SetSelText(self.Tot_MonSelected[0])
        self.Update_Sel_onTxt()
        self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Tot(self, Value):
        self.Tot_MonSelected = Value
        self.Tot_List = QUERIES_TOT_DICT[self.Month_Selected]
        self.Update_Sel_onTxt()
        self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Date(self, Value):
        self.Date_Selected = Value
        self.Update_Sel_onTxt()
        self.Load_All_Data()
        self.Set_All_Select()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_TRsel(self, Value):
        if Value == ALLTR:
            self.Set_All_Select()
            self.Chat.Tx_Request([TOP_QUERY, [TOP_CODES_VIEW], CODE_TO_CLOSE, []])
        else:
            self.TRselected = ''
            self.GRselected = ''
            self.CAselected = ''
            TRlist = self.TR_List.copy()
            TRlist[0] = VIEW_QUERY_REDUC
            # Top_View_Codes(TRlist)
            self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW, [TOP_CODES_MNGR], TRlist)
        self.Update_Sel_onTxt()
        self.Load_All_Data()

    # ------------  see above  ------------------------
    # called from TOP_CODES_VIEW on click on tree
    def TRcode_Selected_OnTopView(self, RecValues):
        TRcode = RecValues[IX_TR_FULL_TR_CODE]
        self.TRselected = self.Data.Get_TrDesc_FromCode(TRcode)
        self.GRselected = ''
        self.CAselected = ''
        self.Update_Sel_onTxt()
        self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_GRsel(self, Value):
        if Value == ALL_GROUPS:
            self.Set_All_Select()
        else:
            self.GRselected = Value
            self.TRselected = ''
            self.CAselected = ''
            self.Update_Sel_onTxt()
        self.Load_All_Data()

    def Clk_CAsel(self, Value):
        if Value == ALL_CAT:
            self.Set_All_Select()
        else:
            self.CAselected = Value
            self.TRselected = ''
            self.GRselected = ''
            self.Update_Sel_onTxt()
        self.Load_All_Data()

    def Clk_Excl(self, Value):
        self.Excl_Selected = Value
        self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_ViewTransact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_QUERY, [])

    # -------------------------------------------------------------------------------------------------------------
    def Clk_XlsxView(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_QUERY, [])

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Summaries(self):
        pass

    # -------------------------------------------------------------------------------------------------------------
    def Convert_To_Float(self, Value):      # exists also in Common_Functions
        self.Dummy = 0
        flVal      = Value
        Type = type(Value)
        if Type is str or Type is None:
            return 0.00
        if type(Value) is int:
            flVal = float(Value)
        return flVal

    # -------------------------------------------------------------------------------------------------
    def Get_Credit_Debit(self, Rec):
        self.Dummy = 0
        Credit = Convert_Str_To_Float(Rec[2])
        Debit  = Convert_Str_To_Float(Rec[3])
        return [Credit, Debit]

    # ------------------------------------------------------------------------------------------------------------
    # Rec Query_View_List    : Conto Contab Valuta  TR_Desc   Accred    Addeb
    # return                  [fl, fl str, str]
    def Query_List_Setup(self, Rec):
        self.Dummy = 0
        Credit     = Rec[IX_QUERY_ACCRED]         # can be  float or '' or ' '
        Debit      = Rec[IX_QUERY_ADDEB]

        floatCredit = Convert_Str_To_Float(Credit)
        floatDebit  = Convert_Str_To_Float(Debit)

        strCredit   = Float_ToString_Setup(floatCredit)
        strDebit    = Float_ToString_Setup(floatDebit)
        CreditDebit_List = [floatCredit, floatDebit, strCredit, strDebit]
        Rec_Queries_List = [Rec[IX_QUERY_CONTO], Rec[IX_QUERY_CONTAB], Rec[IX_QUERY_VALUTA], Rec[IX_QUERY_DESCR],
                            strCredit, strDebit, Rec[IX_QUERY_IDENT]]
        return [Rec_Queries_List, CreditDebit_List]

    # -----------------------------------------------------------------------------------------------------------
    def Clk_Check(self):
        self.Mod_Mngr.Top_Launcher(TOP_TRANSACT_VERIFY, TOP_QUERY, [])

    # ----------------------------------------------------------------------------------------------------------
    def Set_Tot_Transact_xMonth(self):
        for Index in range(0, 12):
            List_xMonth = self.Transact_xMonth_List[Index]
            self.Tot_Transact_xMonth[Index] = len(List_xMonth)
            pass


# =================================================================================================================