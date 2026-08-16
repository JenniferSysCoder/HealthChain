class NodeData:
    def __init__(self, pnodeName, pIPAddress, psocketNum):
        self.nodeName = pnodeName
        self.IPAddress = pIPAddress
        self.socketNum = psocketNum

    def get_node_name(self):
        return self.nodeName

    def get_ip_address(self):
        return self.IPAddress

    def get_socket_num(self):
        return self.socketNum
