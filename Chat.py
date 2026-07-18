# --------------------------------------------- #
#                                               #
#           *****     Chat.py     *****         #
#      Exchanging messages between classes      #
#                                               #
# --------------------------------------------- #

import time
from Common.Constants import *
from Widgt.Dialogs import Message_Dlg

# ---------------------------------------------------------------------------------------
class Messages_Chat:
    def __init__(self):
        self._Participants_Id_List = []  # [   [<class>, NAME], ... , [<class>, NAME]  ]
        self.Value        = 0
        self.Start_nsTime = time.clock_gettime_ns(0)
        self._Msg_To_Tx_Queue  = []      # First in / First out QUeue

    def _Share_Msg(self):
        for Participant_Id in self._Participants_Id_List:
            Participant_Id[0].update()

    def Attach(self, Participant_Id):
        if not self._Participants_Id_List or Participant_Id not in self._Participants_Id_List:
            self._Participants_Id_List.append(Participant_Id)
            pass

    def Detach(self, Participant_Name):
        if self._Participants_Id_List:
            Participant_Id = self.Get_Participant_Id_From_Name(Participant_Name)
            if Participant_Id in self._Participants_Id_List:
                self._Participants_Id_List.remove(Participant_Id)

    def Get_Participants(self):
        return self._Participants_Id_List

    def Get_Participant_Id_From_Name(self, Name):
        if not self._Participants_Id_List:
            return []
        else:
            for Partic_Id in self._Participants_Id_List:
                if Partic_Id[IX_TOP_NAME] == Name:
                    return Partic_Id
            return []

    def Get_Participant_Name_from_classInstance(self, Class):
        if not self._Participants_Id_List:
            return []
        else:
            for Partic_Id in self._Participants_Id_List:
                if Partic_Id[IX_TOP_CLASS] == Class:
                    return Partic_Id[IX_TOP_NAME]
            return UNKNOWN

    def Check_Name_Is_On_Participants_List(self, Name):
        for Particip_Id in self._Participants_Id_List:
            if Particip_Id[IX_TOP_NAME] == Name:
                return True
        return False

    def Set_Start_Time(self):
        self.Start_nsTime = time.time_ns()

    def Get_Elapsed_Time(self):
        Elapsed_Time = time.time_ns() - self.Start_nsTime
        Time_ms = Elapsed_Time/1000000
        iVal100 = int(Time_ms * 100 + 0.5)
        myVal = iVal100 / 100
        return myVal

    def Increment_Value(self, value, nVolte):
        self.Value += value * nVolte
        self._Share_Msg()

    def _Share_Messages(self):
        while self._Msg_To_Tx_Queue:
            Msg_To_Tx   = self._Msg_To_Tx_Queue[0]
            self._Msg_To_Tx_Queue.remove(Msg_To_Tx)
            Receiv_Name = Msg_To_Tx[1]
            Transmtr    = Msg_To_Tx[0]
            Request     = Msg_To_Tx[2]
            Values_List = Msg_To_Tx[3]
            Participant_Id = self.Get_Participant_Id_From_Name(Receiv_Name)
            if Participant_Id:
                # -------------------------------------------------------------
                Participant_Class = Participant_Id[IX_TOP_CLASS]
                Participant_Class.Share_Msg_on_Chat(
                                 Transmtr, Request, Values_List)
                # -------------------------------------------------------------

    def Tx_Request(self, Tx_Req_List):       # [Txr, [RecList], Request, [Values]]
        # Transmitter         = Tx_Req_List[0]
        Receivers_Name_List = Tx_Req_List[1]
        if Tx_Req_List and self._Participants_Id_List:
            if Receivers_Name_List[0] == ANY:
                for Participant_Id in self._Participants_Id_List:
                    ParticipantName = Participant_Id[IX_TOP_NAME]
                    if ParticipantName != Tx_Req_List[0]:
                        Tx_List = [Tx_Req_List[0],
                                   Participant_Id[IX_TOP_NAME],
                                   Tx_Req_List[2],
                                   Tx_Req_List[3]]
                        self._Msg_To_Tx_Queue.append(Tx_List)
            else:
                for Receiv_Name in Receivers_Name_List:
                    if self.Check_Name_Is_On_Participants_List(Receiv_Name):
                        Tx_List = [Tx_Req_List[0],
                                   Receiv_Name,
                                   Tx_Req_List[2],
                                   Tx_Req_List[3]]
                        self._Msg_To_Tx_Queue.append(Tx_List)
        self._Share_Messages()

    @classmethod
    def View_Partic(cls):
        myChat = Ms_Chat
        Participants_List = myChat.Get_Participants()
        Text = '-----------------------------\nParticipants List:'
        for Participant in Participants_List:
            Text += '\n   - ' + Participant[IX_TOP_NAME]
        Text += '\n-----------------------------'
        Msg_Dlg = Message_Dlg(MSG_BOX_INFO, Text)
        Msg_Dlg.wait_window()
    # -------------------------------------------------------------------------------------


# ============================ #
#                              #
Ms_Chat = Messages_Chat()      #
#                              #
# ============================ #