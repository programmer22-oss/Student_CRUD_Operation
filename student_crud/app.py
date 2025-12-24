from flask import Flask, redirect, render_template, request, url_for, flash, Response
import sqlite3
import math
import csv
import io


app = Flask(__name__)
app.secret_key = "secret_key"


def init_db():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student(
        name TEXT,
        branch TEXT,
        regno TEXT PRIMARY KEY
    )
    """)
    con.commit()
    con.close()


init_db()


def get_db():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    return con


@app.route("/")
def index():
    con = get_db()
    cur = con.cursor()

    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    search_query = request.args.get("q", "")
    sort_by = request.args.get("sort_by", "regno")
    order = request.args.get("order", "asc")

    # Whitelist validation for security
    if sort_by not in ["regno", "name", "branch"]:
        sort_by = "regno"
    if order not in ["asc", "desc"]:
        order = "asc"

    if search_query:
        cur.execute("SELECT COUNT(*) FROM student WHERE name LIKE ?",
                    ("%" + search_query + "%",))
        total = cur.fetchone()[0]
        query = f"SELECT * FROM student WHERE name LIKE ? ORDER BY {sort_by} {order} LIMIT ? OFFSET ?"
        cur.execute(query, ("%" + search_query + "%", per_page, offset))
    else:
        cur.execute("SELECT COUNT(*) FROM student")
        total = cur.fetchone()[0]
        query = f"SELECT * FROM student ORDER BY {sort_by} {order} LIMIT ? OFFSET ?"
        cur.execute(query, (per_page, offset))

    data = cur.fetchall()
    total_pages = math.ceil(total / per_page)
    return render_template("index.html", students=data, page=page, total_pages=total_pages, search_query=search_query, sort_by=sort_by, order=order)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        branch = request.form["branch"]
        regno = request.form["regno"]
        con = get_db()
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO student VALUES(?,?,?)",
                        (name, branch, regno))
            con.commit()
            flash("Student Added Successfully", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash(
                f"Error: Registration No '{regno}' already exists.", "danger")
            return render_template("add_student.html")
    return render_template("add_student.html")


@app.route("/delete/<regno>")
def delete_student(regno):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM student WHERE regno=?", (regno,))
    con.commit()
    if cur.rowcount > 0:
        flash("Student Deleted Successfully", "danger")
    else:
        flash("Student not found or already deleted.", "warning")
    return redirect(url_for("index"))


@app.route("/update/<regno>", methods=["GET", "POST"])
def update_student(regno):
    con = get_db()
    cur = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        branch = request.form["branch"]

        cur.execute(
            "UPDATE student SET name=?, branch=? WHERE regno=?", (name, branch, regno))
        con.commit()
        flash("Student Updated Successfully", "info")
        return redirect(url_for("index"))

    cur.execute("SELECT * FROM student WHERE regno=?", (regno,))
    student = cur.fetchone()
    if student is None:
        flash("Student not found.", "danger")
        return redirect(url_for("index"))
    return render_template("update_student.html", student=student)


@app.route("/export")
def export_data():
    con = get_db()
    cur = con.cursor()

    search_query = request.args.get("q", "")

    if search_query:
        cur.execute("SELECT * FROM student WHERE name LIKE ?",
                    ("%" + search_query + "%",))
    else:
        cur.execute("SELECT * FROM student")

    data = cur.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['Registration No', 'Name', 'Branch'])
    for row in data:
        writer.writerow([row['regno'], row['name'], row['branch']])

    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=student_list.csv"})


if __name__ == "__main__":
    app.run(debug=True)
