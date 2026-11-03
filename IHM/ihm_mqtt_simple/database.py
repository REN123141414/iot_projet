"""Lecture SQLite par l’IHM ; l’écriture appartient au ClientMQTT (§5)."""
from pathlib import Path
import sqlite3


class Database:
    def __init__(self, path):
        path = Path(path)
        self.conn = (sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True, timeout=5)
                     if path.is_file() else None)

    def count(self, sid=None):
        if self.conn is None:
            return 0
        if sid is None:
            return self.conn.execute('SELECT COUNT(*) FROM IOT_DATA').fetchone()[0]
        return self.conn.execute('SELECT COUNT(*) FROM IOT_DATA WHERE Id_capteur=?', (sid,)).fetchone()[0]

    def latest(self, sid):
        if self.conn is None:
            return None
        row = self.conn.execute('SELECT Id_capteur, Date, Version, Temperature, Humidite '
            'FROM IOT_DATA WHERE Id_capteur=? ORDER BY Date DESC, rowid DESC LIMIT 1', (sid,)).fetchone()
        if row is None:
            return None
        return dict(zip(('sensor_id', 'date', 'version', 'temperature', 'humidity'), row))

    def recent(self, sid):
        if self.conn is None:
            return []
        rows = self.conn.execute('SELECT Date, Temperature, Humidite FROM IOT_DATA '
            'WHERE Id_capteur=? ORDER BY Date DESC, rowid DESC LIMIT 30', (sid,)).fetchall()
        return list(reversed(rows))

    def query(self, sid, start, end):
        if self.conn is None:
            return []
        return self.conn.execute('SELECT Date, Temperature, Humidite FROM IOT_DATA '
            'WHERE Id_capteur=? AND Date BETWEEN ? AND ? ORDER BY Date ASC', (sid, start, end)).fetchall()

    def close(self):
        if self.conn is not None:
            self.conn.close()
