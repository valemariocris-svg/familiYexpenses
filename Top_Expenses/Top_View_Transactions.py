# ================================================================================= #
#                  *****     Top_View_Transact.py     *****                         #
# XLS_Row_List : nRow  Contab  Valuta  Descr1  Accred  Addeb  Descr2                #
# ================================================================================= #

from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data_Manager

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import *
from Top_Expenses.Modules_Manager import Modul_Mngr
from Widgt.Widgets import TheButton, TheText, TheCombo

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
        self.geometry(TOP_TR_VIEW_GEOMETRY)
        self.title('***   View transactions database  *** ')
        self.configure(background=BACKGND)

        # --------------------------   Create Treeview Frame   ------------------------------------
        self.Frame_Transactions  = TheFrame(self, 10, 20, self.Clk_On_Transaction)
        self.Frame_Transactions_Setup()
        self.Frame_Transactions.Frame_View()

        self.Txt_dates    = TheText(self, TXT_DISAB,      10, 870,  21, 2, '')
        self.Txt_FullDesc = TheText(self, TXT_DISAB,     220, 870,  76, 3, '')
        self.Txt_Code     = TheText(self, TXT_DISAB,      10, 950,  13, 1, '')
        self.Txt_TrDesc   = TheText(self, TXT_DISAB,     150, 950,  28, 1, '')

        self.StrVar_List  = tk.StringVar
        self.OptMenu_List = TheCombo(self,  self.StrVar_List, 550, 950, 210, 20,
                                     TRANSACT_VIEW_SEL, TRANSACT_VIEW_ALL, self.Clk_ListSel)
        self.Btn_Exit = TheButton(self, BTN_DEF_EN, 770, 945, 13, '  E S C I  ', self.Call_OnClose)

        self.Transact_Record   = None
        self.TR_Code           = 0
        self.TRdesc            = ''
        self.View_Transact_mde = self.Data.Get_sel_dictionary_value(TRANSACT_VIEW_MODE)

        self.All_Transact_as_is= []
        self.All_TR_Contab_ASC = []
        self.TR_Normal_Code    = []
        self.TR_Generic_Code   = []

        self.Fill_Transactions_Frame()
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

    # --------------------------------------------------------------------------------------------
    def Fill_Transactions_Frame(self):
        transact_list = self.Data.Get_Transact_recs_asis()
        self.Frame_Transactifons_Load()
        pass

    # ---------------------------------------------------------------------------------------------
    def Clear_Sel_Updt_Btn(self):
        self.Txt_Code.Clear_Text()

    # ---------------------------------------------------------------------------------------------
    def Clk_ListSel(self, Value):
        self.View_Transact = Value
        self.Frame_Transactifons_Load()
        self.Transact_Id_Selcted = None

    # ---------------------------------------------------------------------------------------------
    def Clk_Delete_Transact(self):
        if self.Transact_Id_Selcted is not None:
            Messg  = 'Delete Tansaction Id : ' + str(self.Transact_Id_Selcted) + '\n'
            Messg += 'Transaction code     : ' + str(self.TR_Code) + '\n'
            Messg += 'Transact description : ' + self.TRdesc
            Msg_Dlg = Message_Dlg(MSG_BOX_ASK, Messg)
            Msg_Dlg.wait_window()
            Reply = Msg_Dlg.data
            if Reply == YES:
                self.Data.Delete_Transact_Rec(self.Transact_Id_Selcted)

    # ---------------------------------------------------------------------------------------------
    def Frame_Transactifons_Load(self):
        TR_Name = Get_File_Name(self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME))
        if self.View_Transact == TRANSACT_VIEW_AS_IS:
             Title = '     movimenti come in Db'
             List = self.Data.Get_Transact_recs_asis()

        elif self.View_Transact == TRANSACT_VIEW_CONTAB_ASC:
             Title = '     movimenti ordinato-i per contabile'
             List = self.Data.Get_Transact_recs_ordered()

        elif self.View_Transact == TRANSACT_VIEW_NORMAL_CODE:
             Title = '     movimenti con codice normale'
             List  = self.Data.Get_Transac

        else:
            Title = '     movimenti con codici generici'
            List = self.Data.Get_Transact_GenericCode_List()
        #
        FrameText = ('      ' + TR_Name + '     ' + str(List) + str(Title))
        template = [INT_TOSTRING, SIC, YMD, YMD, FLOAT_TOSTR, FLOAT_TOSTR, SIC, INT_TOSTRING, SIC]

        view_list = []
        for Rec in List:
            rec_toView = convert_rcord_toView(template, Rec)
            view_list.append(rec_toView)
        #
        self.Frame_Transactions.Frame_Title(FrameText)
        self.Frame_Transactions.Frame_View()

    # ---------------------------------------------------------------------------------------------
    def Clk_On_Transaction(self, Values):
        self.Transact_Id_Selcted = Values[0]
        FullDesc = Values[7]
        self.Txt_FullDesc.Set_Text(FullDesc)
        self.TR_Code = Values[8]
        TR_Str = 'Code = ' + str(Values[8])
        self.TRdesc  = str(Values[4])
        self.Txt_Code.Set_Text(TR_Str)
        self.Txt_TrDesc.Set_Text(self.TRdesc)
        self.Transact_Record = list(Values)
        # self.BtnDelet.Btn_Enable()
        pass

    # ---------------------------------------------------------------------------------------------
    #                     0    1     2      3      4      5      6      7        8      9
    # List_Transact_DB :  Id  nRow  Conto Contab Valuta Accred  Addeb  TR_Desc TRcode FullDesc
    # ----------------------------------------------------------------------------------------------
    def Frame_Transactions_Setup(self):
        Nrow = 39
        Ncol = 10
        Headings = ['#0','Ident', 'Riga', 'Conto', 'Contab', 'Valuta', 'Accred  ','Addeb  ', 'Descrizione', ' Codice ', 'Descizione Compl.']
        Anchor   = ['c', 'c',     'c',    'c',     'c',      'c',      'e',       'e',         'w',         'c',        'w']
        Width    = [ 0,   30,      30,     80,      80,       80,       80,        80,         100,         80,         200 ]
        Form_List = [Nrow, Ncol, Headings, Anchor, Width]
        self.Frame_Transactions.Tree_Setup_Strech(Form_List, ['#10'])
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

    # ---------------------------------------------------------------------------------------------
    def get_dates_from_listToInsert(self, Id):
        rec = self.Data.Get_rec_from_list_toInsert(Id)
        if rec:
            return rec[IX_TRANSACT_CONTAB], rec[IX_TRANSACT_VALUTA]
        return '---', '---'

# =================================================================================================
