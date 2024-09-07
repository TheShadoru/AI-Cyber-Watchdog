import sqlite3

def writeData(fdtn, prompt, data, response):
    con = sqlite3.connect('./reports/{0}.sqlite'.format(fdtn))
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data(prompt, data, response);")
    con.commit()
    cur.execute("""INSERT INTO data VALUES({0}, {1}, {2})""".format(prompt, data, response))
    con.commit()
    con.close()


def readDB(fdtn):
    con = sqlite3.connect('./reports/{0}.sqlite'.format(fdtn))
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM data;").fetchall()
    con.close()
    print(rows)