#!/bin/bash
set -e
cd "$(dirname "$0")"
for APP_PYTHON in "$PWD/.venv_mac/bin/python" "$HOME/Desktop/iot_projet/IHM_backup/IHM_TempHumiX_Cours/.venv_mac/bin/python" "$HOME/Desktop/iot_projet/IHM_backup/IHM_TempHumiX/.venv_mac/bin/python" "$HOME/Desktop/iot_projet/IHM/IHM_TempHumiX/.venv_mac/bin/python"; do
  if [ -x "$APP_PYTHON" ]; then
    exec "$APP_PYTHON" main.py
  fi
done
if [ ! -x /opt/homebrew/bin/python3.12 ]; then
  printf 'Installer Python 3.12 Homebrew : brew install python@3.12\n'
  exit 1
fi
/opt/homebrew/bin/python3.12 -m venv .venv_mac
.venv_mac/bin/python -m pip install -r requirements.txt
exec .venv_mac/bin/python main.py
