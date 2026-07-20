#!/usr/bin/env python3

# *********************************************************************************************** #
#                            ***   Main_Window.py   ***                                           #
#               2026-07-18    the first version  with  github                                     #
# *********************************************************************************************** #

from Top_Expenses.Modules_Manager import Modul_Mngr
from Widgt.Dialogs import *
from Widgt.Widgets import *
from Top_Expenses.Top_Codes_Mngr import Top_Codes_Mngr
from Top_Expenses.Top_Codes_View import Top_View_Codes
from Top_Expenses.Top_GR_Codes_Mngr import Top_GR_Codes_Mngr
from Top_Expenses.Top_Xlsx_Rows_View import Top_XLSX_Rows_View
from Top_Expenses.Top_Insert import Top_Insert
from Top_Expenses.Top_View_Transactions import Top_View_Transact
from Top_Expenses.Top_Queries import Top_Queries

# -------------------------------------------------------------------------------------------------
class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data_Manager
        self.Mod_Mngr = Modul_Mngr
        self.Chat.Attach([self, MAIN_WIND])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry('5x5+900+600')
        self.configure(background=BACKGND)
        self.title('')

        self.Top_Level_Id_Create_List()
        self.Txt1 = TheText(self, TXT_DISAB, 20, 20, 36, 11, '')

        self.geometry(MAIN_WIND_GEOMETRY)
        self.title('* Gestione spese familiari  Vers. 3.0  17 Lug 2026 *')

        Widgets_Styles()   # Setup Styles  once called

        self.Dummy         = '  '
        self.Top_Gen       = None
        self.View_Xlsx     = None
        self.Top_Codes_Mngr= None
        self.Top_View      = None

        TheButton(self,  BTN_DEF_EN,  20, 250, 36, 'Gestione codi file xls e file movimenti',  self.Clk_Manage_Codes)
        TheButton(self, BTN_DEF_EN,  20, 300, 36, 'QUERIES',         self.Clk_Queries)
        TheButton(self, BTN_BOL_EN,  24, 350, 32, '  E S C I   ',    self.Call_OnClose)

        # =======================   startup initializations   =================================
        result = self.Mod_Mngr.Init_selections_dictionary()
        if result == NEW:
            Msg  = Message_Dlg(MSG_BOX_INFO, "new selections dictionary\nis  created\n\nplease select a codes database")
            Msg.wait_window()
        elif result == OK:
            pass
        else:
            Msg = Message_Dlg(MSG_BOX_ERR, "FATAL ERROR 1 on creating\nnew selections dictionary")
            Msg.wait_window()
            self.Call_OnClose()
        self.Top_Level_Id_Create_List()

        # -----------------------------------------------------------------
        if not self.Mod_Mngr.Check_codes(MAIN_WIND):
            self.Call_OnClose()
            return
        else:
            status, data = self.Mod_Mngr.Load_Codes_Mngr(MAIN_WIND)
            if not status:
                Msg = Message_Dlg(MSG_BOX_ERR, "FATAL ERROR 2:\ncodes database corrupted\nExit")
                Msg.wait_window()
                self.Call_OnClose()
                return

        self.Check_filenames()  # files names must be unknown or correct except codes database
        self.View_Selections()  # Set Selections filenames, files_satus, [tot], Queries,
        self.mainloop()

    # =============================================================================================
    def Call_OnClose(self):
        self.destroy()

    # ---------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, MAIN_WIND, Request_Code, Values_List)
        if Request_Code == CODE_SHOW_PARTIC_LIST:
            self.Chat.View_Partic()
        if Request_Code == VIEW_SELECTIONS:
            self.View_Selections()

     # -----------------------------------------------------------------------
    def Clk_Manage_Codes(self):
        self.Mod_Mngr.Top_Launcher(TOP_CODES_MNGR, MAIN_WIND, [])

    # ---------------------------------------------------------------------------------------------
    def Clk_Queries(self):
        self.Mod_Mngr.Top_Launcher(TOP_QUERY, MAIN_WIND, [])
        pass

    # ---------------------------------------------------------------------------------------------
    # Check if filenames are correct or unknown, set to unknown if not correct
    def Check_filenames(self):
        Full_Codes_DB_Filename = self.Data.Get_sel_dictionary_value(CODES_FILENAME)
        if Full_Codes_DB_Filename == UNKNOWN:
            pass
        elif not os.path.isfile(Full_Codes_DB_Filename):
            self.Data.Update_key_dictionary(CODES_FILENAME, UNKNOWN)
        else:
            status, data = Gl_Cek_Codes_Name(Full_Codes_DB_Filename)
            if not status:
                data += "\nFATAL ERROR 3: Codes filename set to unknown"
                msg_dlg = Message_Dlg(MSG_BOX_ERR, data)
                msg_dlg.wait_window()
                self.Data.Update_key_dictionary(CODES_FILENAME, UNKNOWN)

        # -----------------------------------------------------------------------
        Full_Xlsx_Filename = self.Data.Get_sel_dictionary_value(XLSX_FILENAME)
        if Full_Xlsx_Filename == UNKNOWN:
            pass
        elif not os.path.isfile(Full_Xlsx_Filename):
            self.Data.Update_key_dictionary(XLSX_FILENAME, UNKNOWN)
        else:
            status, data = Gl_Cek_Xlsx_Name(Full_Xlsx_Filename)
            if not status:
                data += "\nERROR xlsx filename set to unknown"
                msg_dlg = Message_Dlg(MSG_BOX_ERR, data)
                msg_dlg.wait_window()
        # -----------------------------------------------------------------------
        Full_Transact_Filename = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)
        if Full_Transact_Filename == UNKNOWN:
            pass
        elif not os.path.isfile(Full_Transact_Filename):
            self.Data.Update_key_dictionary(TRANSACT_FILENAME, UNKNOWN)
        else:
            status, data = Gl_Cek_Transactions_Name(Full_Transact_Filename)
            if not status:
                data += "\nERROR transactions filename set to unknown"
                msg_dlg = Message_Dlg(MSG_BOX_ERR, data)
                msg_dlg.wait_window()

    # ================================================================================
    def View_Selections(self):     # Set file Selections
        Full_Codes_DB_Filename = self.Data.Get_sel_dictionary_value(CODES_FILENAME)
        if Full_Codes_DB_Filename == UNKNOWN:
            msg_dlg = Message_Dlg(MSG_BOX_ERR, "FATAL ERROR 4: codes filename unknown\nExit")
            msg_dlg.wait_window()
            self.Call_OnClose()
        else:
            status, data =  Gl_Cek_Codes_Name(Full_Codes_DB_Filename)
            if not status:
                msg_dlg = Message_Dlg(MSG_BOX_ERR, data)
                msg_dlg.wait_window()
                self.Call_OnClose()
        Codes_Filename = Get_File_Name(Full_Codes_DB_Filename)
        # -----------------------------------------------------------
        Xlsx_Filename = UNKNOWN
        Full_xlsx_Filename = self.Data.Get_sel_dictionary_value(XLSX_FILENAME)
        if Full_xlsx_Filename == UNKNOWN:
            pass
        else:
            status, data =  Gl_Cek_Xlsx_Name(Full_xlsx_Filename)
            if not status:
                msg_dlg = Message_Dlg(MSG_BOX_ERR, data)
                msg_dlg.wait_window()
            else:
                Xlsx_Filename = Get_File_Name(Full_xlsx_Filename)

        # -------------------------------------------------------------
        Transact_Filename = UNKNOWN
        Full_Transact_Filename = self.Data.Get_sel_dictionary_value(TRANSACT_FILENAME)
        if Full_Transact_Filename == UNKNOWN:
            pass
        else:
            status, data =  Gl_Cek_Transactions_Name(Full_Transact_Filename)
            if not status:
                msg_dlg = Message_Dlg(MSG_BOX_ERR, data)
                msg_dlg.wait_window()
            else:
                Transact_Filename = Get_File_Name(Full_Transact_Filename)

        # -------------------------------------------------------------
        Filenames  = f"file codici:        {Codes_Filename}\n"
        Filenames += f"file  xlsx:           {Xlsx_Filename}\n"
        Filenames += f"file movimenti: {Transact_Filename}\n\n"

        visCodici  = self.Data.Get_sel_dictionary_value(CODES_VIEW_MODE)
        insertMode = self.Data.Get_sel_dictionary_value(TRANSACT_INSERT_MODE)
        strMode =  f"visualizza codici:        {visCodici}\n"
        strMode += F"modo ins. movimenti:  {insertMode}\n"

        year_selected = Get_Transactions_Year(Transact_Filename)    # 0 for UNKNOWN

        Conto      = self.Data.Get_sel_dictionary_value(QUERY_CONTO)
        Month      = self.Data.Get_sel_dictionary_value(QUERY_START_MONTH)
        Tot_Months = self.Data.Get_sel_dictionary_value(QUERY_TOT_MONTHS)
        Date       = self.Data.Get_sel_dictionary_value(QUERY_VAL_CONT_DATE)

        TRcode     = self.Data.Get_sel_dictionary_value(QUERY_CODE_SEL)
        GRcode     = self.Data.Get_sel_dictionary_value(QUERY_GROUP_SEL)
        CAcode     = self.Data.Get_sel_dictionary_value(QUERY_CATEGORY_SEL)
        TotMonths = int(TOT_MONTH_INT[Tot_Months])

        strQuery  = f"QUERY:\nanno:   {str(year_selected)}    Conto:  {Conto}   data:  {Date}\n"
        strQuery += f"mese:  {Month}   tot mesi:  {str(TotMonths)} \n"
        strQuery += f"{TRcode}    {GRcode}    {CAcode}"
        TextString = Filenames + strMode + strQuery

        self.Txt1.Set_Text(TextString)

    # ---------------------------------------------------------------------------------------
    def Top_Level_Id_Create_List(self):
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_Codes_Mngr,        TOP_CODES_MNGR])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_View_Codes,        TOP_CODES_VIEW])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_GR_Codes_Mngr,     TOP_GR_MNGR])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_XLSX_Rows_View,    TOP_XLSX_VIEW])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_Insert,            TOP_INS])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_View_Transact,     TOP_VIEW_TRANSACT])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_Queries,           TOP_QUERY])
        self.Mod_Mngr.Add_Toplevels_Id_List([View_Message,          TOP_VIEW_MESS])

# ================================================================= #
#                                                                   #
if __name__ == "__main__":                                          #
    Main_Window()                                                   #
    pass                                                            #
#                                                                   #
# ================================================================= #
