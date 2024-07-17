import sqlite3
import datetime
import colorama
import pyfiglet

colorama.init()

db = sqlite3.connect("diary.db")
cur = db.cursor()

cur.executescript(
"""
CREATE TABLE IF NOT EXISTS diary_entries (
    id INTEGER PRIMARY KEY NOT NULL,
    timestamp DATETIME,
    title VARCHAR(200),
    content BLOB
);
"""
)
def get_new_entry():
    """
    returns (title, content, timestamp)
    """
    print("\nDiary Entry")
    print("============")
    print(colorama.Style.BRIGHT+"Type in '.' (period) to finish writing!\n"+colorama.Style.RESET_ALL)
    title = input("Title> ")
    print(f"Timestamp> {get_current_timestamp()}")
    content = []
    i = 0
    while True:
        i += 1
        d = input(f"{str(i).rjust(3)}> ")
        if d == '.':
            return (title, '\n'.join(content), get_current_timestamp())
        else:
            content.append(d)
    

def get_current_timestamp():
    """
    SQL appropriate date time
    """
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt

def display_entry(id):
    print("\n"+"="*36)
    cur.execute("SELECT timestamp, title, content FROM diary_entries WHERE id=?", (id,))
    timestamp, title, content = cur.fetchone()
    print(colorama.Style.BRIGHT + title.center(36))
    print(timestamp.center(36))
    print(colorama.Style.NORMAL)
    print(content)
    print("="*36)
    input(colorama.Style.BRIGHT+"Press Enter to continue"+colorama.Style.RESET_ALL)

def search_by_date(date):
    cur.execute("SELECT id, timestamp, title FROM diary_entries WHERE date(timestamp)=? ORDER BY timestamp ASC", (date,))
    ids = []
    for i, (id, timestamp, title) in enumerate(cur):
        ids.append(id)
        print(f"{i+1} {colorama.Fore.RED}{timestamp}{colorama.Fore.RESET}{colorama.Style.BRIGHT} {title} {colorama.Style.RESET_ALL}")

    return ids

def list_entries():
    cur.execute("SELECT id, timestamp, title FROM diary_entries ORDER BY timestamp ASC")
    ids = []
    for i, (id, timestamp, title) in enumerate(cur):
        ids.append(id)
        print(f"{i+1} {colorama.Fore.RED}{timestamp}{colorama.Fore.RESET}{colorama.Style.BRIGHT} {title} {colorama.Style.RESET_ALL}")

    return ids

def main():
    pyfiglet.print_figlet("Diary Manager")
    while True:
        print(
"""
1> Write a new entry
2> Search entries by date
3> List entries
4> Quit
"""
        )
        opt = input(">")
        match opt:
            case "1":
                title, content, timestamp = get_new_entry()
                cur.execute("INSERT INTO diary_entries (title, content, timestamp) VALUES (?,?,?)", (title, content, timestamp))
                db.commit()
            case "2":
                date = input("Date (YY-MM-DD)> ")
                ids = search_by_date(date)
                if not ids:
                    print(colorama.Fore.BLUE+"No entries found"+colorama.Fore.RESET)
                    continue
                entry_id = input("Entry to view> ")
                if entry_id.isnumeric():
                    display_entry(ids[int(entry_id)-1])
            case "3":
                ids = list_entries()
                if not ids:
                    print(colorama.Fore.BLUE+"No entries found"+colorama.Fore.RESET)
                    continue
                entry_id = input("Entry to view> ")
                if entry_id.isnumeric():
                    display_entry(ids[int(entry_id)-1])
            case "4":
                break

if __name__ == "__main__":
    main()