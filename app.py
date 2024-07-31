from flask import Flask, render_template, request, url_for, session, redirect, flash
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='register'
)

# Check MySQL connection
try:
    conn.ping(reconnect=True)
except Exception as e:
    print(f"Failed to connect to MySQL: {e}")

# Create 'users' table if not exists
with conn.cursor() as cursor:
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        pid INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        age INT,
                        address VARCHAR(255),
                        contact VARCHAR(20),
                        mail VARCHAR(255))''')
    except Exception as e:
        print(f"Error creating 'users' table: {e}")

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'register' in request.form:
        if request.method == 'POST':
            uname = request.form["uname"]
            password = request.form["upass"]
            age = request.form["age"]
            address = request.form["address"]
            contact = request.form["contact"]
            mail = request.form["mail"]
            try:
                cur = conn.cursor()
                cur.execute('INSERT INTO users (name, password, age, address, contact, mail) VALUES (%s, %s, %s, %s, %s, %s)',
                            (uname, password, age, address, contact, mail))
                conn.commit()
                flash('User registered successfully', 'success')
            except Exception as e:
                print(e)
            finally:
                cur.close()

    elif 'ulogin' in request.form:
        if request.method == 'POST':
            name = request.form["uname"]
            password = request.form["upass"]
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT * FROM users WHERE name=%s AND password=%s", [name, password])
                res = cur.fetchone()
                if res:
                    session["name"] = res["name"]
                    session["pid"] = res["pid"]
                    return redirect(url_for('user_home'))
                else:
                    return render_template("index.html")
            except Exception as e:
                print(e)
            finally:
                cur.close()

    return render_template("index.html")

@app.route("/user_profile")
def user_profile():
    if 'pid' in session:
        pid = session["pid"]
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM users WHERE pid=%s", [pid])
            data = cur.fetchone()
            if data:
                return render_template("user_profile.html", res=data)
            else:
                flash("User not found", "danger")
        except Exception as e:
            print(e)
        finally:
            cur.close()
    else:
        flash("Session expired, please login again", "danger")
        return redirect(url_for("index"))

@app.route("/update_user", methods=['GET', 'POST'])
def update_user():
    if 'pid' in session:
        pid = session["pid"]
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            age = request.form['age']
            address = request.form['address']
            contact = request.form['contact']
            mail = request.form['mail']
            try:
                cur = conn.cursor()
                cur.execute('''UPDATE users SET name=%s, password=%s, age=%s, address=%s, contact=%s, mail=%s 
                               WHERE pid=%s''', (name, password, age, address, contact, mail, pid))
                conn.commit()
                flash('User updated successfully', 'success')
                return redirect(url_for('user_profile'))
            except Exception as e:
                print(e)
            finally:
                cur.close()
    else:
        flash("Session expired, please login again", "danger")
        return redirect(url_for("index"))

    return render_template("user_profile.html")





@app.route("/user_home")
def user_home():
    if 'name' in session:
        return render_template("user_home.html")
    else:
        flash("Session expired, please login again", "danger")
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.secret_key = '123'
    app.run(debug=True)

# Close MySQL connection when Flask app stops
conn.close()
