import socketimport struct localIP     = "127.0.0.1"localPort   = 20001bufferSize  = 1024# Create a datagram socketUDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)# Bind to address and ipUDPServerSocket.bind((localIP, localPort))print("UDP server up and listening") # Listen for incoming datagramswhile(True):    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)    message = bytesAddressPair[0]    address = bytesAddressPair[1]    clientMsg = "Message from Client:{}".format(message)    clientIP  = "Client IP Address:{}".format(address)    pos= struct.unpack('hhf10s',message)    posx, posy, posz, note= pos        print(clientIP)    print(len(clientMsg))    print(posx)    print(posy)    print(posz)    print(note)        