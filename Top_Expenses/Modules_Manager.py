# ============================================================================= #
#                 -----   Modules_Manager.py   -----                            #
#                    child of class  Mod_Mngr_Init                              #
#        instanced on start as:    Modul_Mngr = Modules_Manager()               #
#                                                                               #
# ============================================================================= #

from Widgt.Dialogs import *

class Modules_Manager:
    def __init__(self):
        super().__init__()
        self.Data = Data_Manager
        self.Chat = Ms_Chat
        self.Toplevels_Id_List = []

        self.Dummy              = None
        self.myList             = []    # n.u.

    # =======================   Selections  settings    ==============================================#
    #                  called at start from Main_Window                                               #
    # =============================================================================================== #
    def Init_selections_dictionary(self):
        Result = self.Data.Load_selections_dictionary()
        if Result == NEW:
            self.Data.Clear_Xlsx_Conto_Year_Month()
            return NEW
        elif Result == OK:
            return OK
        return NOK

    # ============================================================================================= #
    #   ----------   the    CODES_DB  is  CHECKED on startup by Main_Wind    ------                 #
    # ============================================================================================= #
    def Top_Launcher(self, Top_to_launch, Origin, List):
        self.myList = List
        if self.Chat.Check_Name_Is_On_Participants_List(Top_to_launch):
            # close the toplevel just opened
            self.Chat.Tx_Request([Origin, [Top_to_launch], CODE_TO_CLOSE, []])
            return

        # ---------------------------------------------------------------------------
        elif Top_to_launch == TOP_CODES_MNGR: # or\
            # Top_to_launch == TOP_XLSX_VIEW or \   # these top windows are
            # Top_to_launch == TOP_GR_MNGR          # launched only from Top_Codes_Mngr
            if not self.Check_xlsx(Origin):
                msg_dlg = Message_Dlg(MSG_BOX_ERR, "an xlsx file must be selected")
                msg_dlg.wait_window()  # diagnostic in Sel_Xlsx_Mngr
                return
            if not self.Load_xlsx_Mngr(Origin):
                return

            if not self.check_xlsx_transact_filenames_load_transact_create_rows_to_ins_list(Origin):
                return

        # ---------------------------------------------------------------------------
        elif Top_to_launch == TOP_QUERY:
            pass
            # if not self.Check_for_Transact_for_queries():       # check, create transactions Db
            #     return

            if not self.Load_Transact_Mngr(Origin):           # load transactions records
                return
        TopLevel = self._Get_TopLev(Top_to_launch)
        TopLevel([])

    # -----------------------------------------------------------------------------------------------
    def check_xlsx_transact_filenames_load_transact_create_rows_to_ins_list(self, Origin):
        if not self.Check_create_transact_database_for_xlsx_filename():
            return False
        File_Name = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)

        if File_Name == UNKNOWN:
            dlg_msg = Message_Dlg(MSG_BOX_ERR, "FATAL ERROR 26:\nthe transactions file not found ")
            dlg_msg.wait_window()
            return False
        if not self.Load_Transact_Mngr(Origin):
            return False
        self.Data.Create_rows_to_insert_list()
        return True

    # ============================================================================================= #
    # manage  codes  xlsx  transactions:
    # Check_: if unknow: select: if not: return False   return True
    # Sel_:   if not: rturn False,   else
    # ============================================================================================= #
    def Check_codes(self, Origin):   # called only in Main_Wind
        Codes_DB_Filename = self.Data.Get_sel_dictionary_value(CODES_FILENAME)
        if Codes_DB_Filename == UNKNOWN:
            if not self.Sel_Codes_Mngr(Origin):
                Msg = Message_Dlg(MSG_BOX_INFO, "without a codes database\nit is impossible to continue\nExit")
                Msg.wait_window()
                return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Sel_Codes_Mngr(self, Origin):
        file_dlg = File_Dialog(CODES_FILENAME)
        status = file_dlg.status
        data   = file_dlg.data
        if not status:
            dbCodesName = self.Data.Get_sel_dictionary_value(CODES_FILENAME)
            statusA, dataA = Gl_Cek_Codes_Name(dbCodesName)
            if not statusA:
                msg_dlg = Message_Dlg(MSG_BOX_ERR, f"{data}\n on selecting a codes database")
                msg_dlg.wait_window()
                return False
            return True
        else:
            self.Chat.Tx_Request([Origin, [MAIN_WIND], VIEW_SELECTIONS, []])
            self.check_xlsx_transact_filenames_load_transact_create_rows_to_ins_list(Origin)
            return True

    # ---------------------------------------------------------------------------------------------
    def Load_Codes_Mngr(self, Origin):
        status, data = self.Data.Load_Codes_Tables()
        if not status:
            Msg_Dlg = Message_Dlg(MSG_BOX_ERR, data)
            Msg_Dlg.wait_window()
            return False, data        # Error on loading codes database
        self.Chat.Tx_Request([Origin, [ANY], CODES_DB_LOADED, []])
        return True, ''

    # =============================================================================================
    def Check_xlsx(self, Origin):
        xlsx_Filename = self.Data.Get_sel_dictionary_value(XLSX_FILENAME)
        if xlsx_Filename == UNKNOWN:
            if not self.Sel_Xlsx_Mngr(Origin):
                return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Sel_Xlsx_Mngr(self, Origin):
        file_dlg = File_Dialog(XLSX_FILENAME)
        status = file_dlg.status
        data = file_dlg.data
        if not status:
            Xlsx_Name = self.Data.Get_sel_dictionary_value(XLSX_FILENAME)
            statusA, dataA = Gl_Cek_Xlsx_Name(Xlsx_Name)
            if not statusA:
                msg_dlg = Message_Dlg(MSG_BOX_ERR, f"{data}\n on selecting xlsx file")
                msg_dlg.wait_window()
                return False
            return True
        else:
            self.Data.Load_Xlsx_Rows()
            self.Chat.Tx_Request([Origin, [MAIN_WIND], VIEW_SELECTIONS, []])
            self.check_xlsx_transact_filenames_load_transact_create_rows_to_ins_list(Origin)
            return True

    # --------------------------------------------------------------------------------------------
    def Load_xlsx_Mngr(self, Origin):
        File_Name = self.Data.Get_sel_dictionary_value(XLSX_FILENAME)
        if File_Name == UNKNOWN:
            if not self.Sel_Xlsx_Mngr(Origin):
                return False
        status, data = self.Data.Load_Xlsx_Rows()
        if not status:
            Msg_Dlg = Message_Dlg(MSG_BOX_ERR, data)
            Msg_Dlg.wait_window()
            return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Sel_Transact_Mngr(self, Origin):
        file_dlg = File_Dialog(TRANSACT_FILENAME)
        status   = file_dlg.status
        data     = file_dlg.data
        if not status:
            msg_dlg = Message_Dlg(MSG_BOX_ERR, data)
            msg_dlg.wait_window()
            return False
        else:
            self.Chat.Tx_Request([Origin, [MAIN_WIND], VIEW_SELECTIONS, []])
            return True

    # --------------------------------------------------------------------------------------------
    def Load_Transact_Mngr(self, Origin):
        File_Name = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)
        if File_Name == UNKNOWN:
            if not self.Sel_Transact_Mngr(Origin):
                return False
        status, data = self.Data.Load_Transactions_Table()
        if not status:
            Msg_Dlg = Message_Dlg(MSG_BOX_ERR, data)
            Msg_Dlg.wait_window()
            return False

        self.Chat.Tx_Request([Origin, MAIN_WIND, VIEW_SELECTIONS, []])
        return True

    # --------------------------------------------------------------------------------------------------
    # /home/mario/bFiles/bXLSX_Files/ FIDEU/FIDEU_2024/
    # /home/mario/bFiles/bXLSX_Files/ TRANSACTIONS/
    def Check_create_transact_database_for_xlsx_filename(self) -> bool:
        full_xlsx_filename, xlsx_Year, xlsx_conto = self.Get_full_xlsx_name_year_conto()
        # xlsx_filename = Get_File_Name(full_xlsx_filename)
        ixConto = full_xlsx_filename.find(xlsx_conto)
        if ixConto == -1:
            msg_dlg = Message_Dlg(MSG_BOX_ERR, "FATAL ERROR 13:\nConto doesn't existin xlsx filename")
            msg_dlg.wait_window()
            return False
        Transactions_Dir       = full_xlsx_filename[:ixConto]
        full_transact_filename = Transactions_Dir + TRANSACT_ID + str(xlsx_Year) + '.db'
        status, data           = Gl_Cek_Transactions_Name(full_transact_filename)
        if not status:
            data += '\nImpossible to cretae transactions filename\nfrom xlsx'
            msg_dlg = Message_Dlg(MSG_BOX_ERR, data)
            msg_dlg.wait_window()
            return False

        if not os.path.isfile(full_transact_filename):
            self.Data.Update_key_dictionary(TRANSACT_FILENAME, full_transact_filename)
            status, data = self.Data.Create_Transact_Table()
            if not status:
                Mess_Dlg = Message_Dlg(MSG_BOX_ERR, data)
                Mess_Dlg.wait_window()
                # error: restore unknown
                self.Data.Update_key_dictionary(TRANSACT_FILENAME, UNKNOWN)
                return False

            Messg = "Transactions database for year:  " + str(xlsx_Year) + "\ncorrectly created"
            Mess_Dlg = Message_Dlg(MSG_BOX_INFO, Messg)
            Mess_Dlg.wait_window()
            directory = Get_Dir_Name(full_transact_filename)
            self.Data.Update_key_dictionary(TRANSACT_DIRECTORY, directory)
            return True
        else:
            status, data = Gl_Cek_Transactions_Name(full_transact_filename)
            if not status:
                Messg = f"FATAL ERROR 14:\n{data}\nFound an erroneous transactions file:\n{full_transact_filename}"
                Mess_Dlg = Message_Dlg(MSG_BOX_ERR, Messg)
                Mess_Dlg.wait_window()
                return False
        # is it necessary to compare transactions and xlsx years ?
        # NO: full_transact_filename = Transactions_Dir + TRANSACT_ID + str(xlsx_Year) + '.db'
        self.Data.Update_key_dictionary(TRANSACT_FILENAME, full_transact_filename)
        return  True

    # --------------------------------------------------------------------------------------------
    def Get_full_xlsx_name_year_conto(self):
        self.Dummy = 0
        Full_xlsx_filename = self.Data.Get_sel_dictionary_value(XLSX_FILENAME)
        # FIDEU_2024_09-1.xlsx
        xlsx_filename = Get_File_Name(Full_xlsx_filename)
        Year     = xlsx_filename[6:10]
        Conto    = xlsx_filename[:5]
        return Full_xlsx_filename, Year, Conto

    # -------------------------------------------------------------------------------------------------------
    # Xlsx Compact Row      nRow   Contab  Valuta    FullDesc  Accr      Addeb
    # Transact DB Record    Ident  Conto   Contab    Valuta    TR_Desc   Accred   Addeb   TRcode  FullDesc
    # -------------------------------------------------------------------------------------------------------
    def Add_Toplevels_Id_List(self, Id):
        if Id not in self.Toplevels_Id_List:
            self.Toplevels_Id_List.append(Id)
        pass

    # ---------------------------------------------------------------------------------------------
    def _Get_TopLev(self, NAME):
        for Id in self.Toplevels_Id_List:
            if Id[IX_TOP_NAME] == NAME:
                return Id[IX_TOP_CLASS]
        return None

    # ---------------------------------------------------------------------------------------------
    # invoked on  sel_Codes_Db  Delete  Add Update  code   sel_xlsx  Insert  (Queries....)
    def Initialize_codes_xlsx_transact(self, Origin):
        self.Chat.Tx_Request([TOP_CODES_MNGR, [ANY], CODE_TO_CLOSE, []])
        if not self.Load_Codes_Mngr(Origin):
            dlg_msg = Message_Dlg(MSG_BOX_ERR, f"FATAL ERROR 21\non loading codes Db")
            dlg_msg.wait_window()
            return False
        elif not self.Load_xlsx_Mngr(Origin):
            dlg_msg = Message_Dlg(MSG_BOX_ERR, f"FATAL ERROR 21\non loading xlsx rows Db")
            dlg_msg.wait_window()
            return False
        elif not self.Load_Transact_Mngr(Origin):
            dlg_msg = Message_Dlg(MSG_BOX_ERR, f"FATAL ERROR 21\non loading transactions Db")
            dlg_msg.wait_window()
            return False
        return True

    # --------------------------------------------------------------------------------------------
    def regenerate_transact_Db(self, Origin):
        Full_transact_filename = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)
        transact_filename = Get_File_Name(Full_transact_filename)
        Messg = f"Confermi di cancellare il database\n{transact_filename}"
        Msg_Dlg = Message_Dlg(MSG_BOX_ASK, Messg)
        Msg_Dlg.wait_window()
        Reply = Msg_Dlg.data
        if Reply == YES:
            # filepath = Full_transact_filename
            # È sempre buona norma verificare prima se il file esiste davvero
            if os.path.exists(Full_transact_filename):
                os.remove(Full_transact_filename)
                print(f"file {transact_filename}\neliminato")
            else:
                msg_dlg = Message_Dlg(MSG_BOX_ERR, f"file {transact_filename}\nnon esiste per la cancellazione")
                msg_dlg.wait_window()
                return False
            if not self.check_xlsx_transact_filenames_load_transact_create_rows_to_ins_list(Origin):
                return False
        return True





# =================================================================================================


# -------------------------------- #
Modul_Mngr = Modules_Manager()     #
# -------------------------------- #
