!include "MUI2.nsh"

Name "MyApp"
OutFile "installer.exe"
InstallDir $PROGRAMFILES\MyApp

Page Directory
Page InstFiles

Section ""
  SetOutPath $INSTDIR
  File /r "dist/windows\*.*"
  CreateShortcut "$DESKTOP\MyApp.lnk" "$INSTDIR\main.exe"
SectionEnd