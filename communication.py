import socket
import numpy as np
import sys
import struct
from time import sleep, time, strftime
import logging
from os import getcwd


def setupLogger(verbose):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s-%(process)d-%(levelname)s-%(message)s')
    fh = logging.FileHandler(filename='CommunicationLogs_' + strftime("%d%b%Y") + '.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if verbose:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

# logging.basicConfig(level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')


def getIP():
    # Get the IP address of the computer executing this file
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    temp_sock.connect(('192.168.0.1', 0))
    ip_address = temp_sock.getsockname()[0]
    temp_sock.close()
    return ip_address


class MessageVerification(object):
    def __init__(self, verbose=False):
        self.logger = setupLogger(verbose)

        self.logger.debug("All the errors of communication module will be logged in %s", getcwd())
        self.logger.debug("You can disable the verbosity by removing the 'verbose=True' from the MessageVerification() constructor.")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.timeout = None
        self.port = 65400
        self.backlog = 1  # maximum number of queued connections

    def setTimeout(self, seconds):
        self.timeout = seconds
        self.logger.info("Connection timeout changed to %s", seconds)

    def setPort(self, port_number):
        self.logger.info("Connection port has been changed to %s from %s", self.port_number, self.port)
        self.port = port_number
        self.logger.info("Make sure you also configure both ends of communication.")

    def setNumberOfConnections(self, number):
        self.backlog = number
        self.logger.info("Maximum number of queued connections changed to %s", number)

    def connectToServer(self, ip_address):
        self.logger.info("Connecting to the server on %s", ip_address)
        self.sock.settimeout(self.timeout)
        server_address = (ip_address, self.port)
        try:
            self.sock.connect(server_address)
            self.logger.info('Connected To %s.', server_address)
        except socket.error:
            logging.exception("Error in MessageVerification")
            print('Connection failed. Check server.')
            raise

    def connectToClient(self, ip_address):
        self.logger.debug("Waiting for the client to be connected.")
        self.sock.settimeout(self.timeout)
        server_address = (ip_address, self.port)
        self.sock.bind(server_address)
        self.sock.listen(self.backlog)  # NOTE: maybe have to be changed in future
        try:
            self.sock, address = self.sock.accept()
            self.logger.info("Connection accepted from %s", address)
        except:
            logging.exception("Error in MessageVerification")
            print('Connection failed. Check server.')
            raise

    def sendMessage(self, text):
        self.logger.debug("Sending: %s", text)
        self.sock.sendall(text)
        # sleep(1)
        self.logger.info("Sent: %s", text)

    def verifyMessage(self, text):
        self.logger.info("Waiting for message.")
        received_text = self.sock.recv(4096)
        self.logger.debug("Received: %s", received_text)
        if received_text == text:
            self.logger.info("Successful message verification: %s", text)
            return True
        else:
            self.logger.info("Failed to receive '%s', received '%s' instead.", text, received_text)
            return False

    def close(self):
        self.logger.debug("Closing the connection.")
        self.sock.close()
        self.logger.info("Connection closed.")


class NaslabNetwork(object):

    def __init__(self, ip_address='192.168.0.25'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        server_address = (ip_address, 1895)
        print('Connecting To %s Port %s' % server_address)
        self.sock.connect(server_address)
        self.degree_to_rad = np.pi / 180

    def getStates(self, num):
        # get position
        check = struct.unpack('<B', self.sock.recv(1))[0]
        if check is not 2:
            print('Warning: Bad Qualisys Packet')
            pose_msg_x = float('nan')
        recieved_data = self.sock.recv(4096)
        if len(recieved_data) < 12:
            print('bad 2')
            pose_msg_x = float('nan')
        num_byte = num * 24
        pose_msg_x = struct.unpack('<f', recieved_data[num_byte:num_byte + 4])[0]
        pose_msg_y = struct.unpack('<f', recieved_data[num_byte + 4:num_byte + 8])[0]
        pose_msg_theta = struct.unpack('<f', recieved_data[num_byte + 12:num_byte + 16])[0]
        # print num, pose_msg_theta
        return pose_msg_x, pose_msg_y, pose_msg_theta

    def close(self):
        self.sock.close()


class LabNavigation(object):

    def __init__(self, ip_address='192.168.0.25'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(10)
        server_address = (ip_address, 1895)
        print('Connecting To %s Port %s' % server_address)
        try:
            self.sock.connect(server_address)
        except socket.error:
            print('Connection failed. Check server.')
            raise

    def getStates(self, num):
        # get position
        self.sock.send(str(num))
        packed_buffer = self.sock.recv(25)
        try:
            agent_id = struct.unpack('<B', packed_buffer[:1])[0]
        except struct.error:
            print('Connection terminated by server.')
            raise
        x = struct.unpack('<f', packed_buffer[1:5])[0]
        y = struct.unpack('<f', packed_buffer[5:9])[0]
        z = struct.unpack('<f', packed_buffer[9:13])[0]
        yaw = struct.unpack('<f', packed_buffer[13:17])[0]
        pitch = struct.unpack('<f', packed_buffer[17:21])[0]
        roll = struct.unpack('<f', packed_buffer[21:25])[0]
        return agent_id, x, y, z, yaw, pitch, roll

    def close(self):
        self.sock.close()
