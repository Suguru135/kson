import sqlite3
import MeCab

import random

class Malkov_na_sqlite:
    def __init__(self, cursor):
        self.cursor = cursor

    def reset(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS malkov")
            self.cursor.execute("CREATE TABLE malkov (prefix TEXT NOT NULL, prefix2 TEXT NOT NULL, suffix TEXT NOT NULL)")


        except sqlite3.Error as e:
            print("init: ", e)


    def insert(self, line):
        w1 = line[0]
        w2 = line[1]
        w3 = line[2]

        try:
            self.cursor.execute("INSERT INTO malkov VALUES (?, ?, ?)", (w1, w2, w3))

        except sqlite3.Error as e:
            print("insert: ", e)


        if line[3:] == []:
            return True

        else:
            return self.insert(line[1:])


    def remake(self, word):
        self.cursor.execute("SELECT * FROM malkov WHERE prefix=?", (word,))
        results = self.cursor.fetchall()

        if results == []:
            return ""

        else:
            prefix, prefix2, suffix = random.choice(results)
            return prefix2 + suffix + self.remake(suffix)

def get_lines_from_a_file(fname):
    m = MeCab.Tagger("-Owakati")

    lines = []

    with open(fname, "r") as f:
        for line in f:
            lines.append(m.parse(line).split(" "))

    return lines



def main():
    conn = sqlite3.connect("kson.db")
    cursor = conn.cursor()

    mal = Malkov_na_sqlite(cursor)
    mal.reset()

    lines = get_lines_from_a_file("./data.txt")
    for line in lines:
        mal.insert(line)

    conn.commit()


    keyword = "努力"
    print(">" + keyword + mal.remake(keyword))


    conn.close()



if __name__ == "__main__":
    main()


