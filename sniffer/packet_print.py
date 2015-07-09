
# Packet sniffer for site debugging by budge
# It is using serial parsing for TinyOS 2.1.1 packet, CTP is basic
# But, specially for the Yggdrasil packet parsing, 
# which is developed based on TinyOS 2.1.1 and modified by Sonnonet in Korea
# in the start point, it needs hardware Kmote or Telosb compliant mote with proper Channel and Group ID
# The application in the mote is BASESTATION which located in ...TinyOS_Main_Dir/apps/Basestation
# Be careful not to use Basestation.15.4 
# this SW has so long boring upgrades from 2003, now moved to Python world
# you can see the packet format and description in wwww.tinyospacket.com
# default baudrate is 115200, which is the defualt value in TinyOS-2.1.1

import serial,os,time
import sys

count, count7e, count7d, comment , nodefor=0, 0, 0, 0, 0
file_=0
temp,tempsub,value,start,end=[],[],[],[],[]
value_,start_,end_,output="","","",""
nodesub, typesub="", ""
node_, type_=[],[]
count = 0
#default baudrate is 115200
default_baudrate = 115200
baudrate = default_baudrate
targetID = -1
targetType = -1
destID = -1
volubility = 0
pckType = 'all'
timeStart=time.time()

def timePrint() :
    timeCurr=time.time()
    print
    print "Up Time : %d sec." %(timeCurr-timeStart)

def dataPrint() :
    parsing_batt_data = int(packet_buf_array[30],16)*256 + int(packet_buf_array[31],16) 
    print " >> BATT. =", parsing_batt_data

def idsPrint() :
    dest_id_d   = int(packet_buf_array[3],16)*256 + int(packet_buf_array[4],16) 
    src_id_d    = int(packet_buf_array[5],16)*256 + int(packet_buf_array[6],16) 
    origin_id_d = int(packet_buf_array[14],16)*256 + int(packet_buf_array[15],16) 

    dest_id_h   = hex(dest_id_d)
    src_id_h    = hex(src_id_d)
    origin_id_h = hex(origin_id_d)
       
    print "  Packet Type is ", pckType 
    if pckType is 'data':
        print ' >> (14:15) ori.ID =', origin_id_d, origin_id_h ,
    if pckType is 'data':
        print ' >> ( 3: 4) dst.ID =', dest_id_d, dest_id_h , 
    print ' >> ( 5: 6) src.ID =', src_id_d, src_id_h  

volubility = len(sys.argv)
print "  "
print "  Thanks for the try, SW execution time : ", timeStart , " >> Volubility, Arg length = ", volubility
if volubility > 1:
    usbdev = sys.argv[1]
    print "  sys.argv[%d],USB Dev = %s" % (1, usbdev) ,

if volubility > 2:
    baudrate = int(sys.argv[2])
    print "  sys.argv[%d],serial speed = %d" % (2, baudrate) ,
   
if volubility > 3:
    pckType = sys.argv[3]
    print "  sys.argv[%d],pckType = %s" % (3, pckType) ,

if volubility > 4:
    targetID = int(sys.argv[4])
    print "  sys.argv[%d],targetID = %d" % (3, targetID) ,

if volubility > 5:
    destID = int(sys.argv[5])
    print "  sys.argv[%d],Dest ID = %d" % (4, destID) ,

if volubility is 1 :
    print "  Stop running, Please check and type serial dev, for instance, (Mac OSX: /dev/cu.usbxxxx)"
    print "  Defualt baudrate is 115200, TinyOS-2.1.2 & Yggdrasil using 115200"
    print "  Example> python packet_print.py {serial device} {serial speed} {packet type, all | data | route} {node ID} {packet type}"
    print "         > python packet_print.py {serial device} will show all packet by serial 115200 speed" 
    print "         > python packet_print.py /dev/ttyUSB0 57600 all 7 119 "
    print "         > python packet_print.py /dev/ttyUSB0 57600 route 7 119 "
    print "         > python packet_print.py /dev/cu.usbABC 115200 data | grep 811 "
    print "  Bye"
    exit()

serial_in_dev = serial.Serial(usbdev,baudrate)

timestamp=time.localtime()
print time.asctime(timestamp)

#packet_buf_array = range(128)
packet_buf_array = ['-' for pbuf_index in range(128)]
packet_print_cnt = 0
packet_inbyte_idx = 0
sync_bytes_detect = 0

while 1 :
    in_byte = serial_in_dev.read(1).encode('hex')

#   just one-time run at the start
    if (in_byte == '7e') and (packet_buf_array[0] != '7e') :
        packet_buf_array[packet_inbyte_idx] = in_byte
        packet_inbyte_idx += 1
        sync_bytes_detect = 0

#   continuously re-visit on every packet
#    if (in_byte == '7e') and (packet_buf_array[0] == '7e') :
#       do nothing
#       continue
#       break

    if (packet_buf_array[0] == '7e') and (in_byte == '45') and (sync_bytes_detect == 0) :
        packet_print_cnt += 1 
        packet_buf_array[packet_inbyte_idx] = in_byte
        packet_inbyte_idx += 1
        sync_bytes_detect = 1
    elif (sync_bytes_detect == 1) :
        packet_buf_array[packet_inbyte_idx] = in_byte
        packet_inbyte_idx += 1
        if packet_inbyte_idx > 126 :
            packet_inbyte_idx = 0
            packet_buf_array = ['-' for pbuf_index in range(128)]
            continue

    if (sync_bytes_detect == 1) and (in_byte == '7e') :
        print_idx = packet_inbyte_idx
        packet_inbyte_idx = 0
        pckTypeID = int(packet_buf_array[9],16)
        if (pckTypeID == 0x70) : 
            pckType = 'route'
        elif (pckTypeID == 0x71) : 
            pckType = 'data'
        elif (pckTypeID == 0x60) : # dissemination
            pckType = 'ds' #dissemination
           
        if (volubility > 3) : #check in coming packet Type ID
            if ('data' in sys.argv) :
                if not (pckTypeID is 0x71):
                    packet_buf_array = ['-' for pbuf_index in range(128)]
                    continue
            elif ('route' in sys.argv):
                if not (pckTypeID is 0x70):
                    packet_buf_array = ['-' for pbuf_index in range(128)]
                    continue
            
        if (volubility > 4) : # volubility 4 defines targetID
            if((int(packet_buf_array[14],16)*256 + int(packet_buf_array[15],16)) != targetID) :
                packet_buf_array = ['-' for pbuf_index in range(128)]
                continue 
            timePrint()
#        if (volubility < 5) :
#        if ((int(packet_buf_array[14],16)*256 + int(packet_buf_array[15],16)) != targetID) : 
#                print "Target Pakcet ID = ", targetID
#                print "other packet"
#                continue
        timePrint()
        print '[pcnt]', packet_print_cnt 
        print '[pkt]', packet_buf_array[:print_idx]
        if volubility > 2 :
            idsPrint()
        if volubility > 2 and (pckType is 'data' or pckType is 'all'):
            dataPrint()    

        packet_buf_array = ['-' for pbuf_index in range(128)]

'''
if hex(ord(result))=='0x7e' :
            count7e=count7e+1
        if hex(ord(result))=='0x7d' :
            count7d=count7d+1
            continue
        if count7d==1 and hex(ord(result))==0x5e :
            result=chr(int(0x7e))
            count7d=0
        elif count7d==1 and hex(ord(result))==0x5d :
            result=chr(int(0x7d))
            count7d=0
        if essence=="DEC" or essence=="dec" :
            for i in range(0,len(result)) :
                temp.append(ord(result[i]))
        elif essence=="HEX" or essence=="hex" :
            for i in range(0,len(result)) :
                tempsub.append(ord(result[i]))
                temp.append(hex(ord(result[i])))
#            if (temp[0] == 0x45) :
#				temp[0] = 0x7e
#				temp[1] = 0x45
#				count7e = 1
       #end[-1]=len(temp)
        #if (len(temp) > 27) and (temp[0] == '0x7e') :
        print(len(temp))
        if (len(temp) > 27) :
			if (temp[0]=='0x45') :
				pkt_offset = 1
				nodeid = int(temp[25],16)*256+int(temp[26],16)
				nodeidStr = str(nodeid)
				pktType = int(temp[8],16)
				parentID = int(temp[2],16)*256+int(temp[3],16)
				if (targetID == -1) :
					print "All packet 45 -> node id " + nodeidStr + " / " + temp[25],temp[26]
					continue
				elif (targetID == nodeid) :
					if ((targetType != -1) and (targetType != pktType) ) :
						print '#',
						continue
					print
					timePrint()
					print "Target Packet node id " + nodeidStr + " / " + temp[25] + " " + temp[26],
					if (temp[8]=='0x71') :
						print "   DataPacket 0x71 ",
						print "parentID = %d, 0x%x" % (parentID,parentID)
						#print temp
					if (temp[8]=='0x70') : print "   RoutePacket 0x70 "
					if (temp[8]=='0x60') : print "   Dissemination 0x60 "
				#print '-',

			elif (temp[0]=='0x7e') :
				pkt_offset = 0
				nodeid = int(temp[26],16)*256+int(temp[27],16)
				nodeidStr = str(nodeid)
				pktType = int(temp[9],16)
				parentID = int(temp[3],16)*256+int(temp[4],16)
				if (targetID == -1) :
					print "All packet 7e -> node id " + nodeidStr + " / " + temp[26],temp[27]
					continue
				elif (targetID == nodeid) :
					if ((targetID != -1) and (targetID == nodeid)) :
						if ((targetType != -1) and (targetType != pktType)) :
							print '#',
							continue
						print
						timePrint()
						print "_Target packet -> node id " + nodeidStr + " / " + temp[26],temp[27]
  					if (temp[9]=='0x71') :
							print "_DataPacket 0x71 ",
							print "_parentID = %d, 0x%x" % (parentID,parentID)
							#print temp
        if (temp[9]=='0x70') : print "   _RoutePacket 0x70 "
        if (temp[9]=='0x60') : print "   _Dissemination 0x60 "
        #print '-' ,

    nodeid = 0
    count7e, count7d=0 ,0
    temp=[]
    tempsub=[]
        #if essence== "HEX" or essence=="hex" :
        count7e, count7d=0 ,0
        if essence== "HEX" or essence=="hex" :
            if node_ != [] :
                for i in range(0,len(node_)) :
                    if temp[9] == node_[i] :
                        print "type = " + str(node_[i])
                        print "count : " + str(count)
                        count+=1
                        for j in range(0,len(value)) :
                            output+=value[j] + " : "
                            for k in range((int(start[j])-1),int(end[j])) :
                                output+= str(temp[k]) + " "
                            if start[j] != end[j] :
                                a =int(start[j])-1
                                b = int(end[j])-1
                                print output, int(temp[a],16)*256+int(temp[b],16)
                            else :
                                print output
                            output=""
                        print
            else :
                for i in range(0,len(value)) :
                    output+=value[i] + " : "
                    for j in range((int(start[i])-1),int(end[i])) :
                        output+= str(temp[j]) + " "
                    if start[j] != end[j] :
                        a =int(start[j])-1
                        b = int(end[j])-1
                        print output, int(temp[a],16)*256+int(temp[b],16)
                    else :
                        print output
                    output=""
            temp=[]
            tempsub=[]

        else :
            print "HEX error"

if len(sys.argv) is 1:


print "number option %d" % (len(sys.argv) - 1)


print "\n<list >"

for i in range(len(sys.argv)):
  print "sys.argv[%d] = '%s'" % (i, sys.argv[i])


'''
