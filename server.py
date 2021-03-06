
from datetime import datetime
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread



import urllib.request




clients = {}
addresses = {}
HOST = '104.248.82.4'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Hello! "+
                          "Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type "/q" to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name

    sock_of_sender = client
    ip_sender = str(sock_of_sender)[str(sock_of_sender).find('raddr=(\'') + 8:str(sock_of_sender).find('raddr=(\'')+21]
    prefix = '<ip:' + ip_sender + '> name: '
    print(prefix, client)

    broadcast(name, bytes(msg, "utf8"), prefix)
    clients[client] = name
    bot_time = 0
    while True:
        msg = client.recv(BUFSIZ)
        if bot_time == 1:
            if msg == bytes("/help", "utf8"):
                string = 'First of all, let me introduce what I can:\n /room, /time, /weather, /quit '
                broadcast_whisper(bytes(name,"utf8"), bytes(string,"utf8"), "BOT: ", '')
            if msg == bytes("/room", "utf8"):
                string = str(list(clients.values()))
                broadcast_whisper(bytes(name,"utf8"), bytes(string,"utf8"), "BOT: they are in room now \n", '')
            if msg == bytes("/time", "utf8"):
                broadcast_whisper(bytes(name,"utf8"), b'', datetime.strftime(datetime.now(), "BOT: real time is %d.%m.%Y-%H:%M:%S"), '')
            if msg == bytes("/quit", "utf8"):
                broadcast_whisper(bytes(name,"utf8"), b'', "BOT: goodbye!)", '')
                bot_time = 0
            else:
                broadcast_whisper(bytes(name,"utf8"), b'', "BOT: if you want to quit, type /quit!)", '')
        elif msg != bytes("/q", "utf8"):
            if msg.find(bytes("(", "utf8")) == 0 and msg.find(bytes(")", "utf8")) != -1:
                receiver_name = msg[msg.find(bytes("(", "utf8"))+1:msg.find(bytes(")", "utf8"))]
                msg = msg[msg.find(bytes(")", "utf8"))+1:]
                prefix = name + " *whisper to " + receiver_name.decode("utf8") + "* (" + datetime.strftime(datetime.now(), "%d.%m.%Y-%H:%M:%S") + "): "
                broadcast_whisper(receiver_name, msg, prefix, name)
            elif msg == bytes('/bot', "utf8"):
                broadcast_whisper(bytes(name,"utf8"), b"Hello, I'm your chatbot. What can I do to you?. Type /help for help", "BOT:", '')
                bot_time = 1
            else:
                broadcast(name, msg, name + " (" + datetime.strftime(datetime.now(), "%d.%m.%Y-%H:%M:%S") + "): ")
        else:
            client.send(bytes("/q", "utf8"))
            client.close()
            del clients[client]
            broadcast(name, bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast_whisper(receiver_name, msg, prefix, name):
    if receiver_name.decode("utf-8") in list(clients.values()):
        sock = get_key(clients, receiver_name.decode("utf-8"))
        if 'BOT' not in prefix:
            sock_of_sender = str(get_key(clients, name))
            ip_sender = str(sock_of_sender).split('\'')[3]
            prefix = prefix[:-2] + '<ip:' + ip_sender + '>: '
        if len(name) != 0:
            sock_host = get_key(clients, name)
            sock_host.send(bytes(prefix, "utf8")+msg)
        sock.send(bytes(prefix, "utf8")+msg)


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def broadcast(receiver_name, msg, prefix=""):
    if '<ip:' not in prefix:
        sock_of_sender = str(get_key(clients, receiver_name))
        ip_sender = str(sock_of_sender).split('\'')[3]
        with urllib.request.urlopen("https://geoip-db.com/jsonp/"+ip_sender) as url:

            html_response = url.read()
            encoding = url.headers.get_content_charset('utf-8')
            decoded_html = html_response.decode(encoding)


            print(type(decoded_html), decoded_html)
            data = decoded_html.split('\"')
            # print(data)
            geo = data[3] + ',' + data[7] + ',' + data[11]
        prefix = prefix[:-2] + '<ip:'+ip_sender+'> ' + 'from ' + geo + ' writes: '
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)





if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
