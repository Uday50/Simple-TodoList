from flask import * 
import sqlite3

app = Flask(__name__,template_folder='./templets')
u = {}
#create a database
connect = sqlite3.connect("./datab.db")
connect.execute("CREATE TABLE IF NOT EXISTS todo(Id INTEGER PRIMARY KEY NOT NULL,Task TEXT NOT NULL,Description TEXT NOT NULL)")
connect.close()

@app.route('/', methods=['GET','POST'])
def welcome():
    if request.method == 'POST':
        name = request.form.get('name')
        uname = name
        connect=sqlite3.connect('./datab.db')
        cursor=connect.cursor()
        cursor.execute("select * from todo")
        todo=cursor.fetchall()
        u['todo']=todo
        u['name']=uname
        return render_template("index.html",todo=u)
    return render_template('welcome.html')

@app.route('/index', methods =['GET','POST'])
def index():
    connect=sqlite3.connect('./datab.db')
    cursor=connect.cursor()
    cursor.execute("select * from todo")
    todo=cursor.fetchall()
    u['todo']=todo
    return render_template("index.html",todo=u)
    
@app.route("/add",methods=["POST","GET" ])
def add():
    task=request.form.get("task")
    description=request.form.get("description")
    connect=sqlite3.connect('./datab.db')
    cursor=connect.cursor()
    cursor.execute("insert into todo(Task,Description) values(?,?)",(task,description))
    connect.commit()
    cursor.close()
    return redirect("/index")

@app.route("/delete/<int:id>")
def delete(id):
    connect=sqlite3.connect('./datab.db')
    cursor=connect.cursor()
    cursor.execute("delete from todo where Id=?",(id,))
    connect.commit()
    cursor.close()
    return redirect("/index")

@app.route("/update/<int:id>",methods=["POST","GET"])
def update(id):
    connect=sqlite3.connect('./datab.db')
    cursor=connect.cursor()
    if request.method=="POST":
       task=request.form.get("task")
       description=request.form.get("description")
       cursor.execute("UPDATE todo SET Task =?,Description=? WHERE Id=?",(task,description,id))
       connect.commit()
       cursor.close()
       return redirect("/index")
    else:
        cursor.execute("select * from todo where Id=?",(id,))
        task=cursor.fetchone()
        cursor.close()
        return render_template("update.html",task=task)


if __name__ == '__main__':
    app.run(debug = True)