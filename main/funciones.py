import json
from werkzeug.security import generate_password_hash, check_password_hash


def encriptar(diccionario):
    dict_encriptado = dict()
    for K, V in diccionario.items():
        dict_encriptado[K] = generate_password_hash(V)        
    return dict_encriptado



def desencriptar(secure_data, diccionario):
    secure_data = secure_data.replace("'", '"')             
    dict_encriptado = json.loads(secure_data)# comvertir el json a un diccionario
    dict_desencriptado = {}
    for key, value in dict_encriptado.items():
        dict_desencriptado[key] = check_password_hash(value, diccionario.get(key, ""))
        value =dict_desencriptado[key]
    return value

