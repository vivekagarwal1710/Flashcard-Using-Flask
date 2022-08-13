from flask import Flask,render_template,request,redirect,url_for, session,flash
import sqlite3

app=Flask(__name__)
app.config['SECRET_KEY']='HELLO@54'

#-----Check session for each end point except allowed routes
@app.before_request
def require_login():
    allowed_routes=['login','register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

    


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""SELECT * FROM users WHERE username=? AND password=?"""
        cur.execute(query,(username,password))
        rows=cur.fetchall()
        
        if len(rows) ==1:
            #set session
            session['username']=username
            
            return redirect(url_for('index'))
        else:
            flash('Incorrect Username or Password')
    return render_template('login.html')

@app.route('/logout')
def logout():
  del session['username']
  flash('You have successfully logged out')
  return redirect('/login') 

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        try:
            name=request.form['name']
            username=request.form['username']
            password=request.form['password']
            conn=sqlite3.connect("project.db")
            cur=conn.cursor()
            query="""INSERT INTO users (name,username,password) VALUES (?,?,?)"""
            cur.execute(query,(name,username,password))
            conn.commit()
            
            if cur.rowcount ==1:
                return "Registered successfully <a href='/login'>Go to Login</a>"
            else:
                return "Username already exists <a href='/register'>Try Register again</a>"
        except:
            return "Something wrong"
        
    return render_template('register.html')


@app.route('/')
def index():
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    username=session['username']
    #query="""SELECT deckname from cards WHERE front IS NULL"""
    #cur.execute(query)
    query="""SELECT deckname from cards WHERE front IS NULL and username=?"""
    cur.execute(query,(username,))
    rows=cur.fetchall()
    
    return render_template('index.html',rows=rows)

@app.route('/createdeck',methods=['GET','POST'])
def createdeck():
    if request.method=="POST":
        deckname=request.form['deckname']
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""INSERT INTO cards (username,deckname) VALUES (?,?)"""
        cur.execute(query,(session['username'],deckname))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('createdeck.html')

@app.route('/deletedeck/<deckname>')
def deletedeck(deckname):
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    query="""DELETE FROM cards WHERE deckname=?"""
    cur.execute(query,(deckname,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/updatedeck/<deckname>',methods=['GET','POST'])
def updatedeck(deckname):
    if request.method=="POST":
        old=deckname
        new=request.form['new']
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""UPDATE cards SET deckname=? WHERE deckname=?"""
        cur.execute(query,(new,old))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('updatedeck.html',deckname=deckname)


@app.route('/review/<deckname>')
def review(deckname):
    
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    query="""SELECT * FROM cards WHERE deckname=? AND username=? AND front IS NOT NULL ORDER BY RANDOM() LIMIT 1"""
    #query="""SELECT * FROM cards WHERE deckname=? AND front IS NOT NULL"""
    cur.execute(query,(deckname,session['username']))
    rows=cur.fetchone()
    if rows is not None:
        return render_template('review.html',deckname=deckname,rows=rows)
    else:
        return redirect(url_for('index'))


@app.route('/addcard/<deckname>',methods=['GET','POST'])
def addcard(deckname):
    if request.method=="POST":
        front=request.form['front']
        back=request.form['back']
        
        conn=sqlite3.connect("project.db")
        cur=conn.cursor()
        query="""INSERT INTO cards (username,deckname,front,back) VALUES (?,?,?,?)"""
        cur.execute(query,(session['username'],deckname,front,back))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('addcard.html',deckname=deckname)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)