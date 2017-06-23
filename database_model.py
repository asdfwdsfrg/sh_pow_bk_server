from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import abort
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shared_pow_bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    passwd = db.Column(db.String(20))
    email = db.Column(db.String(30))
    balance = db.Column(db.Float)

    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd

    def __repr__(self):
        return '<User %r>' % self.username


class Depository(db.Model):
    device_id = db.Column(db.Integer, primary_key=True)
    pow_bank_num = db.Column(db.Integer)
    location = db.Column(db.String(20))
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    chkcode = db.Column(db.Integer)

    def __init__(self, device_id, pow_bank_num, location, lng, lat):
        self.device_id = device_id
        self.pow_bank_num = pow_bank_num
        self.location = location
        self.lng = lng
        self.lat = lat
        self.chkcode = 0

    def __repr__(self):
        return '<Depository_id %r pow_bank_num %r location %r>' \
               % self.device_id, self.pow_bank_num, self.location



