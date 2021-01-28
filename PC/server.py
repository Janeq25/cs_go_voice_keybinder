import socket
import threading
import pickle

class Server():

    '''

    Simple TCP-IP server. Thanks to Tech With Tim. Ip defaults to localhost.
    Usage:
    Initialise Server class and pass it your on_message_handler function (function will recive conn, addr and msg variables)
    run server with Server.run()
    send messages with sv.send(conn, addr, msg) (ensures proper header is sent)


    '''



    def __init__(self, func=None):
        if not func == None:
            self.on_message_handler = func
        else:
            self.on_message_handler = self.on_message
        self.HEADER_SIZE = 64
        self.PORT = 65433
        self.HOST = socket.gethostbyname(socket.gethostname())
        #self.HOST = '0.0.0.0'
        self.ADDR = (self.HOST, self.PORT)
        self.HEADER_FORMAT = 'utf-8'
        self.DISCONNECT_MSG = '!DISCONNECT'

        self.server = socket.socket()
        self.server.bind(self.ADDR)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def on_message(self, conn, addr, msg):
        print(addr, 'said', msg)

    def send(self, conn, addr, msg):
        msg = pickle.dumps(msg)
        message_length = str(len(msg)).encode(self.HEADER_FORMAT)
        header = message_length + (b' ' * (self.HEADER_SIZE - len(message_length)))
        msg = header + msg
        conn.send(msg)





    def handle_client(self, conn, addr):
        print(f'connection from {addr}')

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER_SIZE).decode(self.HEADER_FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = pickle.loads(conn.recv(msg_length))

                if msg == self.DISCONNECT_MSG:
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()
                    connected = False
                    print('DISCONNECTING')
                else:
                    try:
                        self.on_message_handler(conn, addr, msg, self.send)

                    except Exception as e:
                        print('ERROR with message handler: ', e)


        conn.close()

    def start(self):
        self.server.listen()
        print(f'starting server on ip {socket.gethostbyname(socket.gethostname())} : {self.PORT}')
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f'{threading.activeCount() - 1} active connections')
