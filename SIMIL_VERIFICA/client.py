import socket as sck
from threading import Thread
import datetime
import time

address = ('127.0.0.1',8000)

s_client = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

LIVELLO_MISURATO = 6.0
            
def main():
    s_client.connect(address)
    
    data_ora = datetime.datetime.now() 
    print(data_ora)
    while 1:
        mex = input("1 VERIFICA PRESENZA FILE\n2 NUMERO FRAMMENTI DATO UN FILE\n3 DATO NUME FILE E NUMERO FRAMMENTO IP DELL'HOST CHE OSPITA UN FRAMMENTO\n4 DATO NUME FILE IP DEGLI HOST SU CUI SONO SALVATI DEI FRAMMMENTI\n")
        if (mex == "exit"):
            break 
        s_client.sendall(mex.encode())
    s_client.close()

if __name__=="__main__":
    main()
