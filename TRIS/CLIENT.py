import socket

class TrisClient:
    def __init__(self):
        self.s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_client.connect(('127.0.0.1', 8000))

    def gioca(self):
        while True:
            print(self.s_client.recv(1024).decode()) 
            mossa = input("Inserisci la tua mossa (riga,colonna): ")
            self.s_client.sendall(mossa.encode())
            stato_partita = self.s_client.recv(1024).decode()
            print(stato_partita)

            if "La partita è finita" in stato_partita:
                break

if __name__ == "__main__":
    client = TrisClient()
    client.gioca()
