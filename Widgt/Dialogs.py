# -------------------------------------------------------------------------------------- #
#                                 Dialogs.py                                             #
#     -------------------     Messsages   Dialog      ---------------                    #
# -------------------------------------------------------------------------------------- #

import tkinter as tk
from Widgt.Widgets import TheText
from Widgt.Widgets import TheCombo

# =======================   M E S S A G E      D I A L O G       ========================
#  1...44      1 line       1..22 \n  one line

class Message_Dlg(tk.Toplevel):
    def __init__(self, Option, Texto):
        super().__init__()
        self.resizable(False, False)
        self.PosXY = '+700+20'
        Geo = '470x650' + self.PosXY
        self.geometry(Geo)

        self.title('Modal  Dialog')
        self.configure(bg='lightblue')
        self.Texto = ''
        self.data  = ' '
        self.MaxChar_xLine = 42     #  VERY IMPORTANT for nLines count

        if Texto[-1] == '\n':
            self.Txt = Texto[:-1]
        else:
            self.Txt = Texto

        self.Nchar_xLine      = self.MaxChar_xLine
        self.nLine            = 1
        self.nCharCount_xLine = 0

        for Char in self.Txt:
            self.Texto += Char
            self.nCharCount_xLine += 1
            if self.nCharCount_xLine >= self.MaxChar_xLine:    # self.Nchar_xLine:
                self.nCharCount_xLine = 0
                self.nLine += 1
            if Char == '\n':
                self.nCharCount_xLine = 0
                self.nLine           += 1
                if self.nLine        > 80:
                    break
        self.nLine += 2
        VertFlot  = float(self.nLine) * 14.5
        Vert_Delt = int(VertFlot)
        Btn_Xpos  = 280
        Btn_Ypos  = 60  + Vert_Delt
        VertYgeo  = 120 + Vert_Delt
        Geo = '450x' + str(VertYgeo)+ self.PosXY
        self.geometry(Geo)
        # self.geometry('450x' + str(VertYgeo)+'+700+20')

        if Option == MSG_BOX_INFO:
            self.title('Info Message')
            TheText(self, TXT_MSG_WHITE, 10, 10, self.MaxChar_xLine, self.nLine, self.Texto)
            TheButton(self, BTN_DEF_EN, Btn_Xpos, Btn_Ypos, 15, 'OK', self.Clk_OK)

        elif Option == MSG_BOX_ERR:
            self.title('E R R O R   Message')
            TheText(self, TXT_MSG_ERR,   10, 10, self.MaxChar_xLine, self.nLine, self.Texto)
            TheButton(self, BTN_DEF_EN, Btn_Xpos, Btn_Ypos, 15, 'OK', self.Clk_OK)

        elif Option == MSG_BOX_ASK:
            self.title('YES  NO  Selection Request')
            self.Texto += ' ?'
            TheText(self, TXT_MSG_WHITE, 10, 10, self.MaxChar_xLine, self.nLine, self.Texto)
            TheButton(self, BTN_DEF_EN, Btn_Xpos, Btn_Ypos, 15, 'YES', self.Clk_YES)
            TheButton(self, BTN_DEF_EN,  20, Btn_Ypos,  15, 'NO', self.Clk_NO)

        elif Option == MSG_BOX_ASK_YNCH:
            self.title('YES  NO Change Selection Request')
            self.Texto += ' ?'
            TheText(self, TXT_MSG_WHITE,  10, 10, self.MaxChar_xLine, self.nLine, self.Texto)
            TheButton(self, BTN_DEF_EN, 320, Btn_Ypos,  9, 'YES',    self.Clk_YES)
            TheButton(self, BTN_DEF_EN,  20, Btn_Ypos,  9, 'NO',     self.Clk_NO)
            TheButton(self, BTN_DEF_EN, 150, Btn_Ypos, 14, 'CHANGE', self.Clk_CHANGE)
            pass


        elif Option == MSG_BOX_ASK_EXIT:
            self.title('YES  NO EXIT Request')
            self.Texto += ' ?'
            TheText(self, TXT_MSG_WHITE,  10, 10, self.MaxChar_xLine, self.nLine, self.Texto)
            TheButton(self, BTN_DEF_EN, 320, Btn_Ypos,  9, 'YES',    self.Clk_YES)
            TheButton(self, BTN_DEF_EN,  20, Btn_Ypos,  9, 'NO',     self.Clk_NO)
            TheButton(self, BTN_DEF_EN, 150, Btn_Ypos, 14, 'EXIT', self.Clk_CHANGE)
            pass

        else:
            self.title('FATAL ERROR 7\n!!!  Message type unknown   !!!')
            TheText(self,   TXT_MSG_ERR,  43, 20, self.Nchar_xLine, self.nLine, 'Message Code NOT FOUND')
            TheButton(self, BTN_DEF_EN, 260, Btn_Ypos, 15, 'OK', self.Clk_OK)
        self.wait_visibility()
        self.grab_set()
        self.transient()
        pass

    def Clk_OK(self):
        self.data = OK
        self.grab_release()
        self.destroy()

    def Clk_YES(self):
        self.data = YES
        self.grab_release()
        self.destroy()

    def Clk_NO(self):
        self.data = NO
        self.grab_release()
        self.destroy()

    def Clk_CHANGE(self):
        self.data = CHANGE
        self.grab_release()
        self.destroy()

    
    def Clk_EXIT(self):
        self.data = EXIT
        self.grab_release()
        self.destroy()

# ================================================================================= #
#                  *****      Top_View_Message.py      *****                        #
#                       View Message and select a value                             #
# ================================================================================= #

import tkinter as tk
from Common.Common_Functions import *
from Chat import Ms_Chat
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheTextPoints

# -----------------------------------------------------------------------------------
class View_Message_Select(tk.Toplevel):
    def __init__(self, Message, SelectList):
        super().__init__()
        self.resizable(False, False)
        self.geometry('750x650') # '470x650'    +100+500')

        self.title('Select Dialog')
        self.configure(bg='lightblue')
        self.Texto = ''
        self.data  = NONE
        self.MaxChar_xLine = 80     #  45 VERY IMPORTANT for nLines count

        if Message[-1] == '\n':
            self.Txt = Message[:-1]
        else:
            self.Txt = Message

        self.Nchar_xLine      = self.MaxChar_xLine
        self.nLine            = 1
        self.nCharCount_xLine = 0

        for Char in self.Txt:
            self.Texto += Char
            self.nCharCount_xLine += 1
            if self.nCharCount_xLine >= self.MaxChar_xLine:    # self.Nchar_xLine:
                self.nCharCount_xLine = 0
                self.nLine += 1
            if Char == '\n':
                self.nCharCount_xLine = 0
                self.nLine           += 1
                if self.nLine        > 80:
                    break
        self.nLine += 2
        VertFlot  = float(self.nLine) * 14.5
        Vert_Delt = int(VertFlot)
        Btn_Ypos  = 60  + Vert_Delt
        VertYgeo  = 120 + Vert_Delt
        self.geometry('750x' + str(VertYgeo)+'+400+50')

        self.title('Info Message')
        TheText(self, TXT_MSG_WHITE, 10, 10, self.MaxChar_xLine, self.nLine, self.Texto)
        self.StringVar = tk.StringVar
        self.OptMenu   = TheCombo(self, self.StringVar,20, Btn_Ypos, 16, 20, SelectList, SelectList[0], self.ClkCombo )
        self.data      = NONE
        TheButton(self, BTN_DEF_EN, 280, Btn_Ypos, 15, 'S E L E C T', self.Clk_OK)

        self.wait_visibility()
        self.grab_set()
        self.transient()
        pass

    def Clk_OK(self):
        self.grab_release()
        self.destroy()

    def ClkCombo(self, Value):
        self.data = Value
        self.destroy()

# ================================================================================= #
#                  *****      Top_View_Message.py      *****                        #
# ================================================================================= #
class View_Message(tk.Toplevel):
    def __init__(self, Messg):
        super().__init__()
        self.Chat = Ms_Chat
        self.Dummy = 0

        self.Text = Messg[0]
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
        self.Chat.Attach([self, TOP_VIEW_MESS])
        self.resizable(False, False)
        self.geometry(TOP_VIEW_MESS_GEOMETRY)
        self.title('***   Show  message   *** ')
        self.configure(background=BACKGND)
        self.Txt1 = TheTextPoints(self, TXT_MSG_WHITE,  20, 20, 44, 28, self.Text, 11)
        TheButton(self, BTN_DEF_EN, 270, 465, 16, 'E X I T ', self.Call_OnClose)
        pass

    # ----------------------------------------------------------------------------- #
    def Call_OnClose(self):
        self.Chat.Detach(TOP_VIEW_MESS)
        self.destroy()
        return

    # --------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        self.Dummy = Transmitter_Name
        if Request_Code == CODE_TO_CLOSE:
            self.Call_OnClose()
        elif Request_Code == VIEW_MESSAGE:
            self.Txt1.Set_Text('')
            self.Txt1.Set_Text(Values_List[0])
            pass


# =======================   C O M B O       D I A L O G       ========================
class Combo_Dlg(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.resizable(False, False)
        self.title('Combo  Dialog')
        self.configure(bg='lightblue')
        self.data = 'None'
        self.geometry('440x130+900+400')
        self.title('Combo Dialog')
        TheText(self, TXT_DISAB, 80, 25, 17, 1, 'Make a selection')
        self.StrVar = tk.StringVar()
        self.Combo = TheCombo(self, self.StrVar, 260, 25, 20, 14, List, ' Select year  ', self.Clk_Combo)
        TheButton(self, BTN_DEF_EN, 260, 65, 15, 'OK', self.Clk_OK)

        self.wait_visibility()
        self.grab_set()
        self.transient()

    # -------------------------------------------------------------------------
    def Clk_OK(self):
        self.grab_release()
        self.destroy()

    def Clk_Combo(self, Val):
        self.data = Val

# =================================================================================

from Data_Classes.Transact_DB import Data_Manager

# =======================   F I L E S    D I A L O G       ========================
class File_Dialog(tk.Toplevel):
    def __init__(self, Option):
        super().__init__()
        self.resizable(False, False)
        self.geometry('500x380+800+100')
        self.title('File Select  Dialog')
        self.configure(bg='white')
        self.Data = Data_Manager

        self.FileName = ''
        if Option == CODES_FILENAME:
            self.status, self.data = self.Data.Sel_codes_filename(self)
        elif Option == XLSX_FILENAME:
            self.status, self.data = self.Data.Sel_Xlsx_filename(self)
        elif Option == TRANSACT_FILENAME:
            self.status, self.data = self.Data.Sel_Transact_filename(self)
        self.destroy()
        pass

# ==============================================================================