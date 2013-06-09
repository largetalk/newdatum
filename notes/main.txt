Sub Main()
    Dim objRegExp As Object
    Dim objMatch As Object
    Dim colMatches As Object
    Dim RetStr As String
    
    Set objRegExp = CreateObject("vbscript.regexp")
    objRegExp.Pattern = "<right>(.*)</right>"
    objRegExp.IgnoreCase = True
    objRegExp.Global = True
    
    Dim objUnderlineRegExp As Object
    Set objUnderlineRegExp = CreateObject("vbscript.regexp")
    objUnderlineRegExp.Pattern = "<underline>(.*)</underline>"
    objUnderlineRegExp.IgnoreCase = True
    objUnderlineRegExp.Global = True
    
    Dim objMergeRegExp As Object
    Set objMergeRegExp = CreateObject("vbscript.regexp")
    objMergeRegExp.Pattern = "<merge>([\S\s]*)</merge>"
    objMergeRegExp.IgnoreCase = True
    objMergeRegExp.Global = True
    
    For Each ws In ThisWorkbook.Worksheets
        For Each cls In ws.Range("A:F").Cells
            If (objRegExp.Test(cls.Value) = True) Then
                cls.Font.Bold = True
                cls.Value = objRegExp.Replace(cls.Value, "$1")
                'Set objMatches = objRegExp.Execute(cls.Value)
                'For Each objMatch In objMatches
                '    cls.Value = objMatch.Value
                'Next
            End If
            If (objUnderlineRegExp.Test(cls.Value) = True) Then
                cls.Value = objUnderlineRegExp.Replace(cls.Value, "$1")
                rs = cls.Row
                Range(Cells(rs, 1), Cells(rs, 6)).Select
                Selection.Borders(xlDiagonalDown).LineStyle = xlNone
                Selection.Borders(xlDiagonalUp).LineStyle = xlNone
                Selection.Borders(xlEdgeLeft).LineStyle = xlNone
                'Selection.Borders(xlEdgeTop).LineStyle = xlNone
                With Selection.Borders(xlEdgeBottom)
                    .LineStyle = xlContinuous
                    .Weight = xlThin
                    .ColorIndex = xlAutomatic
                End With
                Selection.Borders(xlEdgeRight).LineStyle = xlNone
                Selection.Borders(xlInsideVertical).LineStyle = xlNone
            End If
            If (objMergeRegExp.Test(cls.Value) = True) Then
                rs = cls.Row
                Rows(rs + 1).Select
                insertline = CInt((Len(cls.Value) - 14) / 50)
                For i = 1 To insertline
                    Selection.Insert Shift:=xlDown
                Next
                cls.Value = objMergeRegExp.Replace(cls.Value, "$1")
                Range(cls, Cells(rs + insertline, 5)).Select
                With Selection
                    .HorizontalAlignment = xlLeft
                    .VerticalAlignment = xlTop
                    .WrapText = True
                    .Orientation = 0
                    .AddIndent = False
                    .IndentLevel = 0
                    .ShrinkToFit = False
                    .ReadingOrder = xlContext
                    .MergeCells = False
                End With
                Selection.Merge
            End If
        Next

    Next
    
End Sub

Sub Macro1()
'
' Macro1 Macro
' 宏由 bonnie.li 录制，时间: 2010-12-15
'

'
    Range("B307").Select
    ActiveCell.FormulaR1C1 = _
        " She eats lunch <u>at school</u>.（就划线部分提问）<br><br>___ ___ ___ eat lunch?"
    With ActiveCell.Characters(Start:=1, Length:=19).Font
        .Name = "Arial"
        .FontStyle = "常规"
        .Size = 10
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .ColorIndex = xlAutomatic
    End With
    With ActiveCell.Characters(Start:=20, Length:=9).Font
        .Name = "Arial"
        .FontStyle = "常规"
        .Size = 10
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleSingle
        .ColorIndex = xlAutomatic
    End With
    With ActiveCell.Characters(Start:=29, Length:=5).Font
        .Name = "Arial"
        .FontStyle = "常规"
        .Size = 10
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .ColorIndex = xlAutomatic
    End With
    With ActiveCell.Characters(Start:=34, Length:=9).Font
        .Name = "宋体"
        .FontStyle = "常规"
        .Size = 10
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .ColorIndex = xlAutomatic
    End With
    With ActiveCell.Characters(Start:=43, Length:=30).Font
        .Name = "Arial"
        .FontStyle = "常规"
        .Size = 10
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .ColorIndex = xlAutomatic
    End With
    Range("C308").Select
End Sub
