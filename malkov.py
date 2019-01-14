import sqlite3
import MeCab

class Malkov_na_sqlite:
    def __init__(self, cursor):
        self.cursor = cursor

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

    lines = get_lines_from_a_file("./data.txt")
    for line in lines:
        mal.insert(line)

    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()


