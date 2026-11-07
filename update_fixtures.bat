@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" main.py >> fixtures_update.log 2>&1