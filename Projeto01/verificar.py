from importlib.util import find_spec

pacotes = ["tkgpio", "gpiozero", "mplayer", "flask", "pymongo", "requests", "urllib3", "sounddevice", "PIL", "numpy", "scipy", "cv2"]

tudo_certo = True
mongodb_certo = True
for pacote in pacotes:
    dados = find_spec(pacote)
    if dados == None:
        tudo_certo = False
        if pacote == "pymongo":
            mongodb_certo = False
        
        print("\x1b[1;37;41m" + "\"" + pacote + "\" NÃO ESTÁ INSTALADO!" + "\x1b[0m")
        
if tudo_certo:
    print("\x1b[1;37;42m" + "Todos os pacotes do Python estão instalados corretamente." + "\x1b[0m")
    
if mongodb_certo:
    from pymongo import *
    
    print("Testando MongoDB...")

    documento = None
    try:
        cliente = MongoClient("localhost", 27017, serverSelectionTimeoutMS=3000)
        banco = cliente["banco_de_teste"]
        colecao = banco["colecao_de_teste"]
        colecao.insert_one({"campo1": 42, "campo2": 9001})
        documento = colecao.find_one({"campo1": 42})
    except:
        pass
    
    if documento == None:
        print("\x1b[1;37;41m" + "MONGODB NÃO ESTÁ INSTALADO OU CONFIGURADO CORRETAMENTE!" + "\x1b[0m")
    else:
        print("\x1b[1;37;42m" + "MongoDB está instalado corretamente." + "\x1b[0m")
    
else:
    print("")
    print("\x1b[1;37;41m" + "INSTALE O PYMONGO PARA TESTAR O MONGODB!" + "\x1b[0m")
