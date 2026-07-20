# =========================================================================== #
#            -----   Filesnames_Mngr.py   -----                               #
#   files names managed:                                                              #
#      Files_Names.txt                                                        #
#      Codes_DB.db                                                            #
#      Xlsx_filex.xlsx                                                        #
#      Transact.db                                                            #
#  Classes inheritance:                                                       #
#  Files_Names_Mngr <-- Codes_DB <-- Xlsx_Manager <-- Transact_DB             #
#  Data = Transact_DB()                                                       #
#                                                                             #
#  for more informations see Data_Organization.txt                            #
# =========================================================================== #
import json
import tkinter as tk
from tkinter import filedialog
from Common.Common_Functions import *
from datetime import datetime

# ---------------------------------------------------------------------------------------
class Files_Names_Manager:
    def __init__(self):
        self.Dummy = 0   # to avoid @classmethod
        # '/home/mario/aExpen_Init/Selections'
        # self._Selections_List    = []
        self._Codes_DB_Filename  = UNKNOWN
        # self._Xlsx_Filename      = UNKNOWN
        # self.Sheet_Name          = UNKNOWN
        self._Work_Sheet         = None
        self._Transact_DB_Filename = UNKNOWN

        self._Xlsx_Conto    = None  # or on selecting new file  FIDEU_2024_01.xlsx
        self._Xlsx_Year     = None  # they are  calculated on startup
        self._Xlsx_Month    = None
        self._Transact_Year = None  # or on selecting new file  Transact_2024

        self.Curr_Year  = datetime.now().year    # to max years history setup
        self.Curr_Month = datetime.now().month
        self.Min_Year = self.Curr_Year - 9
        self.Max_Year = self.Curr_Year + 1

        self._sel_dictionary = {}

    # ----------------------------------------------------------------------------------- #
    #            ----------------      public   methods   -----------------               #
    # ----------------------------------------------------------------------------------- #
    def Load_selections_dictionary(self):
        if not os.path.exists(DICTIONARY_FULL_NAME):
            try:
                # 1. Creazione e salvataggio del file
                SelPath = Path(SELECTIONS_DIR_NAME)
                SelPath.mkdir(parents=True, exist_ok=True)
                with open(DICTIONARY_FULL_NAME, "w", encoding="utf-8") as f:
                    # CORREZIONE: Scriviamo il dizionario, non il nome del file!
                    json.dump(Default_selections_dictionary, f, indent=4, ensure_ascii=False)
                    # indent=4 rende il file JSON facilmente leggibile anche da un essere umano

                # 2. Lettura di verifica
                with open(DICTIONARY_FULL_NAME, "r", encoding="utf-8") as f:
                    self._sel_dictionary = json.load(f)
                return NEW

            except Exception as e:
                return f"Error on creating/reading dictionary: {e}"
            finally:
                pass
        else:
            try:
                with open(DICTIONARY_FULL_NAME, "r", encoding="utf-8") as fff:
                    self._sel_dictionary = json.load(fff)
                    return OK
            except Exception as e:
                return f"error on loading\nselections dictionary:\n  {e}"
            finally:
                pass

    # -----------------------------------------------------------------------------------
    def Get_selections_dictionary(self):  # NEW SEL
        self._Load_dictionary()
        return self._sel_dictionary

    # --------------------------------------------------------------------------------
    def Get_sel_dictionary_value(self, Key):
        return self._sel_dictionary[Key]

    def Update_key_dictionary(self, Key, Value):     # Update an Item
        self._sel_dictionary[Key] = Value
        self._Save_dictionary()
        pass

    # -----------------------------------------------------------------------------------
    def Get_TransacYear(self):
        return self._Transact_Year

    # ----------------------------------------------------------------------------------
    def Sel_codes_filename(self, Parent):
        Codes_Directory = self.Get_sel_dictionary_value(CODES_DIRECTORY)
        if Codes_Directory == UNKNOWN:
            Codes_Directory = DEFAULT_INIT_DIR
        # -----------------------------------------------------
        Full_filename = tk.filedialog.askopenfilename(parent=Parent,
            title='Select codes database',
            filetypes=[('db file', '*.db')],
            initialdir=Codes_Directory)
        # -----------------------------------------------------
        if not Full_filename:
            return False, " ERROR 9:\n a codes database MUST be selected"
        status, data = Gl_Cek_Codes_Name(Full_filename)
        if not status:
            data += "\nFATAL ERROR 6:\nfilenamename error on codes select"
            return False, data
        Codes_Directory = Get_Dir_Name(Full_filename)
        self.Update_key_dictionary(CODES_FILENAME, Full_filename)
        self.Update_key_dictionary(CODES_DIRECTORY, Codes_Directory)
        return True, Full_filename

    # ----------------------------------------------------------------------------------
    def Sel_Xlsx_filename(self, Parent):
        Xlsx_Directory = self.Get_sel_dictionary_value(XLSX_DIRECTORY)
        if Xlsx_Directory == UNKNOWN:
            Xlsx_Directory = DEFAULT_INIT_DIR
        # -----------------------------------------------------
        Full_filename = tk.filedialog.askopenfilename(parent=Parent,
            title='Select xlsx file',
            filetypes=[('xlsx file', '*.xlsx')],
            initialdir=Xlsx_Directory)
        # -----------------------------------------------------
        if not Full_filename:
            return False, "xlsx not selected"
        status, data = Gl_Cek_Xlsx_Name(Full_filename)
        if not status:
            data += "\nfilenamename error on xlsx select"
            return False, data
        Codes_Directory = Get_Dir_Name(Full_filename)
        self.Update_key_dictionary(XLSX_FILENAME, Full_filename)
        self.Update_key_dictionary(XLSX_DIRECTORY, Codes_Directory)
        return True, Full_filename

    # ----------------------------------------------------------------------------------
    def Sel_Transact_filename(self, Parent):
        Transact_Directory = self.Get_sel_dictionary_value(TRANSACT_DIRECTORY)
        if Transact_Directory is UNKNOWN:
            Transact_Directory = DEFAULT_INIT_DIR
        # -----------------------------------------------------
        Full_filename = tk.filedialog.askopenfilename(parent=Parent,
            title='Select transactions database',
            filetypes=[('db file', '*.db')],
            initialdir=Transact_Directory)
        # -----------------------------------------------------
        if not Full_filename:
            return False,  "filenamename error  on transactions select"
        self.Update_key_dictionary(CODES_FILENAME, Full_filename)
        Transact_Directory = Get_Dir_Name(Full_filename)
        self.Update_key_dictionary(TRANSACT_DIRECTORY, Transact_Directory)
        return True

    # -------------------------------------------------------------------------------------
    # def Get_Xls_CommonDir(self):
    #     nSlash = []
    #     Count  = -1
    #     for Char in self._Xlsx_Filename:
    #         Count = Count + 1
    #         if Char == '/':
    #             nSlash.append(Count)
    #     Len_nSlash = len(nSlash)
    #     if Len_nSlash < 4:
    #         return False
    #     IndexCommon = nSlash[Len_nSlash-3]
    #     CommonXlsx = self._Xlsx_Filename[0:IndexCommon]
    #     return CommonXlsx

    # -------------------------------------------------------------------------------------
    # def Get_Transact_CommonDir(self):
    #     nSlash = []
    #     Count  = -1
    #     for Char in self._Transact_DB_Filename:
    #         Count = Count + 1
    #         if Char == '/':
    #             nSlash.append(Count)
    #     Len_nSlash = len(nSlash)
    #     if Len_nSlash < 4:
    #         return False
    #     IndexCommon = nSlash[Len_nSlash-2]
    #     CommonTransact = self._Transact_DB_Filename[0:IndexCommon]
    #     return CommonTransact


    # ----------------------------------------------------------------------------------- #
    #            ----------------      internal  methods   ---------------                #
    # ----------------------------------------------------------------------------------- #
    # def _Read_Selections(self):
        # self._Selections_List = []
        # Selection_File = open(SELECTIONS_FULL_NAME)  # default is 'r'
        # for Line in Selection_File:
        #     self._Selections_List = eval(Line)
        # Selection_File.close()
        #
        # self._Codes_DB_Filename = self._Selections_List[IX_CODES_FILE]
        # self._Xlsx_Filename     = self._Selections_List[IX_XLSX_FILE]
        # self.Sheet_Name         = self._Selections_List[IX_SHEET_NAME]
        # self._Transact_DB_Filename = self._Selections_List[IX_TRANSACT_FILE]
        #
        # self._Codes_DB_Filename    = self._sel_dictionary[CODES_FILENAME]
        # self._Xlsx_Filename        = self._sel_dictionary[XLSX_FILENAME]
        # self._Transact_DB_Filename = self._sel_dictionary[TRANSACT_FILENAME]
        # pass

    # ------------------------------------------------------------------------------------
    def _Save_dictionary(self):
        try:
            with open(DICTIONARY_FULL_NAME, "w", encoding="utf-8") as f:
                # indent=4 rende il file JSON facilmente leggibile anche da un essere umano
                json.dump(self._sel_dictionary, f, indent=4, ensure_ascii=False)
            return True, ""
        except Exception as e:
            return False, f"Error on saving\nseletcions dictionary: {e}",

    # ----------------------------------------------------------------------------------------
    def _Load_dictionary(self):
        if not os.path.exists(DICTIONARY_FULL_NAME):
            self._sel_dictionary = Default_selections_dictionary
            with open(DICTIONARY_FULL_NAME, "w", encoding="utf-8") as f:
                # indent=4 rende il file JSON facilmente leggibile anche da un essere umano
                json.dump(DICTIONARY_FULL_NAME, f, indent=4, ensure_ascii=False)
            self._Save_dictionary()

        try:
            with open(DICTIONARY_FULL_NAME, "r", encoding="utf-8") as f:
                self._sel_dictionary = json.load(f)
            return OK
        except Exception as e:
            print(f"New dictionary : {e}")
            return NEW

# =======================================================================================
