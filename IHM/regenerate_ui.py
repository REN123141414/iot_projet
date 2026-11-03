"""§4.4 et §6.3 : convertir les fichiers Designer avec le même Python."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
tool = Path(sys.executable).parent / ('pyside6-uic.exe' if sys.platform == 'win32' else 'pyside6-uic')
if not tool.is_file():
    raise SystemExit('Activer l’interpréteur du projet et installer PySide6.')
for ui in sorted(root.rglob('*.ui')):
    if any(part.startswith('.') for part in ui.relative_to(root).parts):
        continue
    subprocess.run([str(tool), str(ui), '-o', str(ui.with_suffix('.py'))], check=True)
    print(ui.relative_to(root))
