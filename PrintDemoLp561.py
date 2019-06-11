from printer.PrintLib import *
import xml.sax
import sys

# print job test
if(not RG_OpenPort("COM10", 1, 115200)):
    print("the port connect failue")
    exit

status = RGLP_QueryStatus()
if(status == -1):
    print("print not connect")
elif(status == 0):
    print("printer status ok")
elif(status == 1):
    print("Paper sensor detected no paper")
elif(status == 2):
    print("Paper presence sensor detects paper presence")
else:
    print("unknow error")

if(status is not 0):
    print("query status error, exit")
    sys.exit(0)


# RGLP_PageStart(50, 0, 400, 600, 2, 0)
# RGLP_Rectange(70, 10, 360, 100)
# RGLP_PrintText(40, 35, True, False, True, True, True, 'VIBRANT CARE PHARMACY INC\n', 'utf-8')
# RGLP_PrintText(40, 65, True, False, True, True, True, 'Ph:(510) 638-9851 Fax:(510) 638-9852\n', 'utf-8')
# RGLP_PrintText(40, 95, True, False, True, True, False, '7400 MACARTHUR BLVD OAKLAND, CA 94605\n', 'utf-8')

# RGLP_PrintText(30, 140, False, False, False, False, True, 'Rx No.', 'utf-8')
# RGLP_PrintText(20, 140, True, False, False, False, False, 'Doctor Name', 'utf-8')
# RGLP_PrintText(40, 140, True, False, False, False, False, 'Facility Name\n', 'utf-8')

# RGLP_PrintText(30, 175, False, False, False, False, True, 'Patient_Name\n', 'utf-8')
# RGLP_PrintText(30, 205, False, False, False, False, False, 'Drug_Name', 'utf-8')
# RGLP_PrintText(30, 205, False, False, False, False, False, '#Quantity', 'utf-8')
# RGLP_2DBarcode(30, 205, 3, 1, "www.rgprt.com")
# RGLP_PrintText(30, 235, False, False, False, False, False, 'SIG in Preferred Language', 'utf-8')
# RGLP_PrintText(30, 265, False, False, False, False, False, 'Caution:', 'utf-8')
# RGLP_PrintText(30, 295, False, False, False, False, True, 'HOA: 8:00 AM 10:00 PM', 'utf-8')

# RGLP_PrintText(30, 325, True, False, False, False, False, 'Filled Date:', 'utf-8')
# RGLP_PrintText(30, 325, True, False, False, False, False, 'Exp Date:', 'utf-8')
# RGLP_OppsiteColor(True)
# RGLP_PrintText(30, 325, True, False, False, False, False, 'NDC: 00000000000000\n', 'utf-8')
# RGLP_Rectange(70, 380, 360, 100)
# RGLP_OppsiteColor(False)
# RGLP_PrintText(40, 400, True, False, True, True, False, 'Federal or state law prohibits transfer of this prescription to any\n', 'utf-8')
# RGLP_PrintText(40, 465, True, False, True, True, False, 'person other than patient for whom it was prescribed.\n', 'utf-8')
# RGLP_PageEnd()

RGLP_PrintXML("print.xml")
RG_ClosePort()
