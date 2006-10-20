# Script generated by the HM NIS Edit Script Wizard.

# HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Maestro"
!define PRODUCT_VERSION "0.2.0"
!define FILE_VERSION "${PRODUCT_VERSION}.0"
!define PRODUCT_PUBLISHER "Infiscape Corporation"
!define PRODUCT_WEB_SITE "http://realityforge.vrsource.org/trac/maestro/"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\maestro.py"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

#SetCompressor lzma
SetCompressor bzip2
!define ALL_USERS "1"

# MUI 1.67 compatible ------
!include "MUI.nsh"
!include WriteEnvStr.nsh
!include FileAssociation.nsh
!include StartMenu.nsh
!include "Sections.nsh"
!include "LogicLib.nsh"

# MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "infiscape_maestro.ico"
!define MUI_UNICON "infiscape_maestro.ico"

# Welcome page
!insertmacro MUI_PAGE_WELCOME
# Components page
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE ComponentLeaveFunc
!insertmacro MUI_PAGE_COMPONENTS
# Directory page
!insertmacro MUI_PAGE_DIRECTORY
# Instfiles page
!insertmacro MUI_PAGE_INSTFILES
# Finish page
!insertmacro MUI_PAGE_FINISH

# Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

# Language files
!insertmacro MUI_LANGUAGE "English"

# Variables
Var GUI_INST
Var SERVICE_INST
Var DOC_INST

# MUI end ------

Name "Maestro ${PRODUCT_VERSION}"
OutFile "Maestro ${PRODUCT_VERSION} Setup.exe"
InstallDir "$PROGRAMFILES\Infiscape\Maestro ${PRODUCT_VERSION}"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails hide
ShowUnInstDetails hide
BrandingText "Maestro ${PRODUCT_VERSION} Installer by Infiscape Corporation"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "${PRODUCT_NAME}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "${PRODUCT_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "Infiscape Corporation © 2006"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${FILE_VERSION}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "Maestro Installer"
VIProductVersion "${FILE_VERSION}"

!define SHCNE_ASSOCCHANGED 0x08000000
!define SHCNF_IDLIST 0

Function RefreshShellIcons
  # By jerome tremblay - april 2003
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v \
  (${SHCNE_ASSOCCHANGED}, ${SHCNF_IDLIST}, 0, 0)'
FunctionEnd

Section "!Maestro Core" SecCore
  SectionIn RO
  SetOverwrite ifnewer
  SetOutPath "$INSTDIR\maestro\core"
  File /r /x .svn maestro\maestro\core\*
  SetOutPath "$INSTDIR\maestro\util"
  File /r /x .svn maestro\maestro\util\*
  SetOutPath "$INSTDIR\maestro"
  File maestro\maestro\__init__.py
  SetOutPath "$INSTDIR"
  File /r core_deps\*

  Call SetStartMenuToUse
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
SectionEnd

Section "Maestro GUI" SecGUI
  SetOverwrite ifnewer
  SetOutPath "$INSTDIR\maestro\gui"
  #File /r /x .svn /x dist /x doc /x pyqt_ext /x test /x playpen infiscape_maestro.ico ensemble.ico stanza.ico maestro\gui\*
  File /r maestro\maestro\gui\* 

  SetOutPath "$INSTDIR\stanzas"
  File /r /x .svn maestro\stanzas\* 

  SetOutPath "$INSTDIR"
  File maestro\cluster.ensem maestro\LICENSE.txt maestro\Maestro.py maestro\maestrod.py maestro\maestrod.xcfg maestro\server.pem
  File infiscape_maestro.ico ensemble.ico stanza.ico
  File /r gui_deps\*

  # Associate .ensem files with the Maestro GUI.
  Push ".ensem"
  Push "MaestroEnsemble"
  Push "Ensemble File"
  Push "$INSTDIR\ensemble.ico"
  Push "Load Ensemble into Maestro"
  # XXX: This path to python.exe should not be hard coded!
  Push 'C:\Python24\python.exe "$OUTDIR\Maestro.py" "%1"'
  Call FileAssociation

  # Associate .stanza files with the Maestro GUI.
  Push ".stanza"
  Push "MaestroStanza"
  Push "Stanza File"
  Push "$INSTDIR\stanza.ico"
  Push "Load Stanza into Maestro"
  # XXX: This path to python.exe should not be hard coded!
  Push 'C:\Python24\python.exe "$OUTDIR\Maestro.py" -s "%1" -v "Launch View"'
  Call FileAssociation

  Call RefreshShellIcons
SectionEnd

Section "Maestro Service" SecService
  SetOverwrite ifnewer
  SetOutPath "$INSTDIR\maestro\daemon"
  File /r /x .svn maestro\maestro\daemon\*
  SetOutPath "$INSTDIR"
  File maestro\maestrod.py
SectionEnd

Section "Maestro Documentation" SecDoc
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File /r /x .svn /x *.mk /x Makefile /x *.xml /x README.txt maestro\doc
SectionEnd

Section -AdditionalIcons
  Call SetStartMenuToUse

  ${If} $GUI_INST == '1'
    CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Maestro.lnk" "$INSTDIR\Maestro.py" '' "$INSTDIR\infiscape_maestro.ico"
  ${EndIf}

  ${If} $DOC_INST == '1'
    CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\User Guide (PDF).lnk" "$INSTDIR\doc\userguide.pdf"
    CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\User Guide (HTML).lnk" "$INSTDIR\doc\userguide\index.html"
  ${EndIf}

  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"

  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\Maestro.py"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\Maestro.py"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"

  ${If} $GUI_INST == '1'
    ReadRegStr $1 HKCR ".ensem" ""
    WriteRegStr HKCR "$1\shell" "" "MaestroEnsemble"

    ReadRegStr $1 HKCR ".stanza" ""
    WriteRegStr HKCR "$1\shell" "" "MaestroStanza"
  ${EndIf}

  ${If} $SERVICE_INST == '1'
    # XXX: This path to python.exe should not be hard coded!
    ExecWait 'C:\Python24\python.exe "$INSTDIR\maestrod.py" --interactive --startup auto install' $0
    DetailPrint "Installing the Maestro service returned $0"
    # XXX: This path to python.exe should not be hard coded!
    Exec 'C:\Python24\python.exe "$INSTDIR\maestrod.py" start'
  ${EndIf}
SectionEnd

# Descriptions
LangString DESC_SecCore ${LANG_ENGLISH} \
   "Maestro core (required for both GUI and service)."
LangString DESC_SecService ${LANG_ENGLISH} \
   "Maestro service (required for all non-client cluster nodes)."
LangString DESC_SecGUI ${LANG_ENGLISH} \
   "Maestro client grahpical user interface application."
LangString DESC_SecDoc ${LANG_ENGLISH} \
   "Maestro documentation in HTML and PDF formats."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
   !insertmacro MUI_DESCRIPTION_TEXT ${SecCore} $(DESC_SecCore)
   !insertmacro MUI_DESCRIPTION_TEXT ${SecService} $(DESC_SecService)
   !insertmacro MUI_DESCRIPTION_TEXT ${SecGUI} $(DESC_SecGUI)
   !insertmacro MUI_DESCRIPTION_TEXT ${SecDoc} $(DESC_SecDoc)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "Maestro was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove Maestro and all of its components?" IDYES +2
  Abort
FunctionEnd

Function un.RefreshShellIcons
  # By jerome tremblay - april 2003
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v \
  (${SHCNE_ASSOCCHANGED}, ${SHCNF_IDLIST}, 0, 0)'
FunctionEnd

Section Uninstall
  Call un.SetStartMenuToUse

  ${If} $SERVICE_INST == '1'
    # XXX: This path to python.exe should not be hard coded!
    ExecWait 'C:\Python24\python.exe "$INSTDIR\maestrod.py" stop' $0
    DetailPrint "Stopping the Maestro service returned $0"
    # XXX: This path to python.exe should not be hard coded!
    ExecWait 'C:\Python24\python.exe "$INSTDIR\maestrod.py" remove' $0
    DetailPrint "Removing the Maestro service returned $0"
  ${EndIf}

  RMDir /R "$SMPROGRAMS\${PRODUCT_NAME}"
  RMDir /R /REBOOTOK "$INSTDIR\"

  ${If} $GUI_INST == '1'
    Push ".ensem"
    Push "MaestroEnsemble"
    Call un.RemoveFileAssociation

    Push ".stanza"
    Push "MaestroStanza"
    Call un.RemoveFileAssociation

    Call un.RefreshShellIcons
  ${EndIf}

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd

Function ComponentLeaveFunc

  !insertmacro SectionFlagIsSet ${SecGUI} ${SF_PSELECTED} guiIsSel guiChkAll
  guiChkAll:
  !insertmacro SectionFlagIsSet ${SecGUI} ${SF_SELECTED} guiIsSel guiNotSel
    guiIsSel:
      StrCpy $GUI_INST "1"
      Goto guiEnd
    guiNotSel:
      StrCpy $GUI_INST "0"
  guiEnd:

  !insertmacro SectionFlagIsSet ${SecDoc} ${SF_PSELECTED} docIsSel docChkAll
  docChkAll:
  !insertmacro SectionFlagIsSet ${SecDoc} ${SF_SELECTED} docIsSel docNotSel
    docIsSel:
      StrCpy $DOC_INST "1"
      Goto docEnd
    docNotSel:
      StrCpy $DOC_INST "0"
  docEnd:

  !insertmacro SectionFlagIsSet ${SecService} ${SF_PSELECTED} svcIsSel svcChkAll
  svcChkAll:
  !insertmacro SectionFlagIsSet ${SecService} ${SF_SELECTED} svcIsSel svcNotSel
    svcIsSel:
      StrCpy $SERVICE_INST "1"
      Goto svcEnd
    svcNotSel:
      StrCpy $SERVICE_INST "0"
  svcEnd:

FunctionEnd
