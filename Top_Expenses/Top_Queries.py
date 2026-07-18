# ---------------------------------------------------------------------------------- #
#                      *****     Top_Queries.py     *****                            #
#                      Queries  from  Transactions database                          #
#                                                                                    #
# ---------------------------------------------------------------------------------- #

from Common.Common_Functions import *
from Top_Expenses.Super_Top_Queries import Super_Top_Queries

from Widgt.Dialogs import Print_Received_Message, Message_Dlg
from Widgt.Tree_Widg import TheFrame

# ---------------------------------------------------------------------------------------------------------------------
class Top_Queries(Super_Top_Queries):
    def __init__(self, List):
        super().__init__()
        self.Data_List = List   # Not used

        self.Extraord_TRcode_List    = []
        self.OneYear_Transact_purged = []

        # --------------------------  Trees-Frames    for  Queries   --------------------------------------------------
        self.Frame1 = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnFrame)  # frames for transactions
        self.Frame2 = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnFrame)
        self.Frame3 = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnFrame)
        self.Frames_List = [self.Frame1, self.Frame2, self.Frame3]      # the lists of transactions frames
        self.Frames_Setup()

        self.Frame1_Tot = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnTot) # small frames for total on frame
        self.Frame2_Tot = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnTot)
        self.Frame3_Tot = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnTot)

        self.Frames_Tot_List = [self.Frame1_Tot, self.Frame2_Tot, self.Frame3_Tot]  # the lists of totals
        self.Tot_Frames_Setup()

        # ---------------------------------------------------------------------------------------------
        self.Frame_TotCred     = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnTot)  # the frame for total credits
        self.Credit_Frame_Setup()

        self.Frame_TotDebit = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnTot)  # the frame for total debits
        self.Debit_Frame_Setup()

        self.Frame_Saldo    = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnTot)  # the frame for total number of rows
        self.TotRows_Frame_Setup()

        self.Load_All_Data()

    # ------------------------------------------------------------------------------------------------
    def Load_All_Data(self):
        # here the transactions database is corrrectly loaded from Mod_Manager.py
        self.OneYear_Transact_List = self.Data.Get_Transact_Table()
        self.Setup_Year_Conto_Month_Tot_Date()
        self.Set_All_Selections()
        self.Setup_TR_GR_CA_OptMenu()

        # show the selections for year, conto, month, total months, TR, GR, CA
        self.Show_Selections()
        self.Set_Geometry_Frames()
        self.Set_Widgets_PosX()
        self.Set_Frames_Title()
        self.Set_All_Selections()
        self.Create_Transact_List_perMonth()
        self.Trees_Load()
        pass

    # -------------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:  # Close
            self.Call_OnClose()
        elif Request_Code == CODE_CLK_ON_TR_CODES:
            self.TRcode_Selected_OnTopView(Values_List)  # The Value is Transact_Code
            pass

    # -------------------------------------------------------------------------------------------------
    # Three Frames for transactions view
    def Frames_Setup(self):
        Nrows     = 42
        nColToVis = 7
        Headings  = ['#0', 'Co', 'Contab', 'Valuta', 'Movimento ', 'Entrate ', 'Uscite   ', 'Id']  # TRcode
        Anchor    = ['c',  'c',  'c',      'c',      'w',           'e',        'e',         'c']
        Width     =  [0,    0,    66,       66,       200,           70,         70,          0]

        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        for Frame in self.Frames_List:
            Frame.Tree_Setup_Strech(Form_List, ['#1', '#7'])
            pass

    # -------------------------------------------------------------------------------------------------
    # Three Frames for Total Cred Deb view on each Transactions Frame  view
    def Tot_Frames_Setup(self):
        Nrows     = 1
        nColToVis = 3
        Headings  = ['#0', '      Totale ',  'Entrate  ', 'Uscite  ']
        Anchor    = ['c',  'c',               'e',        'e']
        Width     = [ 0,    180,              100,        100]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        for Frame in self.Frames_Tot_List:
            Frame.Tree_Setup(Form_List)

    # --------------------------------------------------------------------------------------------------
    def TotRows_Frame_Setup(self):
        Nrows     = 1
        nColToVis = 1
        Headings  = ['#0', ' saldo                   ']
        Anchor    = ['c',  'e']
        Width     = [ 0,    125]
        Form_ListT = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Saldo.Tree_Setup(Form_ListT)

    # --------------------------------------------------------------------------------------------------
    def Credit_Frame_Setup(self):
        Nrows     = 1
        nColToVis = 1
        HeadingsC = ['#0', 'totale    entrate  ']
        Anchor    = ['c',  'e']
        Width     = [ 0,    125]
        Form_ListCred     = [Nrows, nColToVis, HeadingsC, Anchor, Width]
        self.Frame_TotCred = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnTot)
        self.Frame_TotCred.Tree_Setup(Form_ListCred)

    # --------------------------------------------------------------------------------------------------
    def Debit_Frame_Setup(self):
        Nrows     = 1
        nColToVis = 1
        HeadingsC = ['#0', 'totale    uscite ']
        Anchor    = ['c',  'e']
        Width     = [ 0,    125]
        Form_ListDeb = [Nrows, nColToVis, HeadingsC, Anchor, Width]
        self.Frame_TotDebit = TheFrame(self, XY_TO_HIDE, 10, self.Click_OnTot)
        self.Frame_TotDebit.Tree_Setup(Form_ListDeb)

    # -------------------------------------------------------------------------------------------------
    def Click_OnTot(self, Value):
        self.Dummy = Value
        self.Frame_Saldo.Clear_Focus()
        self.Frame_TotCred.Clear_Focus()
        self.Frame_TotDebit.Clear_Focus()
        self.Frame1_Tot.Clear_Focus()
        self.Frame2_Tot.Clear_Focus()
        self.Frame3_Tot.Clear_Focus()

    # -------------------------------------------------------------------------------------------------
    def Click_OnFrame(self, Value):
        ViewMesg_Text = '\n *****    TRANSACTION   NOT   FOUND    *****'
        if self.Tot_MonSelected != ONE_MONTH:
            Msg_Dlg = Message_Dlg(MSG_BOX_INFO, 'Please select only one month')
            Msg_Dlg.wait_window()
            return
        Ident = int(Value[IX_QUERY_IDENT])
        RecordFound = self.Data.Get_List_Item_From_Ident(Ident)
        if RecordFound:
            ViewMesg_Text = '-----   Transaction   found   -----\n'
            Index = -1
            for Item in RecordFound:
                Index = Index + 1
                if Index == 6:
                    ViewMesg_Text += "------------------------------------\n"
                ViewMesg_Text += str(Item) + '\n'
            ViewMesg_Text += ' -----------------------------------\n'
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_MESS, TOP_QUERY, [ViewMesg_Text])

   # -------------------------------------------------------------------------------------------------
    def Set_Geometry_Frames(self):
        Geometry_Index       = QUERIES_GEOMETRY_INDEX[ self.Tot_MonSelected]
        self.geometry(TOP_QUERY_GEOMETRY[Geometry_Index])
        self.Widgtes_PosX    = QUERIES_FRAMES_POS_X[Geometry_Index]
        self.nFrames         = QUERIES_NR_FRAMES[ self.Tot_MonSelected]
        self.Months_on_Tree  = QUERIES_NR_MONTHS_BY_TREE[ self.Tot_MonSelected]
        self.iStart_Month    = MONTH_INT[self.Month_Selected]
        self.iTot_Months     = TOT_MONTH_INT[self.Tot_MonSelected]
        self.iEnd_Month      = self.iStart_Month + self.iTot_Months -1
        self.Tot_List        = QUERIES_TOT_DICT[self.Month_Selected]

    # -------------------------------------------------------------------------------------------------
    def Set_Widgets_PosX(self):
        # 10,  XY_TO_HIDE,  XY_TO_HIDE,  450
        PosXok = self.Widgtes_PosX[3]
        self.OptMenu_Year.PosX(PosXok)
        self.OptMenu_Conto.PosX(PosXok)
        self.OptMenu_Start.PosX(PosXok)
        self.OptMenu_Tot.PosX(PosXok)
        self.OptMenu_Tot.SetValues(self.Tot_List)
        self.OptMenu_Date.PosX(PosXok)

        self.OptMenu_TR.PosX(PosXok)
        self.OptMenu_GR.PosX(PosXok)
        self.OptMenu_CA.PosX(PosXok)
        self.OptExclude.PosX(PosXok)
        self.Extraord_Text.PosX(PosXok)
        self.Btn_xlsx_View.SetX(PosXok)

        self.Btn_DB_View.SetX(PosXok)
        self.Btn_Check.SetX(PosXok)
        self.Btn_Exit.SetX(PosXok)

        self.Frame1.Frame_PosXY(self.Widgtes_PosX[0], 10)
        self.Frame2.Frame_PosXY(self.Widgtes_PosX[1], 10)
        self.Frame3.Frame_PosXY(self.Widgtes_PosX[2], 10)
        self.Frame1_Tot.Frame_PosXY(self.Widgtes_PosX[0], 910)
        self.Frame2_Tot.Frame_PosXY(self.Widgtes_PosX[1], 910)
        self.Frame3_Tot.Frame_PosXY(self.Widgtes_PosX[2], 910)

        self.Frame_TotCred.Frame_PosXY(self.Widgtes_PosX[3], 640)
        self.Frame_Saldo.Frame_PosXY(self.Widgtes_PosX[3], 780)      # 640 70
        self.Frame_TotDebit.Frame_PosXY(self.Widgtes_PosX[3],710)

    # -------------------------------------------------------------------------------------------------
    def Set_Frames_Title(self):
        Tit1 = '   ' + self.Month_Selected + '   '
        self.Frame1.Frame_Title(Tit1)
        nextMonth2 = self.iStart_Month + self.Months_on_Tree
        if nextMonth2 <= 12:
            Tit2 = '   ' + MONTHS_NAMES[nextMonth2-1] + '   '
            self.Frame2.Frame_Title(Tit2)
            nextMonth3 = self.iStart_Month  + self.Months_on_Tree *2
            if nextMonth3 <= 12:
                Tit3 = '   ' + MONTHS_NAMES[nextMonth3-1] + '   '
                self.Frame3.Frame_Title(Tit3)

    # -------------------------------------------------------------------------------------------------
    # Check for insert in Transact_xMonth_List (year[Date] Conto (TR GR CA)  return iMonth(0-11)  or -1
    def CheckForInsert(self, Rec):
        # Check for Year    Contabile can be of the next year (Jan: 2026 :  Dec: 2025)
        #                   Valuta can be of the previous year (Jan: 2025 : Dec: 2024)
        DateContab = Rec[IX_TRANSACT_CONTAB]
        DateValuta = Rec[IX_TRANSACT_VALUTA]
        YearContab = int(DateContab[0:4])
        YearValuta = int(DateValuta[0:4])

        # check for year  -------------------------------------------------------
        if YearContab == self.iYear_Selected  or  YearValuta == self.iYear_Selected:
            pass
        else:
            return -1   # quite impossible neither Contab  neither Valuta == year selected

        if self.Date_Selected == CONTAB_DATE:
            Date = DateContab
        else:
            Date = DateValuta
        if int(Date[0:4]) != self.iYear_Selected:
            return -1

        # check for month -------------------------------------------------------
        iMonth = int(Date[5:7]) - 1
        if iMonth < 0 or iMonth > 11:
            return -1

        # Check for Conto -------------------------------------------------------
        if self.Conto_Selected == FIDFLH:
            ContoInDB = Rec[IX_TRANSACT_CONTO]
            if ContoInDB == FIDEU or ContoInDB == FLASH or ContoInDB == POSTA:
                pass
            else:
                return -1
        elif self.Conto_Selected != Rec[IX_TRANSACT_CONTO]:
            return -1

        # Check for TRcode ------------------------------------------------------
        if self.TRselected != ALL_CODES and self.TRselected != '':
            if self.TRselected == Rec[IX_TRANSACT_TR_DESC]:
                pass
            else:
                return -1
        # Check for GRcode ------------------------------------------------------
        GR_CA_List = self.Data.Get_GR_CA_desc_From_TRdesc(Rec[IX_TRANSACT_TR_DESC])
        if self.GRselected != ALL_GROUPS and self.GRselected != '':
            if self.GRselected == GR_CA_List[0]:
                pass
            else:
                return -1
        # Check for CAcode ------------------------------------------------------
        if self.CAselected != ALL_CAT and self.CAselected != '':
            if self.CAselected == GR_CA_List[1]:
                pass
            else:
                return -1
        return iMonth

    # -------------------------------------------------------------------------------------------------
    # Create Transact_xMonth_List on base of Conto, Year, Date, TR, GR, CA
    # On Db      :[nRow    Contab    Valuta    TR_Desc   Accred   Addeb   TRcode]
    # Query view : ['Date', 'Description', 'Credits  ', 'Debits  ']
    # (date based on VALDATE/ACCDATE)  (Conto <- self.ContoSelected)
    # -------------------------------------------------------------------------------------------------
    def Create_Transact_List_perMonth(self):
        self.Transact_xMonth_List = [ [], [], [], [], [], [], [], [], [], [], [], [] ]
        self.Tot_Transact_xMonth  = [0,] * 12
        self.DateCount_PerMonth   = [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0  ]

        self.Extraord_TRcode_List    = self.Data.Get_Extraordinary_List()
        self.OneYear_Transact_purged = []
        for Rec in self.OneYear_Transact_List:
            Exclude_Rec = self.Check_if_Rec_is_to_exclude(Rec)
            if Exclude_Rec:
                pass
            else:
                self.OneYear_Transact_purged.append(Rec)
        Text = "mov. straor. = " + str(len(self.Extraord_TRcode_List))
        self.Extraord_Text.Set_Text(Text)

        # ------------------------------------------
        for Rec in self.OneYear_Transact_purged:
                                                    # **************************************** #
            iMonth = self.CheckForInsert(Rec)       # ***  the heart of records selecting  *** #
                                                    # **************************************** #
            if iMonth >= 0:
                Counts = self.DateCount_PerMonth[iMonth]
                Counts += 1
                if Counts > 10:
                    Counts = 0
                self.DateCount_PerMonth[iMonth] = Counts
                # ['Conto, 'Contab', 'Valuta', 'Description', 'Credits  ', 'Debits  ']
                Contabile = Rec[IX_TRANSACT_CONTAB]
                Valuta    = Rec[IX_TRANSACT_VALUTA]

                DateContab = Set_Month_Day(Contabile, Counts)
                DateValuta = Set_Month_Day(Valuta, Counts)
                TRcode   = Rec[IX_TRANSACT_TR_CODE]
                TRdescr  = self.Data.Get_TrDesc_FromCode(TRcode)
                Conto = CONTO_RED[Rec[IX_TRANSACT_CONTO]]
                # View_Rec = [Date, Conto, TRdescr, Rec[IX_TRANSACT_ACCRED], Rec[IX_TRANSACT_ADDEB], Rec[IX_TRANSACT_IDENT]]
                View_Rec = [Conto, DateContab, DateValuta,  TRdescr, Rec[IX_TRANSACT_ACCRED], Rec[IX_TRANSACT_ADDEB],
                            Rec[IX_TRANSACT_IDENT]]
                self.Transact_xMonth_List[iMonth].append(View_Rec)
                self.Tot_Transact_xMonth[iMonth] += 1
                pass
        pass

    # -------------------------------------------------------------------------------------------------
    def Check_if_Rec_is_to_exclude(self, Rec):
        if self.Excl_Selected == EXTRAORD_INCL:
            return False
        for Excl_TRcode in self.Extraord_TRcode_List:
            TRcode_ToCheck = Rec[IX_TRANSACT_TR_CODE]
            pass
            if TRcode_ToCheck == Excl_TRcode:
                return True     # Exclude
        return False            # NOT exclude

    # -------------------------------------------------------------------------------------------------
    # from Transact_xMonth_List (created on base of Conto,Year, Date, TR, GR, CA)
    def Trees_Load(self):
        Tot_Rec = 0
        Month_Start  = MONTH_INT[self.Month_Selected] - 1
        Total_Months_xTree = self.Months_on_Tree
        Start1 = Month_Start
        End1   = Month_Start + Total_Months_xTree
        Start2 = End1
        End2   = Month_Start + Total_Months_xTree * 2
        Start3 = End2
        End3   = Month_Start + Total_Months_xTree * 3
        Init_End_Months  = [[Start1, End1], [Start2, End2], [Start3, End3]]
        self.Tot_CredDeb_xTree = [[0,   0], [0, 0], [0, 0]]
        #                         Cred Deb
        self.Total_Rows = 0
        for index in range(0, self.nFrames):
            Frame     = self.Frames_List[index]
            Frame_Tot = self.Frames_Tot_List[index]
            Frame_List  = []  #
            Month_Start = Init_End_Months[index][0]
            Month_End   = Init_End_Months[index][1]
            for Ix_Month in range(Month_Start, Month_End):
                for Rec in self.Transact_xMonth_List[Ix_Month]:
                    Query_List = self.Query_List_Setup(Rec)
                    Frame_List.append(Query_List[0])
                    self.Tot_CredDeb_xTree[index][0] += Query_List[1][0]
                    self.Tot_CredDeb_xTree[index][1] += Query_List[1][1]
                    Tot_Rec += 1
            Frame.Load_Row_Values(Frame_List)
            Credit = Float_ToString_Setup(self.Tot_CredDeb_xTree[index][0])
            Debit  = Float_ToString_Setup(self.Tot_CredDeb_xTree[index][1])
            LenList= len(Frame_List)
            self.Total_Rows += LenList
            Tot_Transact = str(LenList) + '   Movimenti '
            Tot_List = [[Tot_Transact, Credit, Debit]]
            Frame_Tot.Load_Row_Values(Tot_List)

        Total_Credit = self.Tot_CredDeb_xTree[0][0] + self.Tot_CredDeb_xTree[1][0] + self.Tot_CredDeb_xTree[2][0]
        Total_Debit  = self.Tot_CredDeb_xTree[0][1] + self.Tot_CredDeb_xTree[1][1] + self.Tot_CredDeb_xTree[2][1]
        strTot_Credit= Float_ToString_Setup(Total_Credit)
        strTot_Debit = Float_ToString_Setup(Total_Debit)
        strSaldo     = Float_ToString_Setup(Total_Credit + Total_Debit)
        self.Frame_TotCred.Load_Row_Values([[strTot_Credit]])
        self.Frame_TotDebit.Load_Row_Values([[strTot_Debit]])
        self.Frame_Saldo. Load_Row_Values([[strSaldo]])

        Title = '     **************       Anno:  ' + str(self.iYear_Selected) +   '       Conto  ' + self.Conto_Selected
        Title += '        Movimenti      ' + str(self.Total_Rows) + '     **************'
        self.title(Title)

    # -------------------------------------------------------------------------------------------------
    # selections for year conto, month, total months, TR, GR, CA
    def Show_Selections(self):
        self.OptMenu_Year.SetSelText(str(self.iYear_Selected))
        self.OptMenu_Conto.SetSelText(self.Conto_Selected)
        self.OptMenu_Start.SetSelText(self.Month_Selected)
        self.OptMenu_Tot.SetSelText(self.Tot_MonSelected)
        self.OptMenu_Date.SetSelText(self.Date_Selected)
        self.OptMenu_TR.SetSelText(self.TRselected)
        self.OptMenu_GR.SetSelText(self.GRselected)
        self.OptMenu_CA.SetSelText(self.CAselected)

# =====================================================================================================
