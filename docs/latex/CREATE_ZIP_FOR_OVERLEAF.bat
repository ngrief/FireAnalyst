@echo off
echo Creating ZIP file for Overleaf...
echo.

REM Create temporary directory
if exist temp_overleaf rmdir /s /q temp_overleaf
mkdir temp_overleaf

REM Copy necessary files
copy findings_report.tex temp_overleaf\
copy fires_over_time.png temp_overleaf\
copy peak_years_for_fires.png temp_overleaf\
copy seasonality.png temp_overleaf\
copy cause_distribution.png temp_overleaf\
copy containment_effectiveness.png temp_overleaf\

REM Create ZIP using PowerShell
powershell Compress-Archive -Path temp_overleaf\* -DestinationPath FireAnalyst_Report.zip -Force

REM Cleanup
rmdir /s /q temp_overleaf

echo.
echo SUCCESS! Created: FireAnalyst_Report.zip
echo.
echo Now:
echo 1. Go to https://www.overleaf.com/
echo 2. Click "New Project" -^> "Upload Project"
echo 3. Upload FireAnalyst_Report.zip
echo 4. Click "Recompile"
echo 5. Download your PDF!
echo.
pause
