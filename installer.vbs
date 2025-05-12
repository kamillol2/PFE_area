' Afficher une boîte de dialogue pour demander à l'utilisateur s'il souhaite lancer l'installation
Dim message, title, response
message = "Bonjour, voulez-vous lancer l'installation ?"  ' Message de la boîte de dialogue
title = "Installation"  ' Titre de la boîte de dialogue
response = MsgBox(message, vbYesNo + vbQuestion, title)

' Si l'utilisateur sélectionne "Oui", exécuter le script PowerShell
If response = vbYes Then
    ' Obtenir le chemin du script VBScript
    Dim fso, scriptPath, setupPath
    Set fso = CreateObject("Scripting.FileSystemObject")
    scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)
    
    ' Construire le chemin vers setup_with_gui.ps1
    setupPath = fso.BuildPath(scriptPath, "setup_with_gui.ps1")
    
    ' Exécuter le script PowerShell
    Dim shell
    Set shell = CreateObject("WScript.Shell")
    shell.Run "powershell -ExecutionPolicy Bypass -File """ & setupPath & """", 1, True
End If