from jproperties import Properties
import base64

def read_properties():
    configs = Properties()
    with open('config.properties', 'rb') as read_prop: 
        configs.load(read_prop) 
    return configs