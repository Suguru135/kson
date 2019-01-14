import MeCab
import sqlite3

import malkov
import sys
import random

class Main:
    def main(self):
        args = sys.argv
        if len(args) < 2:
            sys.exit("Err: モード未指定")

        mode = args[1]

        if mode == "s":
            self.startup()
            self.set()
            self.close()

        elif mode == "t":
            self.startup()
            self.talk()
            self.close()

        elif mode == "a":
            self.startup()
            self.set()

            self.talk()
            
            self.close()


    def startup(self):
        self.conn = sqlite3.connect("kson.db")
        self.cursor = self.conn.cursor()
        self.mal = malkov.Malkov_na_sqlite(self.cursor)

    def set(self):
        self.mal.reset()

        lines = malkov.get_lines_from_a_file("./data.txt")
        for line in lines:
            self.mal.insert(line)

        self.conn.commit()

    def talk(self):
        line = input("b:")
        if line == "owari":
            return 0

        m = MeCab.Tagger("-Ochasen")
        n = m.parseToNode(line)
        keywords = []

        while n:
            word = n.surface
            hinshi = n.feature.split(",")[0]
            if hinshi == "名詞":
                keywords.append(word)
            n = n.next

        keyword = random.choice(keywords)

        print("k:" + keyword + self.mal.remake(keyword))

        self.talk()


    def close(self):
        self.conn.close()
    


if __name__ == "__main__":
    Main().main()


