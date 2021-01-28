import socket
import pickle

'''

    Simple TCP-IP server. Thanks to Tech With Tim.
    Usage:
    Initialise class and pass it current server ip as string
    use send, and request to communicate with server (you dont have to connect when you use them, but u have to disconnect after)

'''


class Client():
    def __init__(self, server_ip):
        self.HOST = server_ip
        self.HEADER_SIZE = 64
        self.PORT = 65433
        self.ADDR = (self.HOST, self.PORT)
        self.HEADER_FORMAT = 'utf-8'
        self.DISCONNECT_MSG = '!DISCONNECT'
        self.is_connected = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connects to the socket on ip given at initialisation
    def connect(self):
        if self.is_connected:
            return True
        else:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.settimeout(5)
                self.client.connect(self.ADDR)
                self.is_connected = True
                return True
            except socket.timeout as e:
                print('connection error: ', e)
                raise Exception('Could not Connect')

    #sends '!DISCONNECT' message
    def disconnect(self):
        if self.is_connected:
            self.send('!DISCONNECT')
            #self.client.close()
            self.is_connected = False
        else:
            print('not connected')

    #encodes and sends given string
    def send(self, msg):
        self.connect()
        msg = pickle.dumps(msg)
        message_length = str(len(msg)).encode(self.HEADER_FORMAT)
        header = message_length + (b' ' * (self.HEADER_SIZE - len(message_length)))
        msg = header + msg
        self.client.send(msg)

    #waits for message from server and decodes it
    def recive(self):
        self.connect()
        msg_length = self.client.recv(self.HEADER_SIZE).decode(self.HEADER_FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = pickle.loads(self.client.recv(msg_length))
            return msg


    #sends request message and waits for response
    def request(self, msg):
        #self.connect()
        self.send(msg)
        return self.recive()



