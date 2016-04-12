
def Checksum(packet):
    chksum = 0
    for b in packet:
        chksum ^= b
    return bytes([chksum])


def HasValidChecksum(packet):
    chksum = bytes([packet[-1]])
    return Checksum(packet[:-1]) == chksum


def FindValidPacket(packet, header, length=None, lengthIndex=None, lengthOffset=0, ChksumIncludeHeader=True):
    if length == None and lengthIndex == None:
        raise ValueError("Either length or lengthIndex must be set")
    if len(header) == 0:
        raise ValueError("header must be set")

    checkedPacketList = list()
    remainedPacket = b""
    packetLength = 0
    while True:
        # Find the first header in packet
        index = packet.find(header[0])
        if index < 0:
            break
        print("Found first header index: {}".format(index))
        # Remove everything in front of the first header
        packet = packet[index:]
        # Test the remained packet length
        if length is not None:
            if len(packet) < length+lengthOffset:
                remainedPacket += packet
                break
            packetLength = length + lengthOffset
        else:
            if (len(packet) < lengthIndex+1) or \
                    (len(packet) < packet[lengthIndex]+lengthOffset):
                remainedPacket += packet
                break
            packetLength = packet[lengthIndex] + lengthOffset
        print("Packet length: {}".format(packetLength))
        # Compare the rest of the header
        if packet.startswith(header) is False:
            # Skip the first found header
            packet = packet[1:]
            continue
        print("Found rest of the header")
        # Check the checksum
        if ChksumIncludeHeader:
            if HasValidChecksum(packet[:packetLength]) is False:
                packet = packet[1:]
                continue
        else:
            if HasValidChecksum(packet[len(header):packetLength]) is False:
                packet = packet[1:]
                continue
        print("Checksum validation passed")
        # Pass every examination
        checkedPacketList.append(packet[:packetLength])
        packet = packet[packetLength:]
        print("Current checkedPacketList:")
        print(checkedPacketList, "\n")
    
    print(" Final checkedPacketList:")
    print(checkedPacketList)
    print(" Remained packet:")
    print(remainedPacket)
    return (checkedPacketList, remainedPacket)













