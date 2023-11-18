# Import the dependencies.
from flask import Flask,jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base= automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station=Base.classes.station
measurement=Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app=Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def prec():
	query="""SELECT date,prcp from measurement
	where date>='2016-08-23'
	order by date"""
	result = session.execute(text(query)).all()
	#print(type(result))
	#print (result)
	my_dictionary={}
	for item in result:
		key=item[0]
		value=item[1]
		my_dictionary[key]=value
	#print(my_dictionary)
	return jsonify(my_dictionary)
@app.route("/api/v1.0/stations")
def station():
	query="""SELECT station from station"""
	result = session.execute(text(query)).all()
	my_list=[]
	for item in result:
		my_list.append(item[0])
	return jsonify (my_list)
@app.route("/api/v1.0/tobs")
def tobs():
	design_query3=text("""select tobs from measurement
	where station = 'USC00519281' and date>= DATE("2017-08-23","-1 year")""")
	result = session.execute(design_query3).all()
	my_list=[]
	for item in result:
		my_list.append(item[0])
	return jsonify (my_list)
@app.route("/api/v1.0/<start>")
def question5a(start):
	design_query2=text(f"""select min(tobs),avg(tobs),max(tobs) from measurement
	where date>= '{start}'""")
	result = session.execute(design_query2).all()
	#my_list=[]
	#for item in result:
		#my_list.append(item[0])
	#return jsonify (my_list)
	#print(result)
	result=list(result[0])
	return jsonify(result) 
@app.route("/api/v1.0/<start>/<end>")
def question5b(start,end):
	design_query2=text(f"""select min(tobs),avg(tobs),max(tobs) from measurement
	where date>= '{start}' and date<='{end}'""")
	result = session.execute(design_query2).all()
	#my_list=[]
	#for item in result:
		#my_list.append(item[0])
	#return jsonify (my_list)
	result=list(result[0])
	return jsonify(result)


@app.route("/")
def index():
 	temp = """
 	available routes:\n<br/>
 	/api/v1.0/precipitation\n<br/>
 	/api/v1.0/stations\n<br/>
 	/api/v1.0/tobs\n<br/>
 	/api/v1.0/&ltstart&gt\n<br/>
 	/api/v1.0/&ltstart&gt/&ltend&gt\n<br/>
 	"""
 	return temp
#question5b("2016-09-01","2017-03-01")
app.run()












