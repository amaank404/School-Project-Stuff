import sqlite3
import colorama
import pyfiglet
import datetime

colorama.init()

db = sqlite3.connect("library_management.db")
cur = db.cursor()
# cur.execute("DROP table books")
# cur.execute("DROP table transactions")

cur.executescript(
"""
CREATE TABLE IF NOT EXISTS books(
    bookid INTEGER PRIMARY KEY NOT NULL,
    title VARCHAR(50) NOT NULL,
    author VARCHAR(50),
    available CHAR(1) DEFAULT 'y'
);

CREATE TABLE IF NOT EXISTS transactions(
    tid INTEGER PRIMARY KEY NOT NULL,
    uid INT NOT NULL,
    bookid INT NOT NULL,
    transaction_type CHAR(1) NOT NULL,
    timestamp DATETIME NOT NULL
);
"""
)

checkmark = colorama.ansi.Fore.GREEN+"✔"+colorama.ansi.Fore.RESET
crossmark = colorama.ansi.Fore.RED+"✘"+colorama.Fore.RESET

def add_book(title, author):
    cur.execute("INSERT INTO books (title, author) VALUES (?,?)", (title, author))
    db.commit()

def view_book(bid, history = True):
    cur.execute("SELECT title, author, available FROM books WHERE bookid=? LIMIT 1", (bid, ))
    print_row(bid, *(m := cur.fetchone()))
    if history:
        cur.execute("SELECT timestamp, uid, transaction_type FROM transactions WHERE bookid=?", (bid, ))
        res = cur.fetchall()
        if not res:
            print("No Transaction History")
        else:
            print("Timestamp".ljust(20), "User ID".ljust(10), "Transaction Type")
            for (tstamp, uid, ttype) in res:
                print(tstamp.ljust(20), str(uid).ljust(10), "Borrow" if ttype == "b" else "Return")
    return m[-1]

def list_books():
    cur.execute("SELECT bookid, title, author, available FROM books")
    print_row("BID", "Title", "By", "Available")
    for (book_id, title, author, available) in cur:
        print_row(book_id, title, author, available)

def print_row(bid, title, author, avail):
    print(
        colorama.Fore.BLUE+str(bid).rjust(5)+colorama.Fore.RESET,
        colorama.Style.BRIGHT+title.ljust(30)+colorama.Style.RESET_ALL,
        author.ljust(20),
        checkmark if avail == 'y' else (crossmark if avail == "n" else avail)
    )

def set_avail(bid, avail):
    cur.execute("UPDATE books SET available=? WHERE bookid=?", (avail, bid))

def get_current_timestamp():
    """
    SQL appropriate date time
    """
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt


def record_transaction(uid, bid, ttype):
    cur.execute("INSERT INTO transactions (uid, bookid, transaction_type, timestamp) VALUES (?, ?, ?, ?)", (uid, bid, ttype, get_current_timestamp()))

def main():
    pyfiglet.print_figlet("Library!")
    while True:
        print(
"""
1. Add New Book
2. List Books
3. View Book
4. Borrow Book
5. Return Book
6. Quit
"""
        )
        opt = input("> ")
        match opt:
            case "1":
                title = input("Title> ")
                author = input("By> ")
                add_book(title, author)
            case "2":
                list_books()
            case "3":
                bid = int(input("Book ID> "))
                view_book(bid)
            case "4":
                bid = int(input("Book ID> "))
                uid = int(input("User ID> "))
                avail = view_book(bid, history=False)
                if avail == 'n':
                    print("Book not available")
                else:
                    set_avail(bid, "n")
                    record_transaction(uid, bid, 'b')
                    print("Book Borrowed")
                    db.commit()
            case "5":
                bid = int(input("Book ID> "))
                uid = int(input("User ID> "))
                avail = view_book(bid, history=False)
                if avail == 'y':
                    print("Book already available")
                else:
                    set_avail(bid, "y")
                    record_transaction(uid, bid, 'r')
                    print("Book Returned!")
                    db.commit()
            case "6":
                return
            
if __name__ == '__main__':
    main()
