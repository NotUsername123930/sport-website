@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" news_import.py >> news_update.log 2>&1