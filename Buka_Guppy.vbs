Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

strPath = fso.GetParentFolderName(WScript.ScriptFullName)
batPath = strPath & "\run_guppy.bat"

If fso.FileExists(batPath) Then
    WshShell.CurrentDirectory = strPath
    WshShell.Run """" & batPath & """", 1, False
Else
    MsgBox "File run_guppy.bat tidak ditemukan di folder ini!" & vbCrLf & vbCrLf & "Pastikan Anda telah mengekstrak file ZIP hasil unduhan Google Drive sepenuhnya.", 16, "Guppy Launcher"
End If
