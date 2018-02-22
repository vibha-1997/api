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



#Hardcoded latitude and longitude values
##latitude = 45.12 
##longitude = 71.12
@app.route('/')
def home():
	return jsonify("Nothing here. Please go to the get, post or register endpoint.")
@app.route('/post_location', methods = ['POST'])
def post_location():
        conn = psycopg2.connect(database = 'mydb', user = 'postgres', password = 'itsmevibha', host = 'localhost')
        curs = conn.cursor()
        print(request.json)
        
       
        key=request.json['key']
        place_name=request.json['place_name']
        admin_name1=request.json['admin_name1']
        latitude=request.json['latitude']
        longitude=request.json['longitude']
        accuracy=request.json['accuracy']
        if latitude == ""  or longitude == "" or place_name=="" or admin_name1=="" or accuracy=="":
                return jsonify("Empty fields not allowed")
        curs.execute("insert into table_2 (key,place_name,admin_name1,latitude,longitude,accuracy) values(%s,%s,%s,%s,%s,%s);",[key,place_name,admin_name1,float(latitude),float(longitude),float(accuracy)])
        curs.close()
        conn.commit()
        
        return jsonify({'task':'success'})


@app.route('/get_data')
def data():
        conn = psycopg2.connect(database = 'mydb', user = 'postgres', password = 'itsmevibha', host = 'localhost')
        curs = conn.cursor()
        

    # here we want to get the value of user (i.e. ?user=some-value)
        lat = 45.12
        longi = 75.13
        #curs.execute("select * from table_2 where place_name=%s;",[place_name])
        curs.execute("select * from table_2 where (point(longitude,latitude) <@> point(%s,%s)) <= 5/1.6;",[float(longi),float(lat)])
        rows=curs.fetchall()
        curs.close()
        conn.commit()
        return jsonify({'result':rows})


@app.route('/get_data_self')
def data_2():
        conn = psycopg2.connect(database = 'mydb', user = 'postgres', password = 'itsmevibha', host = 'localhost')
        curs = conn.cursor()
        

    # here we want to get the value of user (i.e. ?user=some-value)
        lat = 45.12
        longi = 75.13
        #curs.execute("select * from table_2 where place_name=%s;",[place_name])
        curs.execute("select * from ( select  place_name, latitude, longitude, (3959 * acos (cos ( radians(%s) ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians(%s) ) + sin ( radians(%s) ) * sin( radians( latitude ) ) ) ) AS distance FROM table_2 order by distance) items where distance < 5/1.6;",[lat,longi,lat])

        rows=curs.fetchall()
        curs.close()
        conn.commit()
        return jsonify({'result':rows})


if __name__ == '__main__':
    app.run()

