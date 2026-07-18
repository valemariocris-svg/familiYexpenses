# ----------------------------------------------------------------------------#
#                   ***  Top_GR_Codes_Mngr.py   ***                           #
#                  Window Class to  View Groups Codes                         #
#           1 Frame_GR_CA  : Groups x Category                                #
#           2 Frame_TRxGR  : Transactions x Group                             #
#           3 Frame_TRxCA  : Transactions per Category                        #
# ----------------------------------------------------------------------------#

import tkinter as tk
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data_Manager
from Common.Common_Functions import *

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheText
from Widgt.Widgets import TheCombo
from Widgt.Dialogs import Message_Dlg

# =============================================================================
class Top_GR_Codes_Mngr(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.Chat  = Ms_Chat
        self.Data  = Data_Manager

        self.Chat.Attach([self, TOP_GR_MNGR])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry(TOP_GRCODES_GEOMETRY)
        self.title('*****     Manage Groups Codes     *****')
        self.configure(background=BACKGND)

        self.Data_List = List
        self.Dummy     = None
        self.Value     = []

        self.Combo_PosX         = 320
        self.List_GRxCA         = []
        self.List_GRxCA_Full    = []
        self.List_TRxGR         = []
        self.List_TRxCA         = []
        self.CA_Codes_Ordered   = []
        self.GR_Codes_Ordered   = []
        self.GR_Rec_Full        = []
        self.Groups_Order       = False

        self.GRcode   = 0
        self.GRdesc   = ''
        self.CAcode   = 0
        self.CAdesc   = ''

        # self.New_GRcode_Selected = False
        # self.New_CAcode_Selected = False

        # --------------------------------  for updating Group vs. Category  --------------------------------
        self.Txt_GRcode = TheText(self, TXT_DISAB, 100, 815, 4, 1, '0')
        self.Txt_GRdesc = TheText(self, TXT_ENAB,  150, 815, 17, 1, 'Group Text')
        self.CategBlok  = TheText(self, TXT_DISAB, 320, 780, 23, 1, '          C a t e g o r y')
        self.Txt_CAcode = TheText(self, TXT_DISAB, 320, 815, 4,  1, '0')
        self.Txt_CAdesc = TheText(self, TXT_ENAB,  370, 815, 17, 1, 'Category text')

        # ----------------------------------   Category  Combo  ---------------------------------------------
        self.ComboList = ['Category for Group']
        self.StrVar    = None
        self.CA_Combo  = None

        # ----------------------------------    B U T T O N S     -------------------------------------------
        self.Btn_GR_Updt = TheButton(self, BTN_DEF_DIS, 550, 780, 26,
                                     'Update Categ. for Group\nand update descriptions', self.Update)
        self.Btn_Updt   = TheButton(self, BTN_DEF_EN, 550, 900, 26, '  Reload ',         self.Clk_Reload)

        self.Btn_Order = TheButton(self, BTN_DEF_EN,  100, 855, 20, '  Groups order ',        self.Clk_Order)
        self.Btn_New_GR = TheButton(self, BTN_DEF_EN, 100, 900, 20, 'Add new Group Record ', self.Clk_Add_GR)
        self.Btn_Del_GR = TheButton(self, BTN_DEF_EN, 100, 945, 20, 'Delete Group selected', self.Clk_Del_GR)
        self.Btn_New_CA = TheButton(self, BTN_DEF_EN, 320, 900, 20, 'Add new Categ. Record', self.Clk_Add_CA)
        self.Btn_Del_CA = TheButton(self, BTN_DEF_EN, 320, 945, 20, 'Delete Categ. selected',self.Clk_Del_CA)

        self.Btn_Exit   = TheButton(self, BTN_DEF_EN, 550, 945, 26, '  E X I T ',       self.Call_OnClose)

        # ----------------------------    T R E E   of  Groups x Categories      ----------------------------
        self.Frame_GRxCA = TheFrame(self,   232,  10, self.Clk_On_GRxCA_Tree)

        # ----------------------------    T R E E   of  Transactions x Category  ----------------------------
        self.Frame_TRxCA = TheFrame(self,  600,  10, self.Clk_On_TRxCA_Tree)

        # -----------------------------    T R E E   of  Transactions x Group    ----------------------------
        self.Frame_TRxGR = TheFrame(self,   10,  10, self.Clk_On_TRxGR_Tree)

        self.View_Codes_Frame()

    # -------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_GR_MNGR)
        self.destroy()

    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:               # Close
            self.Call_OnClose()
        elif Request_Code == CODE_CLEAR_FOCUS:          # Clear Focus
            self.Frame_TRxGR.Clear_Focus()
            self.Frame_TRxCA.Clear_Focus()
            self.Frame_GRxCA.Clear_Focus()

        elif Request_Code == CODE_CLIK_ON_XLSX:         # Clicked on Xlsx Tree  [nRow, Date]
            self.Frame_TRxGR.Clear_Focus()
            self.Frame_TRxCA.Clear_Focus()
            self.Frame_GRxCA.Clear_Focus()

        elif Request_Code == CODES_DB_LOADED:          # Clicked on Code Update
            self.Clk_Reload()

    # -------------------------------------------------------------------------------------------------------
    def Clk_Combo(self, CAdesc):
        CAcode = Get_List_Item(self.Data.Get_CA_Codes_Table(), IX_CA_CA_DESC, CAdesc, IX_CA_CA_CODE, -1)
        if CAcode == -1:
            return
        self.Txt_CAcode.Set_Text(CAcode)
        self.Txt_CAdesc.Set_Text(CAdesc)
        self.CAcode = CAcode
        self.CAdesc = CAdesc

    # -------------------------------------------------------------------------------------------------------
    def View_Codes_Frame(self):
        self.Frame_GRxCA_Setup()
        self.Frame_TRxCA_Setup()
        self.Frame_TRxGR_Setup()

        self.ComboList = ['Category for Group']
        for Rec in self.Data.Get_CA_Codes_Table():
            self.ComboList.append(Rec[IX_CA_CA_DESC])
        self.StrVar    = tk.StringVar()
        self.CA_Combo  = TheCombo(self, self.StrVar, XY_TO_HIDE, 850, 20, 22,
                                  self.ComboList, 'Category for Group', self.Clk_Combo)

        self.Frame_GRxCA.Frame_View()
        self.Frame_TRxCA.Frame_View()
        self.Frame_TRxGR.Frame_View()

        self.Frame_GRxCA.Clear_Focus()
        self.Frame_TRxCA.Clear_Focus()
        self.Frame_TRxGR.Clear_Focus()

    # ----------------------------    T R E E   of  Groups x Categories    --------------------------------------------
    def Frame_GRxCA_Setup(self):
        self.Frame_GRxCA.Frame_Title('  Groups  by Category  ')
        Nrows     = 35
        nColToVis = 3
        Headings  = ['#0', "Group", "Category", 'GRcod']
        Anchor    = ['c',   'w',        'w',       'c']
        Width     = [ 0,   170,         170,        0 ]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]

        self.Frame_GRxCA.Tree_Setup_Strech(Form_List, ['#3'])
        self.Set_GRxCA_List()
        self.Frame_GRxCA.Load_Row_Values(self.List_GRxCA)

    # ---------------------------------------------------------------
    def Clk_On_GRxCA_Tree(self, strValue):    #   #0 GRdesc  CAdesc  GRcode
        self.CA_Combo.PosX(XY_TO_HIDE)
        self.GRdesc = strValue[0]
        self.CAdesc = strValue[1]
        strGRcode   = strValue[2]
        if not CheckInteger(strGRcode):
            return
        self.GRcode = int(strGRcode)
        self.New_GRcode_Selected = False
        self.New_CAcode_Selected = False

        if len(self.GRdesc) < 3 and len(self.CAdesc) < 3:          # do nothing (impossible case)
            pass
        elif len(self.GRdesc) < 3:                            # case of New Category without associated Group
            self.CAcode = self.Data.Get_CA_Code_From_Desc(self.CAdesc)
            self.GRcode = 0
            self.GRdesc = ''
        else:                                            # Group present
            self.GR_Rec_Full = self.Data.Get_GR_RecFull_From_GRcode(self.GRcode)
            self.GRdesc = self.GR_Rec_Full[IX_GR_GR_DESC]   # 1
            self.CAcode = self.GR_Rec_Full[IX_GR_CA_CODE]   # 2
            self.CAdesc = self.GR_Rec_Full[3]               # added from Get_GR_RecFull_From_GRcode

            self.Set_List_TRxCA(self.CAcode)
            self.Frame_TRxCA.Load_Row_Values(self.List_TRxCA)
            self.Set_List_TRxGR(self.GRcode)
            self.Frame_TRxGR.Load_Row_Values(self.List_TRxGR)

            strLen_TRxCA = str(len(self.List_TRxCA))
            Title = '   ' +strLen_TRxCA + ' Transactions   '
            self.Frame_TRxCA.Frame_Title(Title)
            Head_TRxCA = ' by Cat:  ' + self.CAdesc
            self.Frame_TRxCA.Tree.heading(f'#{1}', text=Head_TRxCA)

            strLen_TRxGR = str(len(self.List_TRxGR))
            Title = '   ' + strLen_TRxGR + ' Transactions   '
            self.Frame_TRxGR.Frame_Title(Title)
            Head_TRxGR = ' by Group   ' + self.GRdesc
            self.Frame_TRxGR.Tree.heading(f'#{1}', text=Head_TRxGR)

        self.Txt_CAcode.Set_Text(str(self.CAcode))
        self.Txt_CAdesc.Set_Text(self.CAdesc)
        # self.CA_Combo.SetSelText(self.CAdesc)
        self.Txt_GRcode.Set_Text(str(self.GRcode))
        self.Txt_GRdesc.Set_Text(self.GRdesc)
        self.Btn_GR_Updt.Btn_Enable()


    # ----------------------------    T R E E   of  TRdesc x CAdesc    --------------------------------------
    def Frame_TRxCA_Setup(self):
        self.Frame_TRxCA.Frame_Title(' Transactions  ')
        self.Dummy = 0
        Nrows     = 35
        nColToVis = 1
        Headings  = ['#0', ' ']
        Anchor    = ['c',   'w']
        Width     = [ 0,   190]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_TRxCA.Tree_Setup(Form_List)

    # ---------------------------------------------------------------
    def Clk_On_TRxCA_Tree(self, Values):
        self.New_GRcode_Selected = False
        self.New_CAcode_Selected = False
        self.Dummy = Values[0]
        self.Frame_TRxCA.Clear_Focus()

    # --------------------    T R E E   of  TRcodes x GRcode   ----------------------------------------------
    def Frame_TRxGR_Setup(self):
        self.Frame_TRxGR.Frame_Title(' Transactions x groups ')
        Nrows     = 35
        nColToVis = 1
        Headings  = ['#0', '']
        Anchor    = ['c', 'w']
        Width     = [0, 190]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_TRxGR.Tree_Setup(Form_List)

    def Clk_On_TRxGR_Tree(self, Values):
        # self.New_GRcode_Selected = False
        # self.New_CAcode_Selected = False
        self.Dummy = Values[0]
        self.Frame_TRxGR.Clear_Focus()


    # ---------------------------------------------------------------
    def Set_GRxCA_List(self):
        self.List_GRxCA_Full  = []     # GRdesc  CAdescr   GRcode
        self.CA_Codes_Ordered = self.Data.Get_CA_Codes_Ordered()
        self.GR_Codes_Ordered = self.Data.Get_GR_Codes_Ordered()

        if not self.Groups_Order:
            self.Set_GRxCA_List_CAord()
        else:
            self.Set_GRxCA_List_GRord()

    # -------------------------------------------------------------------------------------------------------
    def Set_GRxCA_List_CAord(self):
        for RecCA in self.CA_Codes_Ordered:
            CAcode  = RecCA[0]
            if CAcode != 0:
                CAdescr = RecCA[1]
                Found   = False
                for RecGR in self.GR_Codes_Ordered:
                    if RecGR[IX_GR_CA_CODE] == CAcode:
                        self.List_GRxCA_Full.append([CAdescr, RecGR[IX_GR_GR_DESC], RecGR[IX_GR_GR_CODE]])
                        Found = True
                if not Found:
                    self.List_GRxCA_Full.append([CAdescr, ' ', 0])
        # --------------------------------------------
        self.List_GRxCA = []
        Current_Descr = ''
        for RecordCA in self.List_GRxCA_Full:
            CAdescr = RecordCA[0]
            if CAdescr != Current_Descr:
                Current_Descr = CAdescr
            else:
                CAdescr = ''
            RecordCA = [RecordCA[1], CAdescr, RecordCA[2]]
            self.List_GRxCA.append(RecordCA)

    # --------------------------------------------------------------------
    def Set_GRxCA_List_GRord(self):
        for RecGR in self.GR_Codes_Ordered:
            GRcode  = RecGR[IX_GR_GR_CODE]
            if GRcode != 0:
                CAcode  = RecGR[IX_GR_CA_CODE]
                CAdescr = self.Data.Get_CAdescr(CAcode)
                self.List_GRxCA_Full.append([CAdescr, RecGR[IX_GR_GR_DESC], RecGR[IX_GR_GR_CODE]])
        self.List_GRxCA = []
        Current_Descr = ''
        for RecordCA in self.List_GRxCA_Full:
            CAdescr = RecordCA[0]
            if CAdescr != Current_Descr:
                Current_Descr = CAdescr
            else:
                CAdescr = ''
            RecordCA = [RecordCA[1], CAdescr, RecordCA[2]]
            self.List_GRxCA.append(RecordCA)

    # -------------------------------------------------------------------------------------------------------
    def Set_List_TRxCA(self, CaCode):
        self.List_TRxCA = []
        TRcodesFull = self.Data.Get_TR_Codes_Full(-1)   # <<<<<<<<<<-----------------
        for Rec in TRcodesFull:
            if Rec[IX_TR_FULL_CA_CODE] == CaCode:
                self.List_TRxCA.append([Rec[IX_TR_FULL_TR_DESC]])
        self.List_TRxCA.sort()

    def Set_List_TRxGR(self, GRcode):
        self.List_TRxGR = []
        TRcodesFull = self.Data.Get_TR_Codes_Full(-1)   # <<<<<<<<<<-----------------
        for Rec in TRcodesFull:
            if Rec[IX_TR_FULL_GR_CODE] == GRcode:
                self.List_TRxGR.append([Rec[IX_TR_FULL_TR_DESC]])
        self.List_TRxGR.sort()

    # =======================================================================================================

    def Get_Data_From_GR_and_CA(self):
        self.GRcode  = self.Txt_GRcode.Get_Text(INTEGER)
        self.CAcode  = self.Txt_CAcode.Get_Text(INTEGER)
        self.GRdesc  = self.Txt_GRdesc.Get_Text(STRING).replace('\n', '', 5)
        self.CAdesc  = self.Txt_CAdesc.Get_Text(STRING).replace('\n', '', 5)

    def Set_Data_For_GR_and_CA(self):
        self.Txt_GRcode.Set_Text(str(self.GRcode))
        self.Txt_CAcode.Set_Text(str(self.CAcode))
        self.Txt_GRdesc.Set_Text(self.GRdesc)
        self.Txt_CAdesc.Set_Text(self.CAdesc)

    def Clear_Data(self):
        self.GRcode = 0
        self.CAcode = 0
        self.GRdesc = ''
        self.CAdesc = ''
        self.CA_Combo.PosX(XY_TO_HIDE)

    # =======================================================================================================
    def View_Result(self, Result):
        self.Dummy = 0
        if Result[0] == OK:
            self.View_Codes_Frame()
            Dlg_Msg = Message_Dlg(MSG_BOX_INFO, "Completed OK")
        else:
            Dlg_Msg = Message_Dlg(MSG_BOX_ERR, Result[1])
        Dlg_Msg.wait_window()

    # -------------------------------------------------------------------------------------------------------
    # CAT  Test  Confirm   GR Test Confirm   UPDATE  CAT && GR .............
    # ITEM  CAT GR BOTH     ACTION ADD  DEL  UPDT
    # -------------------------------------------------------------------------------------------------------
    def Confirm_Dialog(self, Item, toDo):
        self.CAdesc = self.Txt_CAdesc.Get_Text(STRING)
        self.GRdesc = self.Txt_GRdesc.Get_Text(STRING)
        Test = ''
        if Item == CATEG or Item == XLSX_AND_TRANSACT:
            if self.CAcode == 0 or self.CAdesc == '':
                Test = 'Category not  filled'
        if Item == GROUP or Item == XLSX_AND_TRANSACT:
            if self.GRcode == 0 or self.GRdesc == '' or self.CAcode == 0 or self.CAdesc == '':
                Test = 'Group or Categ  not  filled'
        if Test:
            Msg_Dlg = Message_Dlg(MSG_BOX_ERR, Test)
            Msg_Dlg.wait_window()
            return False

        if Item == CATEG:
            Message = 'Confirm to ' + toDo + '\nCateg code: ' + str(self.CAcode) + '\nCateg desc: ' + self.CAdesc
        elif Item == GROUP:
            Message = 'Confirm to ' + toDo + '\nGroup code: ' + str(self.GRcode) + '\nGroup desc: ' + self.GRdesc
        else:
            Message = "Confirm to update:\nGroup code: " + str(self.GRcode) + "   GRdesc: " + self.GRdesc
            Message += "\nCateg code: " + str(self.CAcode) + "   CAdesc: " + self.CAdesc

        Ask_Msg = Message_Dlg(MSG_BOX_ASK, Message)
        Ask_Msg.wait_window()
        Reply = Ask_Msg.data
        if Reply == YES:
            return True
        return False

    # -------------------------------------------------------------------------------------------------------
    def Clk_Add_CA(self):
        if self.CAcode == 0 or not self.New_CAcode_Selected:
            Result = self.Data.Get_New_Code(CATEG_CODES_TABLE)
            if Result[0] != OK:
                self.View_Result(Result)
            else:
                self.Clear_Data()
                self.CAcode = Result[1]
                self.Set_Data_For_GR_and_CA()
                self.CA_Combo.PosX(XY_TO_HIDE)
                # self.New_GRcode_Selected = False
                # self.New_CAcode_Selected = True
        else:
            if self.Confirm_Dialog(CATEG, ADD):
                # self.New_GRcode_Selected = False
                # self.New_CAcode_Selected = False
                Result = self.Data.Add_CA_Record(self.CAcode, self.CAdesc)
                self.View_Result(Result)

    def Clk_Del_CA(self):
        self.CA_Combo.PosX(XY_TO_HIDE)
        if self.Confirm_Dialog(CATEG, DEL):
            # self.New_GRcode_Selected = False
            # self.New_CAcode_Selected = False
            self.View_Result(self.Data.Del_CA_Record(self.CAcode))
            self.Clear_Data()
            self.Set_Data_For_GR_and_CA()

    # -------------------------------------------------------------------------------------------------------
    def Clk_Add_GR(self):
        if self.GRcode == 0 or not self.New_GRcode_Selected:
            Result = self.Data.Get_New_Code(GROUPS_CODES_TABLE)
            if Result[0] != OK:
                self.View_Result(Result)
            else:
                self.Clear_Data()
                self.CA_Combo.PosX(self.Combo_PosX)
                self.GRcode = Result[1]
                self.Set_Data_For_GR_and_CA()
                self.New_GRcode_Selected = True
                self.New_CAcode_Selected = False
        else:
            if self.Confirm_Dialog(GROUP, ADD):
                self.Get_Data_From_GR_and_CA()
                self.New_GRcode_Selected = False
                self.View_Result(self.Data.Add_GR_Record(self.GRcode, self.GRdesc, self.CAcode))

    # -------------------------------------------------------------------------------------------------------
    def Clk_Del_GR(self):
        if self.Confirm_Dialog(GROUP, DEL):
            self.New_GRcode_Selected = False
            self.New_CAcode_Selected = False
            self.View_Result(self.Data.Del_GR_Record(self.GRcode))
            self.Clear_Data()
            self.Set_Data_For_GR_and_CA()

    def Update(self):
        self.New_GRcode_Selected = False
        self.New_CAcode_Selected = False
        self.Get_Data_From_GR_and_CA()
        if self.Confirm_Dialog(UPDT_GR_CAT, XLSX_AND_TRANSACT):
            self.View_Result(self.Data.Update_GR_CA_Rec(self.GRcode, self.GRdesc, self.CAcode, self.CAdesc))

    # -------------------------------------------------------------------------------------------------------
    def Clk_Order(self):
        if self.Groups_Order:
            self.Groups_Order = False
        else:
            self.Groups_Order = True
        self.View_Codes_Frame()

    # -------------------------------------------------------------------------------------------------------
    def Clk_Reload(self):
        self.Set_GRxCA_List()
        self.Frame_GRxCA.Load_Row_Values(self.List_GRxCA)
        self.Frame_TRxCA.Load_Row_Values([])
        self.Frame_TRxGR.Load_Row_Values([])

        self.Clear_Data()
        self.Set_Data_For_GR_and_CA()
        self.New_GRcode_Selected = False
        self.New_CAcode_Selected = False

# ===========================================================================================================
