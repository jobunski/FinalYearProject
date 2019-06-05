import  MySQLdb
from time import strftime,localtime
import datetime
from unidecode import unidecode

def connect():
    return MySQLdb.connect(host="localhost", user="ski", password="root", db="Retailer")

def InsertReading()