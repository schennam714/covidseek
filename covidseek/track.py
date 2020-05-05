from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import json
import sys
sys.path.append("/Users/shreyas/Desktop/Web Dev/covidseek")
from covidseek.model import NewModel
from covidseek.createdata import counties
from covidseek.apikey import api_key
import matplotlib
import googlemaps

matplotlib.use('Agg')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    county = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/initial')
def initial():
    return render_template('initpage.html')

@app.route('/locate', methods=['POST', 'GET'])
def locate():
    if request.method == 'POST':
        county_name = request.form['search']
        area = [part.strip() for part in county_name.split(',')]
        test = False
        for place in counties:
            if place["county"]==area[0] and place["state"]==area[1]:
                test = True
        if test is False:
            return redirect('/error')
        new_location = Location(county=area[0], state=area[1], country=area[2])
        try:
            db.session.add(new_location)
            db.session.commit()
            return redirect('/locate')
        except:
            return 'There was an error with your request'
    else:
        locations = Location.query.order_by(Location.id.desc()).first() #look at all the database contents in order of creation and returns all of them
        fit = NewModel(locations.state)
        prev_data, cap = fit.makedata()
        model = fit.train(prev_data, cap)
        filename = "" + locations.state + ".png"
        return render_template('datamap.html', location=locations, deaths=counties, use=True, filename=filename)

@app.route('/about')
def about():
    return render_template('team.html')

@app.route('/error')
def error():
    return "There was an error processing your request. Either you have entered your input wrong or your location does not exist in our database. Please try again."

@app.route('/resources')
def resources():
    locations = Location.query.order_by(Location.id.desc()).first()
    gmaps_key = googlemaps.Client(key = api_key)
    geocode_area = locations.county + ", " + locations.state
    geocode = gmaps_key.geocode(geocode_area)
    lat = 0
    lon = 0
    try:
        lat = geocode[0]["geometry"]["location"]["lat"]
        lon = geocode[0]["geometry"]["location"]["lng"]
    except:
        lat = None
        lon = None
    return render_template('resources.html', city=locations.county, state=locations.state, lat=lat, lon=lon)


