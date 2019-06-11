'''
@Description: REGO printer lib
@Author: steven(wpeng@rgprt.com)
@Date: 2019-05-16
@LastEditTime: 2019-06-11 18:15:55
@steven: Please set LastEditors
'''
from port.SerialPort import *
from enum import Enum
from xml.dom.minidom import parse
import xml.dom.minidom

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
        printPort = open(portName, spec)
        if(printPort == ''):
            return False
        else:
            return True


'''
@description: close connection
'''
def RG_ClosePort():
    global printPort
    if(printPort != ''):
        close(printPort)
        printPort = ''


'''
@description: print string
@param {data} print string
@param {encode} string encode, chinese is gb2312
'''
def RG_PrintString(data, encode):
    global printPort
    if(printPort != ''):
        writedata(printPort, data, encode)

'''
@description: print string
@param {data} print string
@param {encode} string encode, chinese is gb2312
'''
def RG_PrintBuffer(data):
    global printPort
    if(printPort != ''):
        write(printPort, data)


'''
@description: clean printer buffer
'''
def RG_Clear():
    global printPort
    cmd = bytearray(b'\x1b\x40')
    if(printPort != ''):
        write(printPort, cmd)


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
        write(printPort, cmd)


'''
@description: feed paper as dot line
@param{line} dotline pixel
'''
def RG_FeedLine(line):
    global printPort
    cmd = bytearray(b'\x1b\x4a\x00')
    cmd[2] = line

    if(printPort != ''):
        write(printPort, cmd)


'''
@description: let printer cut paper
'''
def RG_CutPaper():
    global printPort
    cmd = bytearray(b'\x1d\x56\x42\x00')

    if(printPort != ''):
        write(printPort, cmd)


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
        write(printPort, cmd)


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
        write(printPort, cmd)


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
        write(printPort, cmd)
        write(printPort, cmd1)


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
        write(printPort, cmd)
        write(printPort, cmd1)


'''
@description: Query printer status
@return: -1 printer offline 0status ok 1cover open 2paper out
'''
def RG_QueryStatus():
    global printPort
    status = -1
    cmd = bytearray(b'\x10\x04\x01\x10\x04\x02\x10\x04\x03\x10\x04\x04')
    if(printPort != ''):
        write(printPort, cmd)
        r = read(printPort, 4)
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


def RGLP_PageStart(posX, posY, width, height, paperType, pageDirection):
    global printPort
    if(printPort != ''):
        pt = bytearray(b'\x1b\x63\x30\x00')
        pageMode = bytearray(b'\x1b\x4c')
        pd = bytearray(b'\x1b\x54\x00')
        clearBuffer = bytearray(b'\x18')

        pt[3] = paperType
        pd[2] = pageDirection
        write(printPort, pt + pageMode + pd + clearBuffer)

        pageDim = bytearray(b'\x1b\x57\x00\x00\x00\x00\x00\x00\x00\x00')
        pageDim[2] = posX % 256
        pageDim[3] = (int)(posX / 256)
        pageDim[4] = posY % 256
        pageDim[5] = (int)(posY / 256)
        pageDim[6] = width % 256
        pageDim[7] = (int)(width / 256)
        pageDim[8] = height % 256
        pageDim[9] = (int)(height / 256)
        write(printPort, pageDim)

def getPos(posX, posY):
    a = bytearray(b'\x1b\x5c\x00\x00\x1d\x24\x00\x00')
    a[2] = posX % 256
    a[3] = (int)(posX / 256)
    a[6] = posY % 256
    a[7] = (int)(posY / 256)
    return a


def RGLP_OppsiteColor(oppsite):
    global printPort
    if(printPort != ''):
        a = bytearray(b'\x1d\x42\x00')
        a[2] = oppsite
        write(printPort, a)


def RGLP_PrintText(posX, posY, mini, underline, width, height, bold,
                   data, encode):
    global printPort
    if(printPort != ''):
        a = bytearray(b'\x1b\x21\x00')
        if(mini):
            a[2] |= 0x01
        elif(width or height):
            if(width):
                a[2] |= 0x20
            if(height):
                a[2] |= 0x10
        if(bold):
            a[2] |= 0x08
        if(underline):
            a[2] |= 0x80
        write(printPort, a)
        write(printPort, getPos(posX, posY))
        writedata(printPort, data, encode)


def RGLP_1DBarcode(posX, posY, hri, height, width, data):
    global printPort
    if(printPort != ''):
        seting = bytearray(
            b'\x1d\x68\x00\x1d\x77\x00\x1d\x48\x00\x1d\x6b\x49\x00')
        seting[2] = height
        seting[5] = width
        seting[8] = hri
        seting[12] = len(data)
        write(printPort, getPos(posX, posY))
        write(printPort, seting)
        writedata(printPort, data, "utf-8")


def RGLP_2DBarcode(posX, posY, size, ecc, data):
    global printPort
    if(printPort != ''):
        qrsize = bytearray(b'\x1d\x28\x6b\x03\x00\x31\x43\x00')
        qrsize[7] = size
        qrecc = bytearray(b'\x1d\x28\x6b\x03\x00\x31\x45\x00')
        qrecc[7] = ecc+48
        write(printPort, getPos(posX, posY))
        write(printPort, qrsize+qrecc)

        qrcontent = data.encode("utf-8")
        qrlen = len(qrcontent)
        qrdata = bytearray(b'\x1d\x28\x6b\x00\x00\x31\x50\x30')
        qrdata[3] = (qrlen+3) % 256
        qrdata[4] = (int)((qrlen+3) / 256)
        write(printPort, qrdata)
        write(printPort, qrcontent)

        qrprint = bytearray(b'\x1d\x28\x6b\x00\x00\x31\x51\x30')
        write(printPort, qrprint)


def RGLP_Rectange(posX, posY, width, height):
    global printPort
    if(printPort != ''):
        seting = bytearray(
            b'\x1b\x6d\x00\x00\x00\x00\x00\x00\x00\x00')
        seting[2] = posX % 256
        seting[3] = int(posX / 256)
        seting[4] = posY % 256
        seting[5] = int(posY / 256)
        seting[6] = width % 256
        seting[7] = int(width / 256)
        seting[8] = height % 256
        seting[9] = int(height / 256)
        write(printPort, seting)


'''
@description: Query LP561 printer status
@return: -1 printer offline 0status ok; 1 Paper sensor detected no paper; 2 Paper presence sensor detects paper presence
'''
def RGLP_QueryStatus():
    global printPort
    status = -1
    cmd = bytearray(b'\x10\x04\x04')
    if(printPort != ''):
        write(printPort, cmd)
        r = read(printPort, 1)
        if(r is not None):
            if(r[0] & 0x60):
                status = 1
            elif(r[0] == 0x0c):
                status = 2
            else:
                status = 0
    return status


def RGLP_PageEnd():
    global printPort
    if(printPort != ''):
        a = bytearray(b'\x0c')
        write(printPort, a)

def RGLP_PrintXML(fileName):
    DOMTree = xml.dom.minidom.parse(fileName)
    collection = DOMTree.documentElement
    lastOppsite = False

    config = collection.getElementsByTagName("config")
    wx = config[0].childNodes
    for node in wx:
        if(node.nodeType == 1):
            print(node.nodeName + ": " + node.childNodes[0].data)
            if(node.nodeName == "startX"):
                startX = node.childNodes[0].data
            if(node.nodeName == "startY"):
                startY = node.childNodes[0].data
            if(node.nodeName == "width"):
                width = node.childNodes[0].data
            if(node.nodeName == "height"):
                height = node.childNodes[0].data
            if(node.nodeName == "paper"):
                if(node.childNodes[0].data == "serial"):
                    paper = 0
                elif(node.childNodes[0].data == "label-with-rollback"):
                    paper = 1
                else:
                    paper = 2
            if(node.nodeName == "direction"):
                # left-right bottom-up right-left up-bottom
                if(node.childNodes[0].data == "left-right"):
                    direction = 0
                elif(node.childNodes[0].data == "bottom-up"):
                    direction = 1
                elif(node.childNodes[0].data == "right-left"):
                    direction = 2
                elif(node.childNodes[0].data == "up-bottom"):
                    direction = 3

    RGLP_PageStart(int(startX), int(startY), int(width), int(height), paper, direction)

    content = collection.getElementsByTagName("content")
    wx = content[0].childNodes
    for node in wx:
        if(node.nodeType == 1):
            if node.hasAttribute("x"):
                posX = node.getAttribute("x")
            if node.hasAttribute("y"):
                posY = node.getAttribute("y")

            mini = False
            if node.hasAttribute("mini"):
                mini = True
            underline = False
            if node.hasAttribute("underline"):
                underline = True
            bold = False
            if node.hasAttribute("bold"):
                bold = True
            width = False
            if node.hasAttribute("width"):
                width = True
            height = False
            if node.hasAttribute("height"):
                height = True
            line = False
            if node.hasAttribute("line"):
                line = True
            opposite = False
            if node.hasAttribute("opposite"):
                opposite = True
            if node.hasAttribute("size"):
                size = node.getAttribute("size")
            if node.hasAttribute("ecc"):
                ecc = node.getAttribute("ecc")

            if(lastOppsite != opposite):
                RGLP_OppsiteColor(opposite)
                lastOppsite = opposite

            if(node.nodeName == "text"):
                data = node.childNodes[0].data
                if(line):
                    data += "\n"
                RGLP_PrintText(int(posX), int(posY), mini, underline, width, height, bold, data, "utf-8")
            elif(node.nodeName == "qrcode"):
                RGLP_2DBarcode(int(posX), int(posY), int(size), int(ecc), node.childNodes[0].data)
            elif(node.nodeName == "rectangle"):
                width = node.getAttribute("width")
                height = node.getAttribute("height")
                RGLP_Rectange(int(posX), int(posY), int(width), int(height))

    RGLP_PageEnd()
