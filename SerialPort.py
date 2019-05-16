import serial


def open(p, b):
    serPort = ''
    try:
        serPort = serial.Serial(p, b, timeout=1000,
                                parity=serial.PARITY_NONE, rtscts=1)
    except Exception as identifier:
        print("exception-------------", identifier)
    return serPort


def close(serPort):
    try:
        if(serPort.is_open):
            serPort.close()
    except Exception as identifier:
        print("exception-------------", identifier)


def writedata(serPort, d, e):
    try:
        if(serPort.is_open):
            result = serPort.write(d.encode(e))
    except Exception as identifier:
        print("exception-------------", identifier)


def write(serPort, h):
    try:
        if(serPort.is_open):
            result = serPort.write(h)
    except Exception as identifier:
        print("exception-------------", identifier)
    return result


def read(serPort, c):
    try:
        if(serPort.is_open):
            result = serPort.read(c)
    except Exception as identifier:
        print("exception-------------", identifier)
    return result
