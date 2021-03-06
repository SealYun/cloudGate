# -*- coding:utf-8 -*-


class NetworkingProcessorBase():
    def __init__(self):
        pass

    def getNetwotks(self, shared, tenantID, routerExternal):
        pass

    def createNetwork(self, inNetwork):
        pass

    def createNetworks(self, inNetworks):
        pass

    def getAPIExtensions(self):
        pass

    def getNetwork(self, networkID):
        pass

    def updateNetwork(self, networkID, inNetwork):
        pass

    def deleteNetwork(self, networkID):
        pass

    def getDHCPAgents(self, networkID):
        pass

    def getSubsets(self, displayName, networkID, gatewayIP, ipVersion, cidr, id, enableDHCP, ipv6RaMode, ipv6AddressMode):
        pass

    def createSubnet(self, inSubnet):
        pass

    def createSubnets(self, inSubnets):
        pass

    def getSubnet(self, subnetID):
        pass

    def updateSubnet(self, subnetID, inSubnet):
        pass

    def deleteSubnet(self, subnetID):
        pass

    def getPorts(self, status, displayName, adminState, networkID, tenantID, deviceOwner, macAddress, portID, securityGroups, deviceID):
        pass

    def createPort(self, inPort):
        pass

    def createPorts(self, inPorts):
        pass

    def getPort(self, portID):
        pass

    def updatePort(self, portID, inPort):
        pass

    def deletePort(self, portID):
        pass

    def getLoadBalancers(self):
        pass

    def createLoadBalancer(self, inLoadBalancer):
        pass

    def getLoadBalancer(self, lbID):
        pass

    def updateLoadBalancer(self, lbID, inLoadBalancer):
        pass

    def deleteLoadBalancer(self, lbID):
        pass

    def getLoadBalancerStatuses(self, lbID):
        pass

    def getListeners(self):
        pass

    def createListener(self, inListener):
        pass

    def getListener(self, listenerID):
        pass

    def updateListener(self, listenerID, inListener):
        pass

    def deleteListener(self, listenerID):
        pass

    def getPools(self):
        pass

    def createPool(self, inPool):
        pass

    def getPool(self, poolID):
        pass

    def updatePool(self, poolID, inPool):
        pass

    def deletePool(self, poolID):
        pass

    def getPoolMembers(self, poolID):
        pass

    def createPoolMember(self, poolID, inMember):
        pass

    def getPoolMember(self, poolID, memberID):
        pass

    def updatePoolMember(self, poolID, memberID, inMember):
        pass

    def deletePoolMember(self, poolID, memberID):
        pass