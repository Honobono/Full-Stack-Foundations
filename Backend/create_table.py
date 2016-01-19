import sqlite3
db = sqlite3.connect('lean_fridge_app.db')
c = db.cursor()

def stockTable():
    c.execute("CREATE TABLE stock(id INT PRIMARY KEY ASC, name varchar(20) NOT NULL, total INT)")

def dataInsert_stock():
    c.execute("INSERT INTO stock VALUES(1, 'apple', 3)")
    c.execute("INSERT INTO stock VALUES(2, 'orange', 4)")
    c.execute("INSERT INTO stock VALUES(3, 'banana', 6)")
    c.execute("INSERT INTO stock VALUES(4, 'yogurt', 2)")
    c.execute("INSERT INTO stock VALUES(5, 'pasta', 2)")
    c.execute("INSERT INTO stock VALUES(6, 'carrot', 6)")
    c.execute("INSERT INTO stock VALUES(7, 'potato', 5)")
    c.execute("INSERT INTO stock VALUES(8, 'celery', 4)")
    c.execute("INSERT INTO stock VALUES(9, 'tomato', 8)")
    c.execute("INSERT INTO stock VALUES(10, 'almond milk', 2)")

    db.commit()
