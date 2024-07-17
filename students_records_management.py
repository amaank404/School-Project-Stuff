import sqlite3
import colorama
import pyfiglet
import sys

colorama.init()

db = sqlite3.connect("students.db")
cur = db.cursor()

cur.executescript(
"""
CREATE TABLE IF NOT EXISTS records (
    student_id INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    grades VARCHAR(255)
);
"""
)

def transform_to_dict(st):
    return {x.split('=', 1)[0]: x.split('=', 1)[1] for x in st.split(', ')}

def transform_to_str(dc):
    return ', '.join(f"{k}={v}" for k, v in dc.items())

def new_record():
    student_id = int(input("ID  >"))
    name = input("NAME> ")
    grades = get_grades()

    cur.execute("INSERT INTO records (student_id, name, grades) VALUES (?, ?, ?)", (student_id, name, grades))
    db.commit()


def display_record():
    cur.execute("SELECT * FROM records ORDER BY student_id ASC")
    print_row("Student ID", "Name", "Grades")
    for (stid, name, grades) in cur:
        print_row(stid, name, grades)


def update_record():
    student_id = int(input("ID> "))
    cur.execute("SELECT name, grades FROM records WHERE student_id=?", (student_id,))
    name, grades = cur.fetchone()
    grades = transform_to_dict(grades)
    print("Name:", colorama.Style.BRIGHT+name+colorama.Style.RESET_ALL)
    for k, v in grades.items():
        print(f"{k.rjust(20)} := {v}")
    grades.update(transform_to_dict(get_grades()))
    g = transform_to_str(grades)
    cur.execute("UPDATE records SET grades=? WHERE student_id=?", (g, student_id))
    db.commit()

def print_row(stid, name, grades):
    print(
        colorama.ansi.Fore.RED+str(stid).rjust(10)+colorama.ansi.Fore.RESET, 
        colorama.ansi.Style.BRIGHT+name.ljust(20)+colorama.ansi.Style.RESET_ALL,
        grades
    )


def get_grades():
    grades = {}
    while (sub := input("\nSubject (leave empty to finish)> ")):
        grade = input("Grade> ")
        grades[sub] = grade

    return transform_to_str(grades)


def main():
    pyfiglet.print_figlet("Student Records")
    while True:
        print(
"""
1. Add new record
2. Display records
3. Update existing record
4. Quit
"""
        )
        opt = input(">")
        match opt:
            case "1":
                new_record()
            case "2":
                display_record()
            case "3":
                update_record()
            case "4":
                sys.exit(1)

if __name__ == "__main__":
    main()