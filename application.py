from flask import Flask,render_template,request
import sqlite3 as sql
import pandas as pd
import numpy as np
import time 

app = Flask(__name__)

con = sql.connect("database.db")

port = int(os.getenv('PORT', 8000))
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def upload_csv():
   return render_template('upload.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
       con = sql.connect("database1.db")
       csv = request.files['myfile']
       file = pd.read_csv(csv)
       file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)	  
       con.close()
       return render_template("result.html",msg = "Record inserted successfully")

@app.route('/newrec', methods=['GET', 'POST'])
def query1():
	if request.method == 'POST':
		 rows=[]
		 mag = float(request.form['mag1'])
		 mag1 = float(request.form['mag2'])
		 query = "select * from Earthquake where mag BETWEEN ' " + str(mag)+ " 'and ' " + str(mag1)+ " ' " 
		 con = sql.connect("database.db") 
		 cur = con.cursor()
		 cur.execute(query)
		 rows = cur.fetchall()
		 return render_template('first.html',data=rows)
	return render_template('first.html')

@app.route('/newrec1', methods=['GET', 'POST'])
def query2():
	if request.method == 'POST':
		 rows=[]
		 start_t = time.time()
		 mag = request.form['mag1']
		 mag1 =request.form['mag2']
		 net1 = str(request.form['net'])
		 query = "select * from Earthquake where nst  > ' "+ net1 +" ' AND mag BETWEEN ' " + str(mag)+ " ' and ' " + str(mag1)+ " ' "
		 #query= 'SELECT * FROM EARTHQUAKE where place LIKE %' + request.form['place'] +'%'
		 con = sql.connect("database.db") 
		 cur = con.cursor()
		 cur.execute(query)
		 rows = cur.fetchall()
		 end_time = time.time()-start_t
		 print(rows)
		 print(end_time)
		 return render_template('first1.html',data=rows, time=end_time)
	return render_template('first1.html')


if __name__ == '__main__':
   #app.run(host='0.0.0.0', port=port, debug=True)
   app.run()
