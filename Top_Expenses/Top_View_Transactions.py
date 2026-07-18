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

        self.Txt_dates    = TheText(self, TXT_DISAB,      10, 870,  21, 2, '')
        self.Txt_FullDesc = TheText(self, TXT_DISAB,     220, 870,  76, 3, '')
        self.Txt_Code     = TheText(self, TXT_DISAB,      10, 950,  13, 1, '')
        self.Txt_TrDesc   = TheText(self, TXT_DISAB,     150, 950,  28, 1, '')
        # self.BtnDelet     = TheButton(self, BTN_DEF_DIS, 620, 950,   15, ' Delete Record',  self.Clk_Delete_Transact)

        self.StrVar_List  = tk.StringVar
        self.OptMenu_List = TheCombo(self,  self.StrVar_List, 550, 950, 210, 20,
                                     TRANSACT_VIEW_SEL, TRANSACT_VIEW_ALL, self.Clk_ListSel)
        self.Btn_Exit = TheButton(self, BTN_DEF_EN, 770, 945, 13, '  E X I T  ',               self.Call_OnClose)

        self.Transact_Record = None
        self.TR_Code          = 0
        self.TRdesc          = ''
        self.View_Transact   = TRANSACT_VIEW_ALL

        self.All_Transact_as_is= []
        self.All_TR_Contab_ASC = []
        self.TR_Normal_Code    = []
        self.TR_Generic_Code   = []

        # self.Fill_Transactions_Frame()
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
        # self.BtnDelet.Btn_Disable()

    # ---------------------------------------------------------------------------------------------
    def Clk_ListSel(self, Value):
        self.View_Transact = Value
        self.Frame_Transactions_Load()
        self.Transact_Id_Selcted = None
        # self.BtnDelet.Btn_Disable()

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
    def Frame_Transactions_Load(self):
        TR_Name = Get_File_Name(self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME))
        if self.View_Transact == TRANSACT_VIEW_AS_IS:
             Title = '     transactions as is'
             Len = len(self.All_Transact_as_is)
             List = self.All_Transact_as_is
        elif self.View_Transact == TRANSACT_VIEW_CONTAB_ASC:
             Title = '     Transactions Contab ASC'
             Len = len(self.All_TR_Contab_ASC)
             List = self.All_TR_Contab_ASC
        elif self.View_Transact == TRANSACT_VIEW_NORMAL_CODE:
             Title = '     Transactions normal code'
             Len = len(self.TR_Normal_Code)
             List = self.TR_Normal_Code
        else:
            Title = '     Transactions generic code'
            Len = len(self.TR_Generic_Code)
            List = self.TR_Generic_Code
        #
        FrameText = ('      ' + TR_Name + '     ' + str(Len) + str(Title))
        template = [INT_TOSTRING, SIC, YMD, YMD, FLOAT_TOSTR, FLOAT_TOSTR, SIC, INT_TOSTRING, SIC]

        view_list = []
        for Rec in List:
            rec_toView = convert_rcord_toView(template, Rec)
            view_list.append(rec_toView)
        #
        self.Frame_Transactions.Frame_Title(FrameText)
        # self.Frame_Transactions.Load_Row_Values(Correct_List)
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
    #                      0     1      2     3      4      5      6      7     8
    # List_Transact_DB :  nRow  Conto Contab Valuta Accred  Addeb  TR_Desc TRcode FullDesc
    # Rec in view         Ident Conto Contab Valuta TR_Desc Accred Addeb  Full_Desc 'x']
    # ----------------------------------------------------------------------------------------------
    def Frame_Transactions_Setup(self):
        Nrow = 39
        Ncol = 9
        Headings = ['#0','Ident','Conto','Contab','Valuta','Description','Accred  ','Addebit  ', 'Full_Description', 'x']
        Anchor   = ['c', 'c',    'c',    'c',     'c',     'w',          'e',       'e',         'w',                'c']
        Width    = [ 0,   45,     70,     80,      80,      160,          80,        80,          300,                0 ]
        Form_List = [Nrow, Ncol, Headings, Anchor, Width]
        self.Frame_Transactions.Tree_Setup_Strech(Form_List, ['#9'])

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
