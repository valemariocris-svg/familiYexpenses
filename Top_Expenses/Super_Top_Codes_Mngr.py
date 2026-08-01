# ---------------------------------------------------------------------------------- #
#            *****     Super_Top_Codes_Mngr.py     *****                             #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
from Top_Expenses.Modules_Manager import Modul_Mngr
from Widgt.Widgets import *
from Widgt.Tree_Widg import *
from Widgt.Canvas_Frame import *
from Widgt.Dialogs import *

# -------------------------------------------------------------------------------------------------------------
class Super_Top_Mngr(tk.Toplevel):
    def __init__(self, Child_ClkNoCode, Child_ClkWithCode):
        super().__init__()
        self.Chat          = Ms_Chat
        self.Data          = Data_Manager
        self.Mod_Mngr      = Modul_Mngr
        self.Chat.Attach([self, TOP_CODES_MNGR])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry('5x5+10000+10000')
        self.title('*****     Transactions  Codes  Manager     *****')
        self.configure(background=BACKGND)

        self.dummy       = 0
        self.TR_Code     = None
        self.GR_Code     = None
        self.CA_Code     = None
        self.TR_Desc     = None
        self.GR_Desc     = None
        self.CA_Desc     = None
        self.FullDesc    = None

        self.Child_ClkNoCode   = Child_ClkNoCode
        self.Child_ClkWithCode = Child_ClkWithCode
        self.FullDesc_OnClick_NoCode   = ""
        self.FullDesc_OnClick_WithCode = ""
        self.View_Without_Code = True
        self.noCode_rows_to_be_inserted_list = []    # with full_date as in NoCodes_list (Xlsx_Mngr)
        self.Row_WithoutCode                 = None  # it is the Row clicked on Frame_NoCodes

        # ----------------------   Frames   -------------------------------------------------------------------
        self.Frame_NoCodes_ToIns = TheFrame(self,   10, 20, self.Clk_OnTree_NoCodes)
        self.Frame_NoCodes_ToIns_Set()
        self.Frame_WithCodes_ToIns = TheFrame(self, 10, 20, self.Clk_OnTree_WithCodes)
        self.Frame_WithCodes_ToIns_Set()

        # ***************************     C A N V A  S    *****************************************************
        self.Canv_CodData = CreateCanvas(self, 10, 640, 380, 130)
        TheLable(self.Canv_CodData, LAB_BLUE, 60, 1, 26, "impostazioni dati per il codice")

        # --------------------------------   Groups    C O M B O            -----------------------------------
        self.StrVar    = tk.StringVar()
        self.GR_Combo  = TheCombo(self.Canv_CodData, self.StrVar, XY_TO_HIDE, XY_TO_HIDE, 1, 1, [], '', self.Clk_Combo)

        # ------------  TEXT Boxes   and   Btn_SelCode  used  on  Child  --------------------------------------
        self.Txt_StrFullDesc1 = TheText(self,              TXT_ENAB,      10, 583,  95, 2, '')   # not in canvas
        self.Txt_StrToFind1   = TheText(self.Canv_CodData, TXT_ENAB,      20, 30,   40, 1, STRTOFIND)
        self.Txt_TR_Code1     = TheText(self.Canv_CodData, TXT_DIS_BLACK, 20, 65,    5, 1, '0')
        self.Txt_TR_Desc1     = TheText(self.Canv_CodData, TXT_ENAB,      82, 65,   33, 1, TRDESC)
        #
        self.Txt_GR_Code1     = TheText(self.Canv_CodData, TXT_DIS_BLACK,  20, 100,  5, 1, '0')
        self.Txt_CA_Code1     = TheText(self.Canv_CodData, TXT_DIS_BLACK,  20, 134,  5, 1, '0')
        self.Txt_CAdesc1      = TheText(self.Canv_CodData, TXT_DIS_BLACK,  82, 134, 33, 1, CATDESC)

    # ---------------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Tx_Request([TOP_CODES_MNGR, [ANY], CODE_TO_CLOSE, []])
        self.Chat.Detach(TOP_CODES_MNGR)
        self.destroy()

    # ==========================  T R E E     Without  Codes   ========================================
    def Frame_NoCodes_ToIns_Set(self):
        Nrows     = 25
        nColToVis = 0   # no more used
        Headings  = ['#0', 'Row', 'Conto', 'Contab', 'Valuta  ', 'Accred  ', 'Addeb  ', 'Descrizione completa']
        Anchor    = ['c',   'w',    'c',   'c',      'c',        'e',         'e',       'w']
        Width     = [0,      70,     50,    90,       90,         80,          80,       380]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        result = self.Frame_NoCodes_ToIns.Tree_Setup(Form_List)
        self.View_frames_error(result)

    # -------------------------------------------------------------------------------------------------
    def Clk_OnTree_NoCodes(self, Values):
        #    0      1       2       3       4      5      6
        #  [nRow, Conto, Contab, Valuta, Accred, Addeb, FullDes
        Row       = int(Values[IX_NO_CODE_NROW])
        Conto     = Values[IX_NO_CODE_CONTO]
        Contabile, Valuta  = self.get_full_datetime(Values)
        FullDesc  = Values[IX_NO_CODE_FULL_DESCR]
        self.Txt_StrFullDesc1.Set_Text(Values[IX_NO_CODE_CONTAB] + '  - ' + FullDesc)

        flAccred  = Convert_It_string_to_float(Values[IX_NO_CODE_ACCRED])
        flAddeb   = Convert_It_string_to_float(Values[IX_NO_CODE_ADDEB])
        intValues = [Row, Conto, Contabile, Valuta, flAccred, flAddeb, FullDesc]

        self.Row_WithoutCode = intValues
        self.Frame_WithCodes_ToIns.Clear_Focus()
        self.FullDesc_OnClick_NoCode = Values[IX_NO_CODE_FULL_DESCR]
        self.Child_ClkNoCode()

    # ==========================  T R E E     With  Codes   ===========================================
    def Frame_WithCodes_ToIns_Set(self):
        self.Frame_WithCodes_ToIns.Frame_Title('  ')
        Nrows     = 25
        nColToVis = 0   # no more used
        Headings = ['#0',  'Row ', 'Conto', 'Contab ', 'Valuta ', 'Accred  ', 'Addeb  ', 'Descrizione ', 'Codice ', 'Full']
        Anchor   = ['c',   'w',     'c',    'c',       'c',       'e',         'e',       'w',           'c',       'w']
        Width    = [ 0,     70,      50,     90,        90,        80,          80,        210,           100,       50 ]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        result = self.Frame_WithCodes_ToIns.Tree_Setup(Form_List)
        self.View_frames_error(result)

    # -------------------------------------------------------------------------------------------------
    def Clk_OnTree_WithCodes(self, Values):
        #  Row    Date   Descrip   Accred   Addeb   TR_Code
        nRow     = int(Values[IX_WITH_CODE_NROW])
        TRcode  = int(Values[IX_WITH_CODE_TR_CODE])
        Descrip  = Values[IX_WITH_CODE_TR_DESCR]
        self.Frame_NoCodes_ToIns.Clear_Focus()
        if int(nRow) < 1 or not Descrip:
            return
        self.Frame_NoCodes_ToIns.Clear_Focus()
        self.View_Descr_Text(TRcode)

        self.Frame_NoCodes_ToIns.Clear_Focus()
        self.FullDesc_OnClick_WithCode = Values[IX_WITH_CODE_FULL_DESCR]
        self.Child_ClkWithCode()

    # -------------------------------------------------------------------------------------------------
    def View_Frames(self, Total_WthoutCode):
        if Total_WthoutCode == 0:               # 0 No Rows Without codes
            self.View_Without_Code = False
            self.Frame_WithCodes_ToIns.Frame_View()
            self.Frame_NoCodes_ToIns.Frame_Hide()
        elif Total_WthoutCode > 0:              # some Rows Without codes
            self.View_Without_Code = True
            self.Frame_WithCodes_ToIns.Frame_Hide()
            self.Frame_NoCodes_ToIns.Frame_View()
        elif Total_WthoutCode < 0:              # -1 view frames as selected
            if self.View_Without_Code:
                self.Frame_WithCodes_ToIns.Frame_Hide()
                self.Frame_NoCodes_ToIns.Frame_View()
                self.Frame_NoCodes_ToIns.Clear_Focus()
            else:
                self.Frame_WithCodes_ToIns.Frame_View()
                self.Frame_NoCodes_ToIns.Frame_Hide()
                self.Frame_WithCodes_ToIns.Clear_Focus()

    # -------------------------------------------------------------------------------------------------
    def Frames_Refresh(self):
        if not self.Mod_Mngr.Initialize_codes_xlsx_transact(TOP_CODES_MNGR):
            return
        self.Load_Trees()
        self.View_Frames(-1)

    # -------------------------------------------------------------------------------------------------
    # self.all_rows_inserted_list            = []
    # self.std_code_rows_to_be_insertd_list  = []
    # self.noCode_rows_to_be_inserted_list   = []
    # -------------------------------------------------------------------------------------------------
    def Load_Trees(self):
        self.Mod_Mngr.check_xlsx_transact_filenames_load_transact_create_rows_to_ins_list(TOP_CODES_MNGR)
        self.noCode_rows_to_be_inserted_list = self.Data.get_noCode_rows_to_be_inserted_list()
        len_NoCode_to_be_inserted      = len(self.noCode_rows_to_be_inserted_list)
        std_cod_to_be_inserted         = self.Data.get_std_code_rows_to_be_insertd_list()
        len_tot_std_cod_to_be_inserted = len(std_cod_to_be_inserted)
        inserted_len                   = self.Data.get_tot_rows_inserted()

        NoCodeStr   = f"righe da ins.senza codice = {str(len_NoCode_to_be_inserted)}"
        WithCodeStr = f"righe da ins. con codice std = {str(len_tot_std_cod_to_be_inserted)}"
        Inserted    = f"tot righe inserite = {str(inserted_len)}"

        TitleNoCode = f"     {NoCodeStr}         {WithCodeStr}         {Inserted}     "
        TitleWith   = f"     {WithCodeStr}         {NoCodeStr}         {Inserted}     "

        self.Frame_NoCodes_ToIns.Frame_Title(TitleNoCode)
        self.Frame_WithCodes_ToIns.Frame_Title(TitleWith)

        # Wihtout_Code_Tree_List     nRow Conto Contabile Valuta Accred Addeb FullDesc
        noCode_rows_to_view_list = []
        template = [INT_TOSTRING, SIC, DMY, DMY, FLOAT_TOSTR, FLOAT_TOSTR, SIC]
        for row in self.noCode_rows_to_be_inserted_list:
            row_to_view = convert_row_for_View_xlsx(template, row)
            noCode_rows_to_view_list.append(row_to_view)
        result = self.Frame_NoCodes_ToIns.Load_Row_Values(noCode_rows_to_view_list)
        self.View_frames_error(result)

        # With_Code_Tree_List  nRow Conto Contabile _Valuta Accred _Addeb TRdesc TRcode
        witCode_rows_to_view_list = []
        template = [INT_TOSTRING, SIC, COMPC_YMD, COMPC_YMD, FLOAT_TOSTR, FLOAT_TOSTR, SIC, INT_TOSTRING, SIC]
        for row in std_cod_to_be_inserted:
            row_to_view = convert_record_for_View_transact(template, row)
            witCode_rows_to_view_list.append(row_to_view)
        result = self.Frame_WithCodes_ToIns.Load_Row_Values(witCode_rows_to_view_list)
        self.View_frames_error(result)

        self.View_Frames(len_NoCode_to_be_inserted)

    # -------------------------------------------------------------------------------------------------
    def Clk_Combo(self, GRdesc):
        GRrec = Get_List_Record(self.Data.Get_GR_Codes_Table(), IX_GR_GR_DESC, GRdesc, [])
        if not GRrec:
            return
        CAcode = GRrec[IX_GR_CA_CODE]
        CArec = Get_List_Record(self.Data.Get_CA_Codes_Table(), IX_CA_CA_CODE, CAcode, -1)
        if not CArec:
            return
        self.Txt_GR_Code1.Set_Text(GRrec[IX_GR_GR_CODE])
        self.Txt_CA_Code1.Set_Text(CArec[IX_CA_CA_CODE])
        self.Txt_CAdesc1.Set_Text(CArec[IX_CA_CA_DESC])
        self.Txt_CAdesc1.Set_Text(CArec[IX_CA_CA_DESC])

    # -------------------------------------------------------------------------------------------------
    def View_Descr_Text(self, TRcode):
        TR_Full_Code = self.Data.Get_TR_Codes_Full(TRcode)
        self.Txt_TR_Code1.Set_Text(TRcode)
        self.Txt_GR_Code1.Set_Text(TR_Full_Code[IX_TR_FULL_GR_CODE])
        self.Txt_CA_Code1.Set_Text(TR_Full_Code[IX_TR_FULL_CA_CODE])
        self.Txt_TR_Desc1.Set_Text(TR_Full_Code[IX_TR_FULL_TR_DESC])
        self.Txt_StrToFind1.Set_Text(TR_Full_Code[IX_TR_FULL_STR_TO_FIND])
        self.Txt_CA_Code1.Set_Text(TR_Full_Code[IX_TR_FULL_CA_CODE])
        self.Txt_CAdesc1.Set_Text(TR_Full_Code[IX_TR_FULL_CA_DESC])
        #
        GRdesc = TR_Full_Code[IX_TR_FULL_GR_DESC]
        self.GR_Combo.SetSelText(GRdesc)

    # -------------------------------------------------------------------------------------------------
    def Clear_Text_Widg(self, Full):
        if Full:
            self.Txt_StrFullDesc1.Set_Text('')
        self.Txt_StrToFind1.Set_Text(STRTOFIND)
        self.Txt_TR_Desc1.Set_Text(TRDESC)
        self.Txt_CAdesc1.Set_Text(CATDESC)

        self.Txt_TR_Code1.Set_Text('0')
        self.Txt_GR_Code1.Set_Text('0')
        self.Txt_CA_Code1.Set_Text('0')

        self.Txt_TR_Code1.Set_Text('0')
        self.Txt_GR_Code1.Set_Text('0')
        self.Txt_CA_Code1.Set_Text('0')

        self.GR_Combo.SetSelText(GROUPSEL)
        pass

    # -----------------------------------------------------------------------------------------------
    def View_frames_error(self, error):
        self.dummy = 0
        if not error:
            return
        msg_dlg = Message_Dlg(MSG_BOX_ERR, error)
        msg_dlg.wait_window()
        pass

    # ---------------------------------------------------------------------------------------------
    def get_full_datetime(self, Values):
        nRow = int(Values[IX_NO_CODE_NROW])
        for row in self.noCode_rows_to_be_inserted_list:
            if nRow == row[IX_NO_CODE_NROW]:
                pass
                full_contab = get_Y_M_D_H_m_S_for_insert(row[IX_NO_CODE_CONTAB])
                full_valuta = get_Y_M_D_H_m_S_for_insert(row[IX_NO_CODE_VALUTA])
                return full_contab, full_valuta
        pass
        return '???-??-??', '???-??-??'

# =================================================================================================
