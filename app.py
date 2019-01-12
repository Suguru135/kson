import MeCab
import sqlite3


def main():
    words = get_text("./data.txt")

    dbpath = 'kson.sqlite'
    conn = sqlite3.connect(dbpath)

    cursor = conn.cursor()

    try:
        cursor.execute("DROP TABLE IF EXISTS malkov")
        cursor.execute("CREATE TABLE malkov (prefix TEXT NOT NULL, prefix2 TEXT NOT NULL, suffix TEXT NOT NULL)")


        for line in words:
            if malkov_v_sql(cursor, line):
                print("ok")

            else:
                print("err")

    except sqlite3.Error as e:
        print("sqlErr: ", e.args[0])
    conn.commit()
    conn.close()


def get_text(fname):
    m = MeCab.Tagger("-Owakati")

    words = []

    with open(fname, "r") as f:

        for line in f:
            words.append(m.parse(line).split(" "))

    return words


def malkov_v_sql(cursor, line):
    w1 = line[0]
    w2 = line[1]
    w3 = line[2]

    try:
        cursor.execute("INSERT INTO malkov VALUES (?, ?, ?)", (w1, w2, w3))
    
    except sqlite3.Error as e:
        print("sqlErr: ", e.args[0])


    if line[3:] == []:
        return True

    else:
        return malkov_v_sql(cursor, line[1:])


if __name__ == "__main__":
    main()
