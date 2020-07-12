#include "Arduino.h"
#include "Brain.h"

MAX_PACKET_LENGTH = 32
EEG_POWER_BANDS = 8

class Brain:
    def __init__(self,brainStream=None,fileStream=None,debug=False):
        # It's up to the calling code to start the stream
        # Usually Serial.begin(9600)


        self.brainStream = brainStream
        self.fileStream = fileStream
        self.debug = debug

        self.packetData = [0]*MAX_PACKET_LENGTH

        self.inPacket = False
        self.latestByte = 0
        self.lastByte = 0
        self.packetIndex = 0
        self.packetLength = 0
        self.checksum = 0
        self.checksumAccumulator = 0
        self.eegPowerLength = 0
        self.hasPower = False

        self.csvBuffer = ""
        self.latestError = ""

        self.signalQuality = 200
        self.attention = 0
        self.meditation = 0

        self.freshPacket = False

        self.eegPower = [0]*EEG_POWER_BANDS


    def update(self):


        if self.brainStream is not None:
            self.latestByte = int.from_bytes(bytearray(self.brainStream.read()),byteorder="big") #should block until bytes are available
        else:
            line = self.fileStream.readline()
            if not line:
                raise EOFError()
            self.latestByte = int(line)
   
        if self.debug: 
            print("LATEST BYTE:",self.latestByte)
              
        # Build a packet if we know we're and not just listening for sync bytes.

        if self.inPacket:
            # First byte after the sync bytes is the length of the upcoming packet.
            if self.packetIndex == 0:
                self.packetLength = self.latestByte
                if self.debug:
                    print("IN PACKET of size",self.packetLength)
                # Catch error if packet is too long
                if self.packetLength > MAX_PACKET_LENGTH:
                    # Packet exceeded max length
                    # Send an error
                    self.latestError = "ERROR: Packet too long " + str(self.packetLength)
                    self.inPacket = False

            elif self.packetIndex <= self.packetLength:
                # Run of the mill data bytes.
                # Print them here
                # Store the byte in an array for parsing later.
                self.packetData[self.packetIndex - 1] = self.latestByte

                # Keep building the self.checksum.
                self.checksumAccumulator += self.latestByte

            elif self.packetIndex > self.packetLength:
                # We're at the end of the data payload.
                # Check the self.checksum.
                self.checksum = self.latestByte
                self.checksumAccumulator = ~(self.checksumAccumulator & 0xFF)
                if self.checksumAccumulator < 0:
                        self.checksumAccumulator += 256

                # Do they match?
                if self.checksum == self.checksumAccumulator:
                    parseSuccess = self.parsePacket()

                    if parseSuccess:
                        self.freshPacket = True
                        if self.debug:
                            print("Good Packet:",self.packetData)

                    else:
                        # Parsing failed, send an error.
                        self.latestError = "ERROR: Could not parse"
                        if self.debug:
                            print("Bad Packet (Couldn't parse):",self.packetData)
                        # good place to print the packet if debugging
                else:
                    # Checksum mismatch, send an error.
                    self.latestError = "ERROR: Checksum"
                    # good place to print the packet if debugging
                    if self.debug:
                        print("Bad Packet (bad checksum):",self.packetData)
                        print("Expected Checksum:",self.checksum,"Received:",self.checksumAccumulator)
                # End of packet
                # Reset, prep for next packet
                self.inPacket = False
            self.packetIndex += 1

        # Look for the start of the packet
        if self.latestByte == 170 and self.lastByte == 170 and not self.inPacket:
            # Start of packet
            self.inPacket = True
            self.packetIndex = 0
            self.checksumAccumulator = 0

        # Keep track of the last byte so we can find the sync byte pairs.
        self.lastByte = self.latestByte

        if self.freshPacket:
            self.freshPacket = False
            return True
        else:
            return False


    def clearPacket(self):
        for i in range(0,MAX_PACKET_LENGTH):
            self.packetData[i] = 0


    def clearEegPower(self):
        # Zero the power bands.
        for i in range(0,EEG_POWER_BANDS):
            self.eegPower[i] = 0


    def parsePacket(self):
        # Loop through the packet, extracting data.
        # Based on mindset_communications_protocol.pdf from the Neurosky Mindset SDK.
        # Returns True if passing succeeds
        self.hasPower = False
        parseSuccess = True
        rawValue = 0

        self.clearEegPower()    # clear the eeg power to make sure we're honest about missing values

        i = 0
        while(i < self.packetLength):
            if self.packetData[i] ==  0x2:
                i += 1
                self.signalQuality = self.packetData[i]
            elif self.packetData[i] == 0x4:
                i += 1
                self.attention = self.packetData[i]
            elif self.packetData[i] == 0x5:
                i += 1
                self.meditation = self.packetData[i]
            elif self.packetData[i] == 0x83:
                # ASIC_EEG_POWER: eight big-endian 3-uint8_t unsigned integer values representing delta, theta, low-alpha high-alpha, low-beta, high-beta, low-gamma, and mid-gamma EEG band power values
                # The next uint8_t sets the length, usually 24 (Eight 24-bit numbers... big endian?)
                # We dont' use this value so let's skip it and just increment i
                i += 1

                # Extract the values
                for j in range(0,EEG_POWER_BANDS):
                    i += 1
                    byte3 = i
                    i += 1
                    byte2 = i
                    i += 1
                    byte1 = i
                    self.eegPower[j] = (self.packetData[byte3] << 16) | (self.packetData[byte2] << 8) | self.packetData[byte1]

                self.hasPower = True
                # This seems to happen once during start-up on the force trainer. Strange. Wise to wait a couple of packets before
                # you start reading.
            elif self.packetData[i] == 0x80:
                # We dont' use this value so let's skip it and just increment i
                # uint8_t self.packetLength = self.packetData[++i]
                i += 1
                i += 1
                byte2 = i
                i += 1
                byte1 = i
                rawValue = (self.packetData[byte2] << 8) | self.packetData[byte1]
            else:
                # Broken packet ?
                
                if self.debug:
                    print("parsePacket UNMATCHED data",hex(self.packetData[i]),"in position",i)
                    self.printPacket()
                
                parseSuccess = False
            i += 1
        return parseSuccess

    # Keeping this around for debug use
    def printCSV(self):
        # Print the CSV over serial
        print(self.signalQuality,self.attention,self.meditation,sep=',',end='')

        if self.hasPower:
            for i in range(0,EEG_POWER_BANDS):
                print(self.eegPower[i],sep=',',end='')

        print("")


    def readErrors(self):
        return self.latestError

    def clearErrors(self):
        self.latestError = ""

    def readCSV(self):
        # spit out a big string?
        # find out how big this really needs to be
        # should be popped off the stack once it goes out of scope?
        # make the character array as small as possible

        if self.hasPower:

            self.csvBuffer = str(self.signalQuality) + "," + \
                            str(self.attention) + "," + \
                            str(self.meditation) + "," + \
                            str(self.eegPower[0]) + "," + \
                            str(self.eegPower[1]) + "," + \
                            str(self.eegPower[2]) + "," + \
                            str(self.eegPower[3]) + "," + \
                            str(self.eegPower[4]) + "," + \
                            str(self.eegPower[5]) + "," + \
                            str(self.eegPower[6]) + "," + \
                            str(self.eegPower[7])

            return self.csvBuffer
        else:
            self.csvBuffer = str(self.signalQuality) + "," + \
                             str(self.attention) + "," + \
                             str(self.meditation)

            return self.csvBuffer

    # For debugging, print the entire contents of the packet data array.
    def printPacket(self):
        print("[",end="")
        for i in range(0, MAX_PACKET_LENGTH):
            print(self.packetData[i],end=", ")
        print("]")

    def printDebug(self):
        print("")
        print("--- Start Packet ---")
        print("Signal Quality: ",self.signalQuality)
        print("Attention: ",self.attention)
        print("Meditation: ",self.meditation)

        if self.hasPower:
            print("")
            print("EEG POWER:")
            print("Delta: ",self.eegPower[0])
            print("Theta: ",self.eegPower[1])
            print("Low Alpha: ",self.eegPower[2])
            print("High Alpha: ",self.eegPower[3])
            print("Low Beta: ",self.eegPower[4])
            print("High Beta: ",self.eegPower[5])
            print("Low Gamma: ",self.eegPower[6])
            print("Mid Gamma: ",self.eegPower[7])

        print("")
        print("Checksum Calculated: ",self.checksumAccumulator)
        print("Checksum Expected: ",self.checksum)

        print("--- End Packet ---")
        print("")

    def readSignalQuality(self):
        return self.signalQuality


    def readAttention(self):
        return self.attention


    def readMeditation(self):
        return self.meditation


    def readPowerArray(self):
        return self.eegPower


    def readDelta(self):
        return self.eegPower[0]


    def readTheta(self):
        return self.eegPower[1]


    def readLowAlpha(self):
        return self.eegPower[2]


    def readHighAlpha(self):
        return self.eegPower[3]


    def readLowBeta(self):
        return self.eegPower[4]


    def readHighBeta(self):
        return self.eegPower[5]


    def readLowGamma(self):
        return self.eegPower[6]


    def readMidGamma(self):
        return self.eegPower[7]



