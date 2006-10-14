# Script generated by the HM NIS Edit Script Wizard.

# HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Maestro"
!define PRODUCT_VERSION "0.1.0"
!define FILE_VERSION "${PRODUCT_VERSION}.1"
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
#!insertmacro MUI_PAGE_COMPONENTS
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

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  # What about a stanza.ico?
  File /r /x .svn /x dist /x doc /x pyqt_ext /x test /x playpen infiscape_maestro.ico ensemble.ico maestro\*
  File /r /x .svn /x *.mk /x Makefile /x *.xml maestro\doc
  Call SetStartMenuToUse
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"

  # Associate .ensem files with the Maestro GUI.
  Push ".ensem"
  Push "Maestro Ensemble"
  Push "Ensemble File"
  Push "$INSTDIR\ensemble.ico"
  Push "Load Ensemble into Maestro"
  # XXX: This path to python.exe should not be hard coded!
  Push 'C:\Python24\python.exe "$OUTDIR\Maestro.py" "%1"'
  Call FileAssociation
  Call RefreshShellIcons
SectionEnd

Section -AdditionalIcons
  Call SetStartMenuToUse

  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Documentation (PDF).lnk" "$INSTDIR\doc\userguide.pdf"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Documentation (HTML).lnk" "$INSTDIR\doc\userguide\index.html"

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

  ReadRegStr $1 HKCR ".ensem" ""
  WriteRegStr HKCR "$1\shell" "" "MaestroEnsemble"

  # XXX: This path to python.exe should not be hard coded!
  ExecWait 'C:\Python24\python.exe "$INSTDIR\maestrod.py" --interactive install' $0
  DetailPrint "Installing the Maestro service returned $0"
  # XXX: This path to python.exe should not be hard coded!
  Exec 'C:\Python24\python.exe "$INSTDIR\maestrod.py" start'
SectionEnd

# Descriptions
#LangString DESC_SecService ${LANG_ENGLISH} \
#   "Maestro service (required for all non-client cluster nodes)."
#LangString DESC_SecGUI ${LANG_ENGLISH} \
#   "Maestro client grahpical user interface application."
#LangString DESC_SecDoc ${LANG_ENGLISH} \
#   "Maestro documentation in HTML and PDF formats."
#
#!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
#   !insertmacro MUI_DESCRIPTION_TEXT ${SecService} $(DESC_SecService)
#   !insertmacro MUI_DESCRIPTION_TEXT ${SecGUI} $(DESC_SecGUI)
#   !insertmacro MUI_DESCRIPTION_TEXT ${SecDoc} $(DESC_SecDoc)
#!insertmacro MUI_FUNCTION_DESCRIPTION_END

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

  # XXX: This path to python.exe should not be hard coded!
  ExecWait 'C:\Python24\python.exe "$INSTDIR\maestrod.py" stop' $0
  DetailPrint "Stopping the Maestro service returned $0"
  # XXX: This path to python.exe should not be hard coded!
  ExecWait 'C:\Python24\python.exe "$INSTDIR\maestrod.py" remove' $0
  DetailPrint "Removing the Maestro service returned $0"

  RMDir /R "$SMPROGRAMS\${PRODUCT_NAME}"
  RMDir /R /REBOOTOK "$INSTDIR\"

  Push ".ensem"
  Push "Maestro Ensemble"
  Call un.RemoveFileAssociation
  Call un.RefreshShellIcons

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd
