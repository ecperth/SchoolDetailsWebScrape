Sub PullSchoolCodes()

    OutputFileNum = FreeFile
    codes = ""

    Set wb = Workbooks.Open("C:\Users\Eoghan\Desktop\Programs\schoolDataScrape/SchoolsList.xlsx")
    Open "C:\Users\Eoghan\Desktop\Programs\schoolDataScrape/school_codes.csv" For Output Lock Write As #OutputFileNum
      
    FirstRow = InputBox("line of first school code:", "First school code")
        
    wsLR = Cells(Rows.Count, "A").End(xlUp).Row - 1
    Range("A" & wsLR).Select
            
    LastRow = InputBox("line of Last school code:", "Last school code")
    Column = InputBox("Column of school codes:", "School codes column")
    For x = FirstRow To LastRow - 1
        codes = codes + Range(Column + CStr(x)).Value & ","
    Next x
    codes = codes + Range(Column + CStr(LastRow)).Value
    Print #OutputFileNum, codes
        
    Close #OutputFileNum
    wb.Close (False)
    
End Sub