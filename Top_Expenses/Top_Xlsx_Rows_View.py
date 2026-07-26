# ================================================================================= #
#                  *****     Top_XLSX_Rows_View.py     *****                        #
# Showing Xlsx Rows exactly as in Xlsx file                                         #
# XLS_Row_List : nRow  Contab  Valuta  Descr1  Accred  Addeb  Descr2                #
# ================================================================================= #

from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data_Manager

from Widgt.Dialogs import Print_Received_Message, Message_Dlg
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import *

from Top_Expenses.Modules_Manager import Modul_Mngr

class Top_XLSX_Rows_View(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data_Manager
        self.Mod_Mngr = Modul_Mngr
        self.Data_List = List           # Not used

        self.Chat.Attach([self, TOP_XLSX_VIEW])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry(TOP_XLSX_VIEW_GEOMETRY)
        self.title('***   View Sheet Rows xlsx file   *** ')
        self.configure(background=BACKGND)

        self.List_WithCode = None
        self.List_Without  = None
        self.List_ToView   = None
        self.Title_ToView  = None

        self.Txt1 = TheTextPoints(self, TXT_DISAB,  20, 860, 33, 4, '', 11)
        self.Txt2 = TheTextPoints(self, TXT_DISAB, 310, 860, 60, 4, '', 11)

        self.Txt_Debit = TheTextPoints(self, TXT_ENAB, 310, 954, 12, 1, '', 11)
        TheButton(self, BTN_DEF_EN, 440, 950, 16, 'cerca addebito',  self.Clk_Find_Debit)
        TheButton(self, BTN_DEF_EN, 650, 950, 15, ' E S C I  ',    self.Call_OnClose)

        # --------------------------   Create Treeview Frame   ------------------------------------
        self.Frame_Desc_x2     = TheFrame(self, 20, 20, self.Clk_On_Sheets_Row)
        self.Frame_Frame_Desc_x2_Setup()
        self.Frame_Sheets_Rows_View()

    # ---------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_XLSX_VIEW)
        self.destroy()
        pass

    # ---------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:
            self.Call_OnClose()
            pass

    # ---------------------------------------------------------------------------------------------
    def Clk_On_Sheets_Row(self, Values):
        if len(Values) == 7:
            self.Txt1.Set_Text(Values[IX_ROW_DESCR1])
            self.Txt2.Set_Text(Values[IX_ROW_DESCR2])
        else:
            self.Txt1.Set_Text('')
            self.Txt2.Set_Text(Values[IX_ROW_COMP_FULLDES])

    # ---------------------------------------------------------------------------------------------
    def Frame_Frame_Desc_x2_Setup(self):  # called only on startup
        nRows      = 39
        NcolToDisp = 7
        Headings = ['#0', 'Row', "Contab", "Valuta", "Descrizione 1",
                    "Credits   ", "Debits   ", "Descrizione 2"]
        Anchor = ['c', 'c', 'c', 'c', 'w', 'e', 'e', 'w']
        Width  = [0,    40,  80,  80,  160, 70,  70,  260]
        Form_List = [nRows, NcolToDisp, Headings, Anchor, Width]
        self.Frame_Desc_x2.Tree_Setup(Form_List)

    def View_Xlsx_Rows(self):
        List = self.Data.Get_Xlsx_Rows_From_Sheet_normalized()
        XLS_Name  =Get_File_Name(self.Data.Get_sel_dictionary_value(XLSX_FILENAME))
        FrameText = ('     ' + XLS_Name + ':   ')
        FrameText += str(len(List)) + '   transactions  on  sheet  rows  '
        self.Frame_Desc_x2.Frame_Title(FrameText)
        self.Frame_Desc_x2.Load_Row_Values(List)
        self.Frame_Desc_x2.Frame_View()

    # ---------------------------------------------------------------------------------------------
    def Frame_Sheets_Rows_View(self):
        self.View_Xlsx_Rows()

    # ---------------------------------------------------------------------------------------------
    def Clk_Find_Debit(self):
        pass

# =================================================================================================
