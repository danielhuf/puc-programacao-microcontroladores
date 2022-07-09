from pymongo import MongoClient
from json import load
import os

def redefinir_banco():
    cliente = MongoClient("localhost", 27017)
    cliente.drop_database("playground")
