@echo off
cd /d "%~dp0.."
python scripts\nightly_window.py >> data\email.log 2>&1
