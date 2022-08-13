import sqlite3
conn=sqlite3.connect("project.db")
cur=conn.cursor()
#create table



query="""CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT NOT NULL UNIQUE,
    password TEXT

)"""
cur.execute(query)

query1=""" CREATE TABLE cards (
    sno INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    deckname TEXT NOT NULL,
    front TEXT,
    back TEXT,
    FOREIGN KEY(username) REFERENCES users(username)
    
)"""
cur.execute(query1)