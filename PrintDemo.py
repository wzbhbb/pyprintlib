from printer.PrintLib import *
import xml.sax

# print job test
if(not RG_OpenPort("COM10", 1, 115200)):
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
RG_2DBarcode(BarcodeType.QR_CODE, 6, 0, 0, "www.rgprt.com",
             "gb2312")

RG_ClosePort()
