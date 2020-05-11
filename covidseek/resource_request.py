from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os

class SearchForm(FlaskForm):
    resource = StringField('Resource', validators=[DataRequired()])
    store = StringField('Store', validators=[DataRequired()])
    submit = SubmitField('Search for Product')

class StoreSearch:
    final = webdriver.ChromeOptions()
    if os.environ.get('GOOGLE_CHROME_BIN'):
        final.binary_location = os.environ['GOOGLE_CHROME_BIN']

    final.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), options=final)
    def __init__(self):
        self.status = "Out of Stock"
        self.products = {}
    def find(self, city, state):
        self.final.get("http://www.google.com")

test = StoreSearch()
test.find("Fairfax", "VA")
