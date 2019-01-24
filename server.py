# import os
# os.system("pip install pyweatherbit")
from datetime import datetime
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
import subprocess
# from pyweatherbit.api import Api


import urllib.request
import json




clients = {}
addresses = {}
HOST = '25.69.126.127'
# HOST = '10.55.200.133'
# 10.55.123.58
# 25.69.126.127
# '192.168.1.57'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# api_key = "9b79a1a03c414bc58dc6a87f13c941d5"
# api = Api(api_key)
# api.set_granularity('daily')
# forecast = api.get_forecast(city="Moscow")

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
            # if msg == bytes("/weather", "utf8"):
            #     string = "description: " + forecast.json["data"][0]["weather"]['description'] + "\nmax_temp: " + forecast.json["data"][0]["max_temp"] + "\nmin_temp: " + forecast.json["data"][0]["min_temp"]
            #     broadcast_whisper(name.decode("utf8"), string.decode("utf8"), "BOT: The weather is\n")
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
            ip_sender = str(sock_of_sender)[str(sock_of_sender).find('raddr=(\'') + 8:str(sock_of_sender).find('raddr=(\'')+21]
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
        ip_sender = str(sock_of_sender)[str(sock_of_sender).find('raddr=(\'')+8:str(sock_of_sender).find('raddr=(\'')+21]

        with urllib.request.urlopen("https://geoip-db.com/json") as url:
            data = json.loads(url.read().decode())
            print(data)
            geo = data['country_code'] + ',' + data['country_name'] + ',' + data['city']

        # cmd = ['ls']
        # output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        # print(output)

        # geo = '1'
        # geo = os.system("ls")
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
