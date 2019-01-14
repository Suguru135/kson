import MeCab
import sqlite3

import malkov


def main():
    conn = sqlite3.connect("kson.db")
    cursor = conn.cursor()

    mal = malkov.Malkov_na_sqlite(cursor)

    lines = malkov.get_lines_from_a_file("./data.txt")
    for line in lines:
        mal.insert(line)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()


