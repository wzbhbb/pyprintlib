'''
@Description: REGO printer lib
@Author: steven(wpeng@rgprt.com)
@Date: 2019-05-16
@LastEditTime: 2019-05-16 16:54:42
@steven: Please set LastEditors
'''
import SerialPort
from enum import Enum

printPort = ''


'''
@description: barcodetype
'''
class BarcodeType(Enum):
    UPCA = 65
    UPCE = 66
    EAN13 = 67
    EAN8 = 68
    CODE39 = 69
    ITF = 70
    CODEBAR = 71
    CODE93 = 72
    CODE128 = 73
    QR_CODE = 97
    DATA_MATRIC = 98
    PDF417 = 99


'''
@description: barcode width
'''
class BarcodeWidth(Enum):
    WIDTH2 = 2
    WIDHT3 = 3
    WIDHT4 = 4
    WIDHT5 = 5
    WIDHT6 = 6


'''
@description: barcode hri position
'''
class HRI(Enum):
    HRI_NONE = 0
    HRI_UP = 1
    HRI_DOWN = 2
    HRI_BOTH = 3


'''
@description: open print port
@param {portName} serial port name
@param {type} 1 serial
@return: True Open port success; False Open port failure
'''
def RG_OpenPort(portName, type, spec):
    global printPort
    if(type == 1):  # serial port
        printPort = SerialPort.open(portName, spec)
        if(printPort is not None):
            return True
        else:
            return False


'''
@description: close connection
'''
def RG_ClosePort():
    global printPort
    if(printPort != ''):
        SerialPort.close(printPort)
        printPort = ''


'''
@description: print string
@param {data} print string
@param {encode} string encode, chinese is gb2312
'''
def RG_PrintString(data, encode):
    global printPort
    if(printPort != ''):
        SerialPort.writedata(printPort, data, encode)


'''
@description: clean printer buffer
'''
def RG_Clear():
    global printPort
    cmd = bytearray(b'\x1b\x40')
    if(printPort != ''):
        SerialPort.write(printPort, cmd)


'''
@description: sent align type {0left 1center 2right}
'''
def RG_Align(type):
    global printPort
    cmd = bytearray(b'\x1b\x61\x00')
    if(type == 1):
        cmd[2] = 0x01
    elif(type == 2):
        cmd[2] = 0x02
    if(printPort != ''):
        SerialPort.write(printPort, cmd)


'''
@description: feed paper as dot line
@param{line} dotline pixel
'''
def RG_FeedLine(line):
    global printPort
    cmd = bytearray(b'\x1b\x4a\x00')
    cmd[2] = line

    if(printPort != ''):
        SerialPort.write(printPort, cmd)


'''
@description: let printer cut paper
'''
def RG_CutPaper():
    global printPort
    cmd = bytearray(b'\x1d\x56\x42\x00')

    if(printPort != ''):
        SerialPort.write(printPort, cmd)


'''
@description: set print line spec
@param {spec} 0 is default other is real spec
'''
def RG_LineSpec(spec):
    global printPort
    cmd = ''
    if(spec == 0):
        cmd = bytearray(b'\x1b\x32')
    else:
        cmd = bytearray(b'\x1b\x33\x00')
        cmd[2] = spec

    if(printPort != ''):
        SerialPort.write(printPort, cmd)


'''
@description: change print font style
@param {mini} mini font 
@param {width} times as high, cannot be used with mini fonts
@param {height} times as width, cannot be used with mini fonts
@param {underline} need underline
@param {bold} need bold
'''
def RG_SetFont(mini, width, height, underline, bold):
    global printPort
    cmd = ''
    if(mini):
        cmd = bytearray(b'\x1b\x21\x01\x1c\x21\x01')
    else:
        cmd = bytearray(b'\x1b\x21\x00\x1c\x21\x00\x1d\x21\x00')
        cmd[8] = width << 4 | height
    if(underline):
        cmd[2] |= 0x80
        cmd[5] |= 0x80
    if(bold):
        cmd[2] |= 0x08
        cmd[5] |= 0x08
    if(printPort != ''):
        SerialPort.write(printPort, cmd)


'''
@description: print 1d barcode
@param {type} barcode type
@param {height} barcode height
@param {width} barcode width fix number
@param {hri} barcode HRI position
@param {data} barcode data
'''
def RG_1DBarcode(type, height, width, hri, data):
    global printPort
    cmd = bytearray(b'\x1d\x77\x02\x1d\x68\x00\x1d\x48\x00\x1d\x6b\x00\x00')
    cmd1 = data.encode("gb2312")
    cmd[2] = width.value
    cmd[5] = height
    cmd[8] = hri.value
    cmd[11] = type.value
    cmd[12] = len(cmd1)
    if(printPort != ''):
        SerialPort.write(printPort, cmd)
        SerialPort.write(printPort, cmd1)


'''
@description: print 2d barcode
@param {type} 2d barcode type
@param {width} size of barcode [1,6]
@param {v} version PDF417(1 ≤ v ≤ 30) DATA MATRIX(0 ≤v ≤ 144 0 is auto) QR(0 ≤ v ≤ 40 0 is auto)
@param {r} ecc PDF417(0 ≤ r ≤ 8)  DATA MATRIX(8 ≤ r ≤ 144) QR(r =76,77,81,72)
@param {data} 2d barcode data
@param {encode} data encode
'''
def RG_2DBarcode(type, width, v, r, data, encode):
    global printPort
    cmd = bytearray(b'\x1d\x5a\x00\x1b\x5a\x00\x00\x00\x00\x00')
    cmd[2] = type.value
    cmd[5] = v
    cmd[6] = r
    cmd[7] = width
    cmd1 = data.encode(encode)
    cmd[8] = len(cmd1) % 256
    cmd[9] = int(len(cmd1) / 256)
    if(printPort != ''):
        SerialPort.write(printPort, cmd)
        SerialPort.write(printPort, cmd1)


'''
@description: Query printer status
@return: -1 printer offline 0status ok 1cover open 2paper out
'''
def RG_QueryStatus():
    global printPort
    status = -1
    cmd = bytearray(b'\x10\x04\x01\x10\x04\x02\x10\x04\x03\x10\x04\x04')
    if(printPort != ''):
        SerialPort.write(printPort, cmd)
        r = SerialPort.read(printPort, 4)
        if(r is not None):
            if(r[0] == 0x16):
                status = 0
            elif(r[1] == 0x16):
                status = 1
            elif(r[3] == 0x72):
                status = 2
            else:
                status = 3
    return status

# print job test
if(not RG_OpenPort("COM4", 1, 115200)):
    print("the port connect failue")
    exit

status = RG_QueryStatus()
if(status == -1):
    print("print not connect")
elif(status == 0):
    print("printer status ok")
elif(status == 1):
    print("the cover open")
elif(status == 2):
    print("out of paper")
else:
    print("unknow error")

if(status is not 0):
    print("query status error, exit")
    exit

RG_Clear()
RG_SetFont(False, 1, 1, True, False)
RG_PrintString("print test ok\r\n", "gb2312")
RG_1DBarcode(BarcodeType.EAN8, 50,
             BarcodeWidth.WIDTH2, HRI.HRI_DOWN, "12345678")
RG_2DBarcode(BarcodeType.QR_CODE, 6, 0, 0, "www.rgprt.com", "gb2312")
RG_ClosePort()
