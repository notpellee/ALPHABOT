import socket as sck

address = ('192.168.1.129',8000)
isRunning = True

s_client = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

def main():
    global isRunning
    
    s_client.connect(address)

    while isRunning:

        mex = input("1 AVANTI 2 DESTRA 3 SINISTRA 4 INDIETRO")
        s_client.sendall(mex.encode())

        print(s_client.recv(4096).decode())

    s_client.close()

if __name__=="__main__":
    main()