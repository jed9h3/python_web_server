import socket as sk  # importing the socket library as sk


# A function responsible for handling response sending
def send_response(csocket, status, type, filee):
    # sending the response status
    csocket.send(bytes('HTTP/1.1 '+status+'\r\n', "utf-8"))
    # sending the response content-type
    csocket.send(bytes('Content-Type: '+type+'\r\n', "utf-8"))
    csocket.send(bytes('\r\n', "utf-8"))
    if isinstance(filee, str):  # if the file is text being html or css it is sent with encoding
        csocket.send(filee.encode())
    else:  # else the file is binary and its sent without encoding
        csocket.send(filee)


def read_file(loc, rtype):  # A function responsible for handling file opening and reading
    try:  # try statement to catch reading file exceptions to handle them properly
        if rtype == 'rb':  # if reading type is binary no encoding is specified
            f1 = open(loc, rtype)
        else:  # encoding is specified if file reading is text
            f1 = open(loc, rtype, encoding="utf-8")
        file_read = f1.read()  # reading the file
        f1.close()
        return file_read  # returning the read file
    except OSError:
        return None  # returning None if the file doesnt exist to identify that it doesnt


def call_error(csocket, address):  # a function responsible for handling error page calling
    # calling the read function giving it the error.html file with reading type of r
    temp = read_file("error.html", "r")
    # formatting the read error.html file to insert the address and port in a location specified by {info}
    order = temp.format(info=address)
    # sending a 404 response with the formatted error.html file with the send function
    send_response(csocket, '404 Not Found', 'text/html', order)


def main():  # main function where code starts
    port = 5500  # specifying the port
    # giving the host variable the device local ip to start hosting using its host name
    host = "127.0.0.1"

    filename = None  # A variable for holding the value of the file name being requested
    filetype = None  # A variable for holding the content-type for the variable being requested
    statustype = None  # A variable for holding the appropriate response status of the response
    rtype = None  # A variable for holding what type of reading should be performed when opeing a file

    # defining the server socket
    sSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    sSocket.bind((host, port))  # binding the host with the port

    # listening to clients with a request queue with the size of 5
    sSocket.listen(5)
    print("Listening on port %s..." % port)

    while True:  # server listening infinite loop
        rtype = 'r'  # defaulting the reading type to r
        csocket, address = sSocket.accept()  # accepting requests
        print("Received connection from %s" % str(address))

        msg = csocket.recv(1024).decode("utf-8")  # recieving the full request
        print('HTTP REQUEST: '+msg)
        request = msg.split()[1]  # stripping the message out of the request

        # specifying the request info for the main_en.html file
        if (request == '/') or (request == ('/main_en.html')) or (request == '/en') or (request == '/index.html'):
            filename = 'main_en.html'  # specifying the file name
            filetype = 'text/html'  # specifying the file content-type
        elif (request == '/ar'):  # specifying the request info for the main_ar.html file
            filename = 'main_ar.html'
            filetype = 'text/html'
        # specifying the request info for other .html files and .css files
        elif (request.endswith(".html")) or (request.endswith(".css")):
            filename = request[1:]  # stripping the file path from the first /
            # taking out the file extension from the file path
            filetype = 'text/'+request.split('.')[-1]
        # specifying the request info for .jpg .jpeg and .png files
        elif request.endswith('.png') or request.endswith('.jpg') or request.endswith('.jpeg'):
            filename = request[1:]
            filetype = 'image/'+request.split('.')[-1]
            rtype = 'rb'  # overriding the default readinng type to binary reading
        # for handling the redirection requests
        elif (request == '/cr') or (request == '/so') or (request == '/rt'):
            # specifying the response status of the respond
            csocket.send('HTTP/1.1 307 Temporary Redirect\r\n'.encode())
            if (request == '/cr'):  # redirecting to cornell website
                csocket.send('Location://cornell.edu\r\n'.encode())
            elif (request == '/so'):  # redirecting to stackoverflow website
                csocket.send('Location://stackoverflow.com\r\n'.encode())
            elif (request == '/rt'):  # redirecting to ritaj website
                csocket.send('Location://ritaj.birzeit.edu\r\n'.encode())
            csocket.send('\r\n'.encode())
            csocket.close()  # closing the client socket since the request is done
            continue  # jumping to the next loop
        else:
            # calling for the error page since the request is wrong
            call_error(csocket, address)
            csocket.close()
            continue

        statustype = '200 ok'  # specifying the response status
        # calling the read function to fetch the file read given the file path and the reading type
        order = read_file(filename, rtype)
        if order:  # if file exists a 200 ok response is sent
            send_response(csocket, statustype, filetype, order)
        else:  # if the file doesnt exist a call for the error function is sent with the client socket and both the address and port
            call_error(csocket, address)

        csocket.close()

    sSocket.close()


if __name__ == "__main__":  # calling the main function when the server script starts running
    main()
