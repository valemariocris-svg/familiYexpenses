# ================================================================================= #
#                  *****     Top_View_Transact.py     *****                         #
# XLS_Row_List : nRow  Contab  Valuta  Descr1  Accred  Addeb  Descr2                #
# ================================================================================= #

# from Common.Common_Functions import *
# from Chat import Ms_Chat
# from Data_Classes.Transact_DB import Data_Manager
#
# from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import *
from Top_Expenses.Modules_Manager import Modul_Mngr
# from Widgt.Widgets import TheButton, TheText, TheCombo
from Widgt.Dialogs import *

# ===================================================================================
class Top_View_Transact(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.Chat      = Ms_Chat
        self.Data      = Data_Manager
        self.Mod_Mngr  = Modul_Mngr
        self.Data_List = List

        self.Chat.Attach([self, TOP_VIEW_TRANSACT])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(True, True)
        self.geometry('10x10+10000+10000')
        self.title('***   View transactions database  *** ')
        self.configure(background=BACKGND)

        self.Txt_dateContab = TheText(self, TXT_DISAB,    10, 870,  21, 1, '')
        self.Txt_dateValuta = TheText(self, TXT_DISAB,    10, 905,  21, 1, '')
        self.Txt_FullDesc   = TheText(self, TXT_DISAB,    220, 870, 95, 3, '')
        self.Txt_Code       = TheText(self, TXT_DISAB,     10, 950,  13, 1, '')
        self.Txt_TrDesc     = TheText(self, TXT_DISAB,    220, 950, 28, 1, '')

        self.View_Transact_mode = self.Data.Get_sel_dictionary_value(TRANSACT_VIEW_MODE)
        self.StrVar_List        = tk.StringVar
        self.Combo_sel = TheCombo(self,  self.StrVar_List, 500, 950, 300, 28,
                                     TRANSACT_VIEW_SEL,  self.View_Transact_mode, self.Clk_ListSel)
        self.Btn_Exit = TheButton(self, BTN_DEF_EN, 910, 950, 18, '  E S C I  ', self.Call_OnClose)

        self.Transact_Record   = None
        self.TR_Code           = 0
        self.TRdesc            = ''

        self.All_Transact_as_is= []
        self.All_TR_Contab_ASC = []
        self.TR_Normal_Code    = []
        self.TR_Generic_Code   = []
        self.Frame_Totals_OK   = False

        # --------------------------   Create Total rows   ------------------------------------
        self.Frame_Totals = TheFrame(self, 10, 20, self.Clk_On_Transaction)
        if not self.Frame_Totals_Setup():
            self.Frame_Totals_OK = False
        else:
            self.Frame_Totals.Frame_View()
            self.Frame_Totals_OK = True
        Title  = "         ----------     confronto  tra  totale movimenti nel Db    e    totale righe in xlsx     ----------         "
        self.Frame_Totals.Frame_Title(Title)
        if not self.Frame_Totals_Load():
            # A) Nascondi immediatamente la finestra per non farla vedere monca
            # self.withdraw()
            # B) Pianifica la distruzione appena l'__init__ ha terminato
            self.after(0, self.Call_OnClose)
            return
        self.geometry(TOP_TR_VIEW_GEOMETRY)

        # --------------------------   Create Transactions records   --------------------------
        self.Frame_Transactions  = TheFrame(self, 10, 130, self.Clk_On_Transaction)
        self.Frame_Transactions_Setup()
        self.Frame_Transactions.Frame_View()
        self.Frame_Transactifons_Load()
        self.Transact_Id_Selcted = None

    # ---------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_VIEW_TRANSACT)
        self.destroy()

    # ---------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:           # Close
            self.Call_OnClose()

    # ---------------------------------------------------------------------------------------------
    def Clear_Sel_Updt_Btn(self):
        self.Txt_Code.Clear_Text()

    # ---------------------------------------------------------------------------------------------
    def Clk_ListSel(self, Value):
        self.View_Transact_mode = Value
        self.Frame_Transactifons_Load()
        self.Transact_Id_Selcted = None

    # ---------------------------------------------------------------------------------------------
    def Frame_Totals_Load(self):
        if not self.Frame_Totals_OK:
            return False
        if self.View_Transact_mode == FIDEU:
            Conto = FIDEU
        elif self.View_Transact_mode == FLASH:
            Conto = FLASH
        else:
            Conto = FIDFLH
        List   = self.Data.get_totals_dict_as_list(Conto)
        result = self.Frame_Totals.Load_Row_Values(List)
        if result != '':
            msg_dlg = Message_Dlg(MSG_BOX_ERR, result)
            msg_dlg.wait_window()
            return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Frame_Transactifons_Load(self):
        TR_Name = Get_File_Name(self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME))
        if self.View_Transact_mode == TRANSACT_VIEW_ALL:
             Title = '     movimenti come in Db'
             List = self.Data.Get_Transact_recs_asis()

        elif self.View_Transact_mode == TRANSACT_VIEW_CONTAB_ASC:
             Title = '     movimenti ordinato-i per contabile'
             List = self.Data.Get_Transact_recs_ordered()

        elif self.View_Transact_mode == TRANSACT_VIEW_STANDARD_CODE:
             Title = '     movimenti con codice normale'
             List  = self.Data.Get_Transact_NormalCode_List()

        elif self.View_Transact_mode == FIDEU:
             Title = f"  movimenti per conto {FIDEU} "
             status, data  = self.Data.Get_transactions_per_conto(FIDEU)
             if not status:
                 return
             List = data

        elif self.View_Transact_mode == FLASH:
             Title = f"  movimenti per conto {FLASH} "
             status, data  = self.Data.Get_transactions_per_conto(FLASH)
             if not status:
                 return
             List = data

        else:
            Title = ''
            List  = self.Data.Get_Transact_GenericCode_List()
        self.Data.Update_key_dictionary(TRANSACT_VIEW_MODE, self.View_Transact_mode)
        #
        FrameText = ('      ' + TR_Name + '     ' + str(len(List)) + str(Title))
        # -------------------------------------------------------------------------------------------------
        #   (auto)  Id, riga, conto, contab, valuta, accred, addeb, TRdesc, TRcode, full_desc
        template = [INT_TOSTRING, INT_TOSTRING, SIC, YMD, YMD, FLOAT_TOSTR, FLOAT_TOSTR, SIC, INT_TOSTRING, SIC]

        view_list = []
        for Rec in List:
            rec_toView = convert_rcord_toView(template, Rec)
            view_list.append(rec_toView)
        #
        self.Frame_Transactions.Frame_Title(FrameText)
        self.Frame_Transactions.Load_Row_Values(view_list)

    # ---------------------------------------------------------------------------------------------
    def Clk_On_Transaction(self, Values):
        Id = 0  #int(Values[IX_TRANSACT_IDENT])
        status, data = self.Data.Get_transact_rec_from_id(Id)
        if not status:
            return
        if not data:
            return
        record = data

        self.Transact_Id_Selcted = record[0]
        self.Txt_dateContab.Set_Text(record[IX_ROW_TOINS_VALUTA])
        self.Txt_dateValuta.Set_Text(record[IX_ROW_TOINS_VALUTA])
        FullDesc = record[IX_TRANSACT_FULL_DESC]
        self.Txt_FullDesc.Set_Text(FullDesc)
        self.TR_Code = record[IX_TRANSACT_TR_CODE]
        TR_code_str = 'Code = ' + str(self.TR_Code)
        self.Txt_Code.Set_Text(TR_code_str)
        self.TRdesc  = str(record[IX_TRANSACT_TR_DESC])

        self.Txt_TrDesc.Set_Text(self.TRdesc)
        self.Transact_Record = list(record)
        pass

    # ----------------------------------------------------------------------------------------------
    def Frame_Totals_Setup(self):
        Nrow = 1
        Ncol = 6
        Headings = ['#0','Conto', 'Righe inserite', 'Cod.std da inserire', 'Senza codici da inserire', 'Totale calcolato ', 'Totale xlsx']
        Anchor   = ['c', 'c',     'c',                'c',                 'c',                        'c',                        'c',  ]
        Width    = [ 0,   70,      200,                200,                 200,                        120,                        120, ]
        Form_List = [Nrow, Ncol, Headings, Anchor, Width]
        result = self.Frame_Totals.Tree_Setup(Form_List)
        if result != '':
            msg_dlg = Message_Dlg(MSG_BOX_ERR,  result)
            msg_dlg.wait_window()
            return False
        return True

    # ---------------------------------------------------------------------------------------------
    #                     0    1     2      3      4      5      6      7        8      9
    # List_Transact_DB :  Id  nRow  Conto Contab Valuta Accred  Addeb  TR_Desc TRcode FullDesc
    # ----------------------------------------------------------------------------------------------
    def Frame_Transactions_Setup(self):
        Nrow = 33
        Ncol = 10
        Headings = ['#0','Ident', 'Riga', 'Conto', 'Contab', 'Valuta', 'Accred  ','Addeb  ', 'Descrizione', ' Codice ', 'Descizione Completa']
        Anchor   = ['c', 'c',     'c',    'c',     'c',      'c',      'e',       'e',         'w',         'c',        'w']
        Width    = [ 0,   60,      60,     60,      90,       90,       70,        60,         160,         80,         320 ]
        Form_List = [Nrow, Ncol, Headings, Anchor, Width]
        self.Frame_Transactions.Tree_Setup(Form_List)
        pass

    # ---------------------------------------------------------------------------------------------
    def Set_Focus_On_Row(self, Values):
        nRow = int(Values[0])
        Date = Values[1]
        Index = -1
        for Rec in self.Frame_Transactions.Loaded_List:
            Index +=1
            if Rec[IX_ROW_NROW] == nRow:
                myDate = Rec[IX_ROW_VALUTA]
                if myDate == Date:
                    self.Frame_Transactions.Set_List_For_Focus(Index)
                    break

# =================================================================================================
