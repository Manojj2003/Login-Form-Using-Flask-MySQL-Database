@app.route("/view_users")
def view_users():
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        if data:
            return render_template("view_users.html", res=data)
        else:
            flash("No users found", "danger")
    except Exception as e:
        print(e)
    finally:
        cur.close()

    return render_template("view_users.html")

@app.route("/delete_users/<int:id>", methods=['GET', 'POST'])
def delete_users(id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE pid=%s", [id])
        conn.commit()
        flash("User deleted successfully", "success")
    except Exception as e:
        print(e)
    finally:
        cur.close()

    return redirect(url_for("view_users"))