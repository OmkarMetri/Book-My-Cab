from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    
    while True:
        global count
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        count =count+1
        client.send(bytes("Greetings from the bookurcab! Now type your name and press enter!", "utf8"))
        #print(count)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def options_handle(client,msg,to_store=[]):
    print(msg)
    if (msg==bytes("pool","utf8")):
        res='you have booked cab from %s to %s' %(str(to_store[0],"utf8"),str(to_store[1],"utf8"))
        client.send(bytes(res, "utf8"))
        pool_handle(client,pool_list,to_store)

    else:
        res='you have booked cab from %s to %s' %(str(to_store[0],"utf8"),str(to_store[1],"utf8"))
        client.send(bytes(res, "utf8"))

def pool_handle(client,pool_list=[],to_store=[]):
    global count
    one = 1
    #print("kkkkkkkkkkkkkkkkkk")
    
    print(len(pool_list))
    if(len(pool_list)<1):
        pool_list.append([to_store[0],to_store[1],one,[client]])
        #print(len(pool_list))
        #client_list.append([client])

    else:
        for i in range(len(pool_list)):
            #print(len(pool_list))
            #print(i)
            if(to_store[0]==pool_list[i][0] and to_store[1]==pool_list[i][1] and pool_list[i][2]<5):
                pool_list[i][2]=pool_list[i][2]+1
                pool_list[i][3].append(client)
                broadcast(pool_list[i][3])
                count = count-1
            else:
                pool_list.append([to_store[0],to_store[1],one, [client]])


def handle_client(client):  
    global count
    name = client.recv(BUFSIZ).decode("utf8")
    if(count<7):
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        user_list.append([client,name])
        client.send(bytes(welcome, "utf8"))
        src = 'enter your pick up  point'
        client.send(bytes(src, "utf8"))
        to_store = []
        new = "You are travelling with %s" % name
        notify(bytes(new, "utf8"))
        clients[client] = name

    else:
        welcome = 'Welcome %s! oopsss!!! sorry there are no cabs available' % name
        client.send(bytes(welcome, "utf8"))
        client.send(bytes("please {quit}", "utf8"))
    while True:

        msg = client.recv(BUFSIZ)
        print(msg)
        if (msg == bytes("pool","utf8") or msg == bytes("go","utf8")):
            print(msg)
            options_handle(client,msg,to_store)
            """if (msg == bytes("pool","utf8"):
                pool_handle()
            else:
                go_handle()"""

        elif msg != bytes("{quit}", "utf8"):
            
            to_store.append(msg)
            #print(len(to_store))
            if(len(to_store)==1):
                dest = 'enter your drop  point'
                client.send(bytes(dest, "utf8"))
            elif(len(to_store)==2):
                client.send(bytes("options","utf8"))


                #res='you have booked cab from %s to %s' %(str(to_store[0],"utf8"),str(to_store[1],"utf8"))
                #client.send(bytes(res, "utf8"))
                
            else:
                qu='please type {quit} once you reach your destination'
                client.send(bytes(qu, "utf8"))
                continue


        else:
            count = count-1
            client.send(bytes("{quit}", "utf8"))
            leave = "%s has left the car" % name
            notify(bytes(leave, "utf8"))
            client.close()
            del clients[client]
            break

def notify(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

def broadcast(client_list=[]):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    
    for inm in client_list:
        for final in user_list:
            if (inm == final[0]):
                res_list.append(final[1])

    str1 = ''.join(str(e) for e in res_list)
    msg = str1 + 'are pooling'

    for sock in client_list:
        sock.send(bytes(msg, "utf8"))

        
clients = {}
addresses = {}
pool_list =[]
client_list = []
user_list = []
res_list = []
HOST = ''
PORT = 33000
BUFSIZ = 1024
global count
count = 0
ADDR = (HOST, PORT)


SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()
