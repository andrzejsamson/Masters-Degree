import sqlite3
from datetime import datetime

def wczytanie(fraza):
    try:
        print("Wczytywana fraza " + fraza + "...")
        db = sqlite3.connect('gbif.db')
        db.row_factory = sqlite3.Row
        kursor = db.cursor()
        kursor.execute(
            """
            SELECT data_wyszukania FROM WYSZUKANIA
            WHERE fraza = ?
            ORDER BY data_wyszukania DESC
            """, [fraza])
        wpis = kursor.fetchone()
        db.close()
        print(wpis[0])
        return wpis[0]
    except:
        print("Podana fraza nie występuje w bazie")
        return None
