import sqlite3
from datetime import datetime

def zapis(fraza):
    try:
        print("Wyszukiwana fraza " + fraza + "...")
        db = sqlite3.connect('gbif.db')
        db.row_factory = sqlite3.Row
        datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        kursor = db.cursor()
        kursor.execute(
            """
            INSERT INTO WYSZUKANIA (fraza, data_wyszukania)
            VALUES (?,?)
            """, (fraza, datetime_now))
        db.commit()
        db.close()
        print("Dodano frazę do bazy danych")
        return True
    except:
        print("Nie dodano, wystąpił błąd")
        return False
