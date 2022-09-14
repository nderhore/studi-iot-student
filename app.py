from flask import Flask, render_template
import sqlite3 as sql

db = "bdd/temperature.sql"

app = Flask(__name__)


@app.route('/')
def html(name=None):
    with sql.connect(db) as con:
        c = con.cursor()
        res = c.execute("SELECT * FROM releve").fetchall()
        xval1, yval1 = [], []
        xval2, yval2 = [], []
        xval3, yval3 = [], []
        xval4, yval4 = [], []
        for elem in res:
            if elem[2] == 1:
                xval1.append(elem[0])
                yval1.append(elem[1])
            if elem[2] == 2:
                xval2.append(elem[0])
                yval2.append(elem[1])
            if elem[2] == 3:
                xval3.append(elem[0])
                yval3.append(elem[1])
            if elem[2] == 4:
                xval4.append(elem[0])
                yval4.append(elem[1])

    return render_template('index.html', xval1=xval1,
                           yval1=yval1, xval2=xval2,
                           yval2=yval2, xval3=xval3,
                           yval3=yval3, xval4=xval4,
                           yval4=yval4)


if __name__ == "__main__":
    app.run()
