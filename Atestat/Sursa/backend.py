import sqlite3

def connect():
    conn = sqlite3.connect("elevi.db")
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS elev (id INTEGER PRIMARY KEY, nume text, prenume text, adresa text, cnp text)")
    conn.commit()
    conn.close()

def insert(nume, prenume, adresa, cnp):
    conn = sqlite3.connect("elevi.db")
    curs = conn.cursor()
    curs.execute("INSERT INTO elev VALUES (NULL, ?, ?, ?, ?)",(nume, prenume, adresa, cnp))
    conn.commit()
    conn.close()

def insert_nota(nume, prenume, data, mate="", romana="", informatica="", fizica=""):
    path = "Elevi/" + prenume + " " + nume + ".db"
    conn = sqlite3.connect(path)
    curs = conn.cursor()
    curs.execute("INSERT INTO nota VALUES (?, ?, ?, ?, ?)", (data, mate, romana, informatica, fizica))
    conn.commit()
    conn.close()

def sterge_capsule(nume, prenume):
    path = "Elevi/" + prenume + " " + nume + ".db"
    conn = sqlite3.connect(path)
    curs = conn.cursor()
    curs.execute("DELETE FROM nota WHERE (matematica is NULL OR matematica ='') AND (romana is NULL OR romana = '') AND (informatica is NULL or informatica = '') AND (fizica is NULL OR fizica = '')")
    conn.commit()
    conn.close()

def creare_tabel_nota(nume, prenume):
    path = "Elevi/" + prenume + " " + nume + ".db"
    conn = sqlite3.connect(path)
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS nota (data integer, matematica integer, romana integer, informatica integer, fizica integer)")
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("elevi.db")
    curs = conn.cursor()
    curs.execute("SELECT * FROM elev")
    rows = curs.fetchall()
    conn.close()
    return rows

def search(nume = "", prenume="", adresa="", cnp=""):
    conn = sqlite3.connect("elevi.db")
    curs = conn.cursor()
    curs.execute("SELECT * FROM elev WHERE nume=? OR prenume=? OR adresa=? OR cnp=?", (nume, prenume, adresa, cnp))
    rows = curs.fetchall()
    conn.close()
    return rows

def generare_nota_mate(nume, prenume):
    path = "Elevi/" + prenume + " " + nume + ".db"
    conn = sqlite3.connect(path)
    curs = conn.cursor()
    curs.execute("SELECT matematica FROM nota WHERE matematica != ''")
    rows = curs.fetchall()
    conn.close()
    return rows

def generare_nota_romana(nume, prenume):
    path = "Elevi/" + prenume + " " + nume + ".db"
    conn = sqlite3.connect(path)
    curs = conn.cursor()
    curs.execute("SELECT romana FROM nota WHERE romana != ''")
    rows = curs.fetchall()
    conn.close()
    return rows

def generare_nota_info(nume, prenume):
    path = "Elevi/" + prenume + " " + nume + ".db"
    conn = sqlite3.connect(path)
    curs = conn.cursor()
    curs.execute("SELECT informatica FROM nota WHERE informatica != ''")
    rows = curs.fetchall()
    conn.close()
    return rows

def generare_nota_fizica(nume, prenume):
    path = "Elevi/" + prenume + " " + nume + ".db"
    conn = sqlite3.connect(path)
    curs = conn.cursor()
    curs.execute("SELECT fizica FROM nota WHERE fizica != ''")
    rows = curs.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("elevi.db")
    curs = conn.cursor()
    curs.execute("DELETE FROM elev WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, nume, prenume, adresa, cnp):
    conn = sqlite3.connect("elevi.db")
    curs = conn.cursor()
    curs.execute("UPDATE elev SET nume=?, prenume=?, adresa=?, cnp=? WHERE id=?", (nume, prenume, adresa, cnp, id))
    conn.commit()
    conn.close()
connect()