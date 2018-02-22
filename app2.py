from flask import Flask, redirect, render_template, request, url_for, flash, jsonify
from models import *
import psycopg2
import random
import timeit
app = Flask(__name__)

#Database configurations of the postgres database
POSTGRES = {
    'user': 'postgres',
    'pw': 'itsmevibha',
    'db': 'mydb',
    'host': 'localhost',
    'port': '5432',
}
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

conn = psycopg2.connect(database = 'mydb', user = 'postgres', password = 'itsmevibha', host = 'localhost')
curs = conn.cursor()

#Hardcoded latitude and longitude values
latitude = 45.12 
longitude = 71.12
@app.route('/')
def home():
	return jsonify("Nothing here. Please go to the get, post or register endpoint.")
@app.route('/post_location', methods = ['POST'])
def post_location():
        
        print(request.json)
        conn.commit()
       
        key=request.json['key']
        place_name=request.json['place_name']
        if key == "" or longitude == "" or place_name == "":
            return jsonify("Empty fields not allowed")
        curs.execute("insert into table_3 (key,place_name,) values(%d,%s);",[key,place_name])
        conn.commit()
        return jsonify("Row Inserted.")
        

if __name__ == '__main__':
    app.run()

