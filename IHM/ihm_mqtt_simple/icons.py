"""Icônes vectorielles locales, sans police ou ressource réseau."""
from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

PATHS = {
    'overview': '<rect x="3" y="3" width="6" height="6" rx="1.5"/><rect x="13" y="3" width="6" height="6" rx="1.5"/><rect x="3" y="13" width="6" height="6" rx="1.5"/><rect x="13" y="13" width="6" height="6" rx="1.5"/>',
    'history': '<path d="M3 4v15h16M6 14l4-5 4 3 5-7"/>',
    'hardware': '<rect x="6" y="6" width="10" height="10" rx="2"/><path d="M9 2v4m4-4v4M9 16v4m4-4v4M2 9h4m-4 4h4m10-4h4m-4 4h4"/>',
    'settings': '<path d="M4 6h14M4 16h14"/><circle cx="8" cy="6" r="3" fill="white"/><circle cx="14" cy="16" r="3" fill="white"/>',
    'logs': '<rect x="4" y="3" width="14" height="17" rx="2"/><path d="M8 8h6m-6 4h6m-6 4h3"/>',
    'play': '<path d="M8 5l9 6-9 6z"/>',
    'pause': '<path d="M8 5v12m6-12v12"/>',
}

def icon(name, color):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" '
           f'fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" '
           f'stroke-linejoin="round">{PATHS[name]}</svg>')
    renderer = QSvgRenderer(QByteArray(svg.encode()))
    result = QIcon()
    for size in (18, 36, 54):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        result.addPixmap(pixmap)
    return result
