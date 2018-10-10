'在oContentwks中查找Olookwks的疾病名称
'别名查找功能：第一列为主疾病名称，查找到别名记为主名称
Sub findName()
    Dim sContent$, sWhat$, sAddress$, iRow%, iNameCol%, iMaxCol%
    Dim oContent As Range, oLook As Range, oResult As Range
    Dim oContentwks As Worksheet, oLookwks As Worksheet
    
    '疾病字典所在的wks
    Set oLookwks = Workbooks("2016WHO中枢神经系统肿瘤分类.xlsx").Worksheets("Sheet1")
    '诊断内容所在的wks
    Set oContentwks = Workbooks("脑肿瘤.xlsm").Worksheets("Sheet1")
    '诊断内容所在列
    Set oContentRange = oContentwks.Range("G:G")
    '同义词最长列
    iMaxCol = 15
    
    For iRow = 1 To oLookwks.Cells(1, 1).End(xlDown).Row '遍历疾病字典
        '从第一列开始遍历同义词
        For iNameCol = 1 To oLookwks.Cells(iRow, iMaxCol).End(xlToLeft).Column
            sWhat = oLookwks.Cells(iRow, iNameCol).Value
            If sWhat <> "" Then
                Debug.Print ("寻找：" & sWhat)
                Set oResult = oContentRange.Find(sWhat)
                If oResult Is Nothing Then
                    Debug.Print ("未找到")
                Else
                    sAddress = oResult.Address
                    Do
                        Set oResult = oContentwks.Range("G:G").FindNext(oResult)
                        '在诊断右侧空格依次写入找到的疾病名称
                        oContentwks.Cells(oResult.Row, 1).End(xlToRight).Offset(0, 1).Value = oLookwks.Cells(iRow, 1).Value
                        Debug.Print ("行：" & oResult.Row)
                    Loop Until oResult.Address = sAddress
                End If
            End If
        Next
    Next
    Debug.Print ("任务完成")
End Sub

