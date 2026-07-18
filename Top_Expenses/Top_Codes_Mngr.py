# -------------------------------------------------------------------------------------- #
#                  *****     Top_Codes_Mngr.py     *****                                 #
#                    VIEW  DELETE  ADD  UPDATE   Codes                                   #
#                                                                                        #
#           here are contained  the Combo  Texts  and Buttons                            #
# -------------------------------------------------------------------------------------- #

from Top_Expenses.Modules_Manager import Modul_Mngr
from Top_Expenses.Super_Top_Codes_Mngr import Super_Top_Mngr

from Widgt.Dialogs import *
from Widgt.Widgets import *
from Widgt.Widgets import TheCombo
from Widgt.Canvas_Frame import *

# -------------------------------------------------------------------------------------------------------------------
class Top_Codes_Mngr(Super_Top_Mngr):
    def __init__(self, List):
        super().__init__(self.Child_ClkNoCode, self.Child_ClkWithCode)
        self.Mod_Mngr    = Modul_Mngr
        self.List         = List        # Not Used. Used on Top_View_Codes
        self.Dummy        = 0

        self.Rec_Candidate = []
        self.Rec_Cand_For_ViewList = []
        self.Top_View_Type         = VIEW_ALL_LARGE
        self.Code_Request          = None
        self.New_Code_for_insert   = 0

        self.GR_List = self.Data.Get_GR_Codes_Table()
        # --------------------------- Group Select Combo  -----------------------------------------------------------
        self.ComboList = self.Data.Get_GRdescr_Ordered_List()
        self.GR_Combo1 = TheCombo(self.Canv_CodData, self.StrVar1, 80, 100, 32, 36,
                                  self.ComboList, GROUPSEL, self.Clk_Combo)

        # --------------------------         B U T T O N S        ---------------------------------------------------
        self.Btn_SelGeneric.Set_Text('Seleziona un codice')    # defined on Super for Ena/Disab for Clk on Frames
        self.Btn_SelGeneric.configure(command=self.Clk_Generic_Select)

        self.geometry(TOP_MNGR_GEOMETRY)

        self.LocConto      = ''
        self.LocIntYear    = 0
        self.Set_Conto_Year()       # Conto Years etc are setted on Load_Xlsx_Lists
        self.Load_Trees()

        # ********************************      C A N V A S      ****************************************************
        self.Canv_CodMngr = CreateCanvas(self, 10, 820, 380, 80)
        TheLable(self.Canv_CodMngr, LAB_BLUE, 110, 1, 25, "gestione dei codici ")

        TheButton(self.Canv_CodMngr, BTN_DEF_EN,  10,  30, 20, "crea codice normale ", self.Clk_Add_Std)
        TheButton(self.Canv_CodMngr, BTN_DEF_EN, 215,  30, 20, "crea codice generico", self.Clk_Add_Generic)
        TheButton(self.Canv_CodMngr, BTN_DEF_EN,  10,  75, 20, "aggiorna codice", self.Clk_Update)
        TheButton(self.Canv_CodMngr, BTN_DEF_EN,  215, 75, 20, "cancella  codice",self.Clk_Delete)


        #    canvas on Super_Top_Codes_Mngr.py
        TheButton(self.Canv_Tr_Mngr, BTN_DEF_EN,   10,   30,  19, "inserisci mov. nel Db", self.Clk_launch_top_insert)
        TheButton(self.Canv_Tr_Mngr, BTN_DEF_EN,   10,   75,  19, "visualizza movimenti",  self.Clk_ViewTransact)
        TheButton(self.Canv_Tr_Mngr, BTN_DEF_EN,  220,   30,  19, "seleziona un codice",self.Clk_Generic_Select)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # TheButton(self.Canv_Tr_Mngr, BTN_DEF_EN,  200,  75,  21, "<<<<  button for test >>>", self.Clk_Canv_Test)
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        self.Canv_CodFile = CreateCanvas(self,   450, 640, 170, 130)
        TheLable(self.Canv_CodFile, LAB_BLUE,     15,   1,  16, "gestione Db codici ")
        TheButton(self.Canv_CodFile, BTN_DEF_EN,  10,  30,  18, "seleziona Db codici", self.Clk_Sel_Codes)
        TheButton(self.Canv_CodFile, BTN_DEF_EN,  10,  75,  18, "visualizza codici",        self.Clk_View_Codes)

        self.Canv_XlsxFile = CreateCanvas(self,  670, 640, 160, 130)
        TheLable(self.Canv_XlsxFile, LAB_BLUE,    15,  1, 15, "  gestione  file xlsx ")
        TheButton(self.Canv_XlsxFile, BTN_DEF_EN, 10, 30, 18, "seleziona file xlsx",    self.Clk_Sel_xlsx)
        TheButton(self.Canv_XlsxFile, BTN_DEF_EN, 10, 75, 18, "visualizza file  xlsx",  self.Clk_View_Xlsx)

        TheButton(self, BTN_DEF_EN, 460, 760, 18, 'Vis. con/senza codice ', self.Clk_With_out)
        TheButton(self, BTN_DEF_EN, 680, 955, 20, 'E S C I ',  self.Call_OnClose)
        # ***********************************************************************************************************

    # ------------------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:
            self.Call_OnClose()
        elif Request_Code == CODE_CLK_ON_TR_CODES:  # Clicked on TCodes Tree [TR_Code]
            self.Clicked_On_CodesView(Values_List)
        elif Request_Code == CODES_DB_LOADED or \
            Request_Code == XLSX_UPDATED:
            self.Mod_Mngr.Init_Xlsx_Lists(TOP_CODES_MNGR)          # Load_Xlsx()
            self.Load_Trees()

    # ------------------------------------------------------------------------------------------------------
    def Child_ClkNoCode(self):
        self.Clear_Text_Widg(False)
        self.Txt_StrFullDesc1.Set_Text(self.Row_WithoutCode[IX_NO_CODE_FULL_DESCR])

    # ---------------------------------------------------------------------------------------------
    def Child_ClkWithCode(self):
        pass

    # ---------------------------------------------------------------------------------------------
    def Set_Conto_Year(self):
        Files_Ident  = self.Data.Get_Full_Xlsx_Transact_Ident()
        self.LocConto   = Files_Ident[IX_XLSX_CONTO]
        self.LocIntYear = Files_Ident[IX_XLSX_YEAR]

    # ---------------------------------------------------------------------------------------------
    def Clk_GR_Mngr(self):
        self.Mod_Mngr.Top_Launcher(TOP_GR_MNGR, TOP_CODES_MNGR, [])

    # ---------------------------------------------------------------------------------------------
    def Clk_With_out(self):
        self.Row_WithoutCode = None
        self.Frame_NoCodes.Clear_Focus()
        self.Frame_WithCodes.Clear_Focus()
        self.Clear_Text_Widg(True)
        if self.View_Without_Code:
            self.View_Without_Code = False
        else:
            self.View_Without_Code = True
            # self.Canv_Sel_Genr.Btn_Disable()
        self.View_Frames(-1)

    # ---------------------------------------------------------------------------------------------
    def Clk_Sel_Codes(self):
        self.Row_WithoutCode = None
        self.Frame_NoCodes.Clear_Focus()
        self.Frame_WithCodes.Clear_Focus()
        self.Mod_Mngr.Sel_Codes_Mngr(TOP_CODES_MNGR)
        # in case of error the diagnostic is made
        # in Sel_Codes_Mngr

    # ---------------------------------------------------------------------------------------------
    # def _load_rows_create_code_Nocode_list(self):
    #     status, data = self.Data.Load_Xlsx_Rows()
        # if not status:
        #     msg_dlg = Message_Dlg(MSG_BOX_ERR, data)
        #     msg_dlg.wait_window()
        #     return False
        # status, TRlist, xlsx_row = self.Data.Create_Code_NoCode_List()
        # if not status:
        #     print(TRlist, xlsx_row[IX_ROW_COMP_FULLDES])
        #     message = f"la descrizione completa per la riga={str(xlsx_row[IX_ROW_COMP_NROW])}\n"
        #     message += f"data={xlsx_row[IX_ROW_COMP_CONT]}  addeb={str(xlsx_row[IX_ROW_COMP_ADDEB])}\n\n"
        #     message += f"combacia con piu stringhe per la ricerca\n\n"
        #
        #     message += f"{xlsx_row[IX_ROW_COMP_FULLDES]}\n"
        #     list_for_select = [NOSELECT]
        #     for code in TRlist:
        #         strList =  f"{str(code)}  {self.Data.Get_TrDesc_FromCode(cLoad_Xlsx_Rowsode)}  {self.Data.Get_strToFind_FromCode(code)} "
        #         list_for_select.append(strList)
        #     dlg_select = View_Message_Select(message, list_for_select)
        #     dlg_select.wait_window()
        #     reply = dlg_select.data
        #     print(f"selezionato: {str(reply)}")
        #     if reply == NOSELECT:
        #         pass
        #     else:
        #         pass
        #         print("INSERIRE ROW IN ROW CON CODICI")
        # return True

    # ---------------------------------------------------------------------------------------------
    def Clk_Sel_xlsx(self):
        if not self.Mod_Mngr.Sel_Xlsx_Mngr(TOP_CODES_MNGR):
            return
        self.Frame_NoCodes.Clear_Focus()
        self.Frame_WithCodes.Clear_Focus()
        self.Load_Trees()

    # --------------------------------------------------------------------------------------------
    def Clk_View_Xlsx(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_CODES_MNGR, [])

    # ********************************************************************************************
    def Clk_launch_top_insert(self):
        self.Mod_Mngr.Top_Launcher(TOP_INS, TOP_CODES_MNGR, [])

    def Clk_ViewTransact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_CODES_MNGR, [])

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Codes(self):   # from Button Codes View
        self.Row_WithoutCode = None
        self.Top_View_Type = VIEW_ALL_LARGE
        self.Frame_NoCodes.Clear_Focus()
        self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW, TOP_CODES_MNGR,
                                   [VIEW_ALL_LARGE])  # Launch Top_Codes_View for ALL Large

    # ---------------------------------------------------------------------------------------------
    # Call from a click in Top_Codes_View Frame
    def Clicked_On_CodesView(self, TR_Full_List):
        if self.Top_View_Type != VIEW_ALL_LARGE:
            if self.View_Without_Code:
                if self.Row_WithoutCode:
                    Result = self.Set_Selected_Code(TR_Full_List)
                    if Result == YES:
                        self.TR_Code = TR_Full_List[IX_TR_FULL_TR_CODE]
                        self.TR_Desc = TR_Full_List[IX_TR_FULL_TR_DESC]
                        self.Data.Add_Row_WithCode_FromNoCode(self.Row_WithoutCode, self.TR_Code, self.TR_Desc)
                        self.Data.Delete_Row_NoCode(self.Row_WithoutCode)
                        Total      = self.Data.Get_Total_Rows()
                        Tot_NoCode = Total[IX_TOT_ROWS_WITHOUT_CODE]
                        if not Tot_NoCode:
                            self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW, TOP_CODES_MNGR, [VIEW_ALL_REDUC])  # Close the reduced Codes View

                        self.Try_To_Insert_Rec_On_Db(TR_Full_List)

                        self.Row_WithoutCode = None
                        self.Load_Trees()
                    else:
                        pass    # NO  Code to Insert
                else:
                    Msg_Dlg = Message_Dlg(MSG_BOX_INFO, 'Please select a Row without Code')
                    Msg_Dlg.wait_window()
            else:
                pass
        else:
            self.Frame_WithCodes.Clear_Focus()           # === Clicked On Codes View No Code Waiting
            self.Row_WithoutCode = None
            self.Txt_TR_Code1.Set_Text(TR_Full_List[IX_TR_FULL_TR_CODE])
            self.Txt_TR_Desc1.Set_Text(TR_Full_List[IX_TR_FULL_TR_DESC])
            self.Txt_GR_Code1.Set_Text( TR_Full_List[IX_TR_FULL_GR_CODE])
            self.GR_Combo1.SetSelText(TR_Full_List[IX_TR_FULL_GR_DESC])
            self.Txt_CA_Code1.Set_Text(TR_Full_List[IX_TR_FULL_CA_CODE])
            self.Txt_CAdesc1.Set_Text(TR_Full_List[IX_TR_FULL_CA_DESC])
            self.Txt_StrToFind1.Set_Text(TR_Full_List[IX_TR_FULL_STR_TO_FIND])
            self.Txt_StrFullDesc1.Set_Text(TR_Full_List[IX_TR_FULL_FULL_DESC])

    # ---------------------------------------------------------------------------------------------
    def Try_To_Insert_Rec_On_Db(self, TR_Full_List):
        #                          1      2     3      4        5      6      7     8
        # Record_List :  (Ident) Conto Contab Valuta  Accred Addeb TRdesc TRcode FullDes
        Conto  = self.LocConto
        Contab = self.Row_WithoutCode[IX_NO_CODE_CONTAB]
        Valuta = self.Row_WithoutCode[IX_NO_CODE_VALUTA]
        Accred = 0 # convert_amount(self.Row_WithoutCode[IX_NO_CODE_ACCRED])
        Addeb  = 0 # convert_amount(self.Row_WithoutCode[IX_NO_CODE_ADDEB])
        TR_Desc = TR_Full_List[IX_TR_FULL_TR_DESC]
        TRcode = TR_Full_List[IX_TR_FULL_TR_CODE]
        FullDesc = self.Row_WithoutCode[IX_NO_CODE_FULL_DESCR]
        Id = 0
        Rec_toInsert = [Id, Conto, Contab, Valuta, Accred, Addeb, TR_Desc, TRcode, FullDesc]
        status, data = self.Data.Insert_Transact_Record(Rec_toInsert)  # it opens also Db
        if status:
            Msg_Dlg = Message_Dlg(MSG_BOX_INFO,
                                  f'Record inserted on Transactions Db\nCode: {TRcode}  Description: {TR_Desc}')
            Msg_Dlg.wait_window()
            return True

        Msg_Dlg = Message_Dlg(MSG_BOX_ERR, data)
        Msg_Dlg.wait_window()
        self.Data.Close_Transactions_Database()
        return False


    # ---------------------------------------------------------------------------------------------
    def Clk_Generic_Select(self):   # from Button  Select a generic Code
        if not self.Row_WithoutCode:
            Msg_Dlg = Message_Dlg(MSG_BOX_INFO, 'Please select a Row without Code')
            Msg_Dlg.wait_window()
            return
        if self.Chat.Check_Name_Is_On_Participants_List(TOP_CODES_VIEW):
            if self.Top_View_Type != VIEW_ALL_REDUC:
                self.Chat.Tx_Request([TOP_CODES_MNGR, [TOP_CODES_VIEW], CODE_TO_CLOSE, []])
                self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW, [TOP_CODES_MNGR], [VIEW_ALL_REDUC])
                self.Top_View_Type = VIEW_ALL_REDUC
            else:
                pass
        else:
            self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW, [TOP_CODES_MNGR], [VIEW_ALL_REDUC])
            self.Top_View_Type = VIEW_ALL_REDUC

    # ----------------------------------------------------------------------------------- #
    # List_Rows_WithoutCode : nRow  Contab  Valuta  Accr     Addeb   FullDes              #
    # List_Rows_WithCode    : nRow  Contab  Valuta  TR_Desc  Accred  Addeb    TR_Code      #
    # ----------------------------------------------------------------------------------- #
    def Set_Selected_Code(self, TRfull_Rec):
        self.TR_Code  = int(TRfull_Rec[IX_TR_FULL_TR_CODE])
        TR_Desc = TRfull_Rec[IX_TR_FULL_TR_DESC]
        Messg   = 'Select Code: ' + str(self.TR_Code) + '\nDescription: ' + TR_Desc + '  '
        Msg_Dlg = Message_Dlg(MSG_BOX_ASK, Messg)
        Msg_Dlg.wait_window()
        Reply   = Msg_Dlg.data
        return Reply

    # ---------------------------------------------------------------------------------------------
    # _Wihtout_Code_Tree_List  nRow  Contab Valuta Accr   Addeb  FullDes
    # _Records_ToInsert_List   Ident Conto  Contab Valuta TRdesc Accred Addeb TR_Code Full_Desc
    def Create_RecToFind_From_NoCode(self, Row):
        Contab = Row[IX_NO_CODE_CONTAB]
        Valuta = Row[IX_NO_CODE_VALUTA]
        Accred = Row[IX_NO_CODE_ACCRED]
        Addeb = Row[IX_NO_CODE_ADDEB]
        flAccred = Convert_Str_To_Float(Accred)
        flAddeb  = Convert_Str_To_Float(Addeb)
        FullDesc = Row[IX_NO_CODE_FULL_DESCR]
        Rec_From_NoCode = [0, self.LocConto, Contab, Valuta, 'TRdesc', flAccred, flAddeb, 0, FullDesc]
        return Rec_From_NoCode

    # ------------------------------------------------------------------------------------------- #
    #    ***   Codes in 1-10.000 are the normal code with StrToFind.                              #
    #          All Xlsx Records with Full description that matches StrToFind                      #
    #          are  automatically selected for insert in transactions DB                          #
    #    ***   Codes  > 10.000   are generic code that can be assigned manually to                #
    #          any Xlsx Record. The assignement must be done for each Xlsx Row                    #
    # ------------------------------------------------------------------------------------------- #
    def Clk_Add_Generic(self):
        if self.Code_Request != BTN_ADD_GEN:
            Result = self.Data.Get_New_Code(GENERICCODE)
            if Result[0] != OK:
                Msg_Dlg = Message_Dlg(MSG_BOX_ERR, Result[1])
                Msg_Dlg.wait_window()
                return
            self.New_Code_for_insert = Result[1]
            self.Txt_TR_Code1.Set_Text(str(Result[1]))
            # self.Set_Button_Status(BTN_ADD_GEN)
            self.Row_WithoutCode = None
            self.Frame_WithCodes.Clear_Focus()
        else:
            if self.Add_Code():
                self.Code_Request = None
                # self.Set_Button_Status(BTN_RESET)

    # ---------------------------------------------------------------------------------------------
    def Clk_Add_Std(self):
        if self.Code_Request != BTN_ADD:
            Result = self.Data.Get_New_Code(NORMAL_CODE)
            if Result[0] != OK:
                Msg_Dlg = Message_Dlg(MSG_BOX_ERR, Result[1])
                Msg_Dlg.wait_window()
                return
            self.New_Code_for_insert = Result[1]
            self.Txt_TR_Code1.Set_Text(str(Result[1]))
            # self.Set_Button_Status(BTN_ADD)
            self.Row_WithoutCode = None
            self.Frame_WithCodes.Clear_Focus()
        else:
            if self.Add_Code():
                self.Code_Request = None
                # self.Set_Button_Status(BTN_RESET)

    # ------------     ***   Add new normal or generic  record  ***     ---------------------------
    def Add_Code(self):
        self.Row_WithoutCode = None
        self.Txt_TR_Code1.Set_Text(str(self.New_Code_for_insert))
        self.Frame_WithCodes.Clear_Focus()
        status, data = self.Check_Codes_Items_Is_OK()
        if not status:
            Msg_Dld = Message_Dlg(MSG_BOX_ERR, data)
            Msg_Dld.wait_window()
            return  False    # Record Data not OK

        if not self.Get_Confirm('Add'):
            return False

        status, data = self.Data.Add_DB_TR_Record(self.Rec_Candidate)
        if not status:
            Msg_Dld = Message_Dlg(MSG_BOX_ERR, data)
            Msg_Dld.wait_window()
            return False

        # elif status and data ==  MULTI:
        #     self.Mod_Mngr.View_Codes_Match_Error(MULTI)
        #     return False

        if self.Mod_Mngr.Load_Codes_Mngr(TOP_CODES_MNGR):
            # EXISTS: False, Error  : True, True exists   : True, False  NOT exists
            status, data = self.Data.Check_If_Code_Exist(self.New_Code_for_insert)
            if not status:
                Messg = f"Fatal error on add new code: {str(self.New_Code_for_insert)}\n{self.TR_Desc}"
                Msg_Dld = Message_Dlg(MSG_BOX_ERR, Messg)
                Msg_Dld.wait_window()
                return False
            else:
                self.Frames_Refresh()
                if data:
                    return True     # exists
        return False                # NOT exist

    # ------------------------     ***   Update TR code Record      -------------------------------
    def Clk_Update(self):
        if not self.Check_TRcode_Desc(BOTH_TR_GR):
            return
        self.Row_WithoutCode = None
        status, data = self.Check_Codes_Items_Is_OK()  # Check if data of record are OK
        if not status:
            Msg_Dld = Message_Dlg(MSG_BOX_ERR, data)
            Msg_Dld.wait_window()
            return                                     # Record Data not OK
        if not self.Get_Confirm('Update'):
            return

        status, data = self.Data.Update_DB_TR_Record(self.Rec_Candidate)
        if status:
            if not self.Mod_Mngr.Load_Codes_Mngr(TOP_CODES_MNGR):
                Msg_Dld = Message_Dlg(MSG_BOX_ERR, "error on reloading ")
                Msg_Dld.wait_window()
            else:
                Msg_Dld = Message_Dlg(MSG_BOX_INFO, "code record correctly updated")
                Msg_Dld.wait_window()
        else:
            if not self.Check_IfCodeExists():
                return
            if not self.Get_Confirm('Update'):
                return
            if self.Update_Record_Code():
                self.Frames_Refresh()
                self.Chat.Tx_Request([TOP_CODES_MNGR, [TOP_CODES_VIEW], CODES_DB_UPDATED, self.Rec_Cand_For_ViewList])
                # self.Set_Button_Status(BTN_RESET)

    # ------------------------     ***   Update TR code Record      -------------------------------
    def Update_Record_Code(self):
        Update_Result = self.Data.Update_DB_TR_Record(self.Rec_Candidate)
        Result = Update_Result[0]
        if Result == MULTI:
            Msg_Dld = Message_Dlg(MSG_BOX_INFO, 'Multimatching!\nTransaction code\nRecord NOT updated')
            Msg_Dld.wait_window()
            self.Mod_Mngr.View_Codes_Match_Error(Update_Result[1])
            return False
        elif Result != OK:
            Msg_Dld = Message_Dlg(MSG_BOX_ERR, Result[1])
            Msg_Dld.wait_window()
            return False
        if not self.Mod_Mngr.Load_Codes_Mngr(TOP_CODES_MNGR):
            return False
        return True

    # ------------------------     ***   Delete  the last TR Record      --------------------------
    def Clk_Delete(self):
        if not self.Check_TRcode_Desc(BOTH_TR_GR):
            return
        self.Row_WithoutCode = None
        status, data = self.Check_Codes_Items_Is_OK()  # Check if data of record are OK
        if not status:
            Msg_Dld = Message_Dlg(MSG_BOX_ERR, data)
            Msg_Dld.wait_window()
            return  # Record Data not OK
        if not self.Get_Confirm('Delete'):
            return

    # ------------------------     ***   Delete  the last TR Record      --------------------------
    def Delete_Code(self):
        Result = self.Data.Delete_DB_TR_Record(self.TR_Code) # return [OK,[]] or [STRING, [Diagn]]
        if Result[0] == STRING:
            Msg_Dld = Message_Dlg(MSG_BOX_ERR, Result[1])
            Msg_Dld.wait_window()
            return False
        else:           # Result[0] == OK:
            if self.Mod_Mngr.Load_Codes_Mngr(TOP_CODES_MNGR):
                if self.Data.Check_If_Code_Exist(self.TR_Code):    # check if record has canceled
                    Messg = ('Code ' + str(self.TR_Code) + '  ' + self.TR_Desc + '\n NOT  deleted ???')
                    Msg_Dld = Message_Dlg(MSG_BOX_ERR, Messg)
                    Msg_Dld.wait_window()
                    return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Check_TRcode_Desc(self, Action):
        self.TR_Code = self.Txt_TR_Code1.Get_Text(INTEGER)
        self.TR_Desc = self.Txt_TR_Desc1.Get_Text(STRING)
        if self.TR_Code == 0:
            Msg_Dlg = Message_Dlg(MSG_BOX_INFO, "Select a non zero code")
            Msg_Dlg.wait_window()
            return False
        if Action == BOTH_TR_GR:
            if self.TR_Desc == TRDESC:
                Msg_Dlg = Message_Dlg(MSG_BOX_INFO, "Select a valid description for code")
                Msg_Dlg.wait_window()
                return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Get_Confirm(self, strOper):     # "Delete"  "Update"  "add"
        Msg = ('Confirm to ' + strOper +'\n'
                'Code:        ') + str(self.TR_Code)
        Msg += '\nDescription: ' + str(self.TR_Desc)
        Msg_Dlg = Message_Dlg(MSG_BOX_ASK, Msg)
        Msg_Dlg.wait_window()
        Reply = Msg_Dlg.data
        if Reply == NO:
            return False # No Action
        return True

    # ---------------------------------------------------------------------------------------------
    def Check_IfCodeExists(self):
        if not self.Data.Check_If_Code_Exist(self.TR_Code):
            Msg_Dld = Message_Dlg(MSG_BOX_ERR, 'The code number do not exist')
            Msg_Dld.wait_window()
            return  False   # Code not  exists
        return True

     # ----------------------------------------------------------------------------------------
    def Check_Codes_Items_Is_OK(self) -> tuple[bool, str]:
        StrToFind     = self.Txt_StrToFind1.Get_Text(STRING).replace('\n', '', 5)
        if StrToFind == STRTOFIND:
            return False, 'Please set String to find'

        StringToFind_List = GetStrList_ForFind_Checked(StrToFind)
        if not StrToFind:
            return False, 'String to find NOT correct'
        self.TR_Code      = self.Txt_TR_Code1.Get_Text(INTEGER)
        self.TR_Desc      = self.Txt_TR_Desc1.Get_Text(STRING).replace('\n', '', 5)
        self.GR_Code      = self.Txt_GR_Code1.Get_Text(INTEGER)
        self.GR_Desc      = self.GR_Combo1.GetValue()
        self.CA_Desc      = self.Txt_CAdesc1.Get_Text(STRING)
        self.FullDesc     = self.Txt_StrFullDesc1.Get_Text(STRING)

        if not Check_strDate(self.FullDesc[0:10]):
            return False, 'Date on Full Desription NOT OK'

        if self.TR_Code == 0 or self.TR_Desc == TRDESC:
            return False, 'Code / Tr description NOT OK'

        if len(self.TR_Desc) <= 6:
            return False, 'TR description too short'

        if self.GR_Code == 0 or self.GR_Desc == GROUPSEL:
            return False, 'Group NOT OK'

        if not StrToFind_in_Fulldescr(StringToFind_List, self.FullDesc):
            return False, 'String To Find:\n' + str(StrToFind) + \
                '\n\ndoes not match with Full Desription:\n' + self.FullDesc

        status, data = self.Data.Check_if_stringToFind_matches(StringToFind_List, self.TR_Code)
        if status:
            return False, data

        self.Rec_Candidate  = [self.TR_Code, self.GR_Code, 0,
                               self.TR_Desc, str(StrToFind), self.FullDesc]
        self.Rec_Cand_For_ViewList = [self.TR_Code, self.TR_Desc, self.GR_Desc, self.CA_Desc, StrToFind]
        return True, ''

 
# ==============================================================================================================
