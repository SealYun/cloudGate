from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler
from api_factory import NetworkingProcessorFactory
import json


class NetworkingBaseHandler(HttpBaseHandler):
    def get_processor(self):
        token = self.request.headers["X-Auth-Token"]
        #print ("token:", token)
        factory = NetworkingProcessorFactory()
        return factory.getAliyunProcessor(token)

    def get(self):
        pass

class NetworksHandler(NetworkingBaseHandler):
    def get(self):
        print "[----------NetworksHandler GET----------]"

        shared = self.get_argument("shared", None)
        tenantID = self.get_argument("tenant_id", None)
        routerExternal = self.get_argument("router:external", None)
        #print "shared: ", shared, ", type: ", type(shared)
        #print "tenant_id: ", tenantID, ", type: ", type(tenantID)
        #print "router:external: ", routerExternal, ", type: ", type(routerExternal)

        processor = self.get_processor()
        networks = processor.getNetwotks(shared, tenantID, routerExternal)
        if networks is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "networks":[
                {
                    "status": network["status"],
                    "subnets": network["subnets"],
                    "name": network["name"],
                    "provider:physical_network": network["provider:physical_network"],
                    "admin_state_up": network["admin_state_up"],
                    "tenant_id": network["tenant_id"],
                    "provider:network_type": network["provider:network_type"],
                    "router:external": network["router:external"],
                    "mtu": network["mtu"],
                    "shared": network["shared"],
                    "id": network["id"],
                    "provider:segmentation_id": network["provider:segmentation_id"],
                }
                for network in networks
            ]
        }

        self.send_json(resp)

    #maybe bulk
    def post(self):
        print "[----------NetworksHandler POST----------]"

        processor = self.get_processor()

        #print self.request.body
        body = json.loads(self.request.body)
        if "network" in body.keys():
            print "create network"
            inNetwork = body["network"]
            outNetwork = processor.createNetwork(inNetwork)
            if outNetwork is None:
                self.set_status(400)
                return
            else:
                self.set_status(201)
            resp = {
                "network":{
                            "status": outNetwork["status"],
                            "subnets": outNetwork["subnets"],
                            "name": outNetwork["name"],
                            "admin_state_up": outNetwork["admin_state_up"],
                            "tenant_id": outNetwork["tenant_id"],
                            "router:external": outNetwork["router:external"],
                            "mtu": outNetwork["mtu"],
                            "shared": outNetwork["shared"],
                            "id": outNetwork["id"]
                        }
                    }
            self.send_json(resp)
            return
        else:
            print "create networks"
            inNetworks = []
            inNetworks.append(body["networks"])
            outNetworks = processor.createNetworks(inNetworks)
            if outNetworks is None:
                self.set_status(400)
                return
            else:
                self.set_status(201)
            resp = {
                "networks":[
                    {
                        "status": network["status"],
                        "subnets": network["subnets"],
                        "name": network["name"],
                        "provider:physical_network": network["provider:physical_network"],
                        "admin_state_up": network["admin_state_up"],
                        "tenant_id": network["tenant_id"],
                        "mtu": network["mtu"],
                        "shared": network["shared"],
                        "id": network["id"],
                        "provider:segmentation_id": network["provider:segmentation_id"],
                    }
                    for network in outNetworks
                ]
            }
            self.send_json(resp)
            return

class NetworksExtensionsHandler(NetworkingBaseHandler):
    def get(self):
        print "[----------NetworksExtensionsHandler GET----------]"

        processor = self.get_processor()
        extensions = processor.getAPIExtensions()
        resp = {
            "extensions":extensions
        }
        self.send_json(resp)

class NetworkHandler(NetworkingBaseHandler):
    def get(self, networkID):
        print "[----------NetworkHandler GET----------]"

        print "network id: ", networkID
        print "request body: ", self.request.body

        processor = self.get_processor()
        network = processor.getNetwork(networkID)
        if network is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "network":{
                "status": network["status"],
                "subnets": network["subnets"],
                "name": network["name"],
                "router:external": network["router:external"],
                "admin_state_up": network["admin_state_up"],
                "tenant_id": network["tenant_id"],
                "mtu": network["mtu"],
                "shared": network["shared"],
                "port_security_enabled":network["port_security_enabled"],
                "id": network["id"]
            }
        }

        self.send_json(resp)

    #add decorator fill network, if not exit set None
    def put(self, networkID):
        print "[----------NetworkHandler PUT----------]"

        inNetwork = json.loads(self.request.body)["network"]

        processor = self.get_processor()
        outNetwork = processor.updateNetwork(networkID, inNetwork)

        if outNetwork is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "network":{
                "status": outNetwork["status"],
                "subnets": outNetwork["subnets"],
                "name": outNetwork["name"],
                "provider:physical_network": outNetwork["provider:physical_network"],
                "admin_state_up": outNetwork["admin_state_up"],
                "tenant_id": outNetwork["tenant_id"],
                "provider:network_type": outNetwork["provider:network_type"],
                "router:external": outNetwork["router:external"],
                "mtu": outNetwork["mtu"],
                "shared": outNetwork["shared"],
                "port_security_enabled":outNetwork["port_security_enabled"],
                "id": outNetwork["id"],
                "provider:segmentation_id": outNetwork["provider:segmentation_id"]
            }

        }

        self.send_json(resp)

    def delete(self, networkID):
        print "[----------NetworkHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deleteNetwork(networkID):
            self.set_status(204)
            return
        else:
            self.set_status(404)
            return

class DHCPAgentsHandler(NetworkingBaseHandler):
    def get(self, network_id):
        print "[----------DHCPAgentsHandler GET----------]"

        processor = self.get_processor()
        agents = processor.getDHCPAgents(network_id)
        if agents is None:
            self.set_status(400)
            return
        else:
            self.set_status(200)

        resp = {
            "agents": agents
        }
        self.send_json(resp)

class SubnetsHandler(NetworkingBaseHandler):
    def get(self):
        print "[----------SubnetsHandler GET----------]"

        displayName = self.get_argument("display_name", None)
        networkID = self.get_argument("network_id", None)
        gatewayIP = self.get_argument("gateway_ip", None)
        ipVersion = self.get_argument("ip_version", None)
        cidr = self.get_argument("cidr", None)
        id = self.get_argument("id", None)
        enableDHCP = self.get_argument("enable_dhcp", None)
        ipv6RaMode = self.get_argument("ipv6_ra_mode", None)
        ipv6AddressMode = self.get_argument("ipv6_address_mode", None)

        processor = self.get_processor()
        subnets = processor.getSubsets(displayName, networkID, gatewayIP, ipVersion, cidr, id, enableDHCP, ipv6RaMode, ipv6AddressMode)

        if subnets is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "subnets":[
                {
                    "name": s["name"],
                    "enable_dhcp": s["enable_dhcp"],
                    "network_id": s["network_id"],
                    "tenant_id": s["tenant_id"],
                    "dns_nameservers": s["dns_nameservers"],
                    "allocation_pools": s["allocation_pools"],
                    "host_routes": s["host_routes"],
                    "ip_version": s["ip_version"],
                    "gateway_ip": s["gateway_ip"],
                    "cidr": s["cidr"],
                    "id": s["id"]
                }
                for s in subnets
            ]
        }

        self.send_json(resp)

    #support bulk create subnet
    def post(self):
        print "[----------SubnetsHandler POST----------]"

        processor = self.get_processor()

        #print self.request.body
        body = json.loads(self.request.body)
        if "subnet" in body.keys():
            print "create subnet"
            inSubnet = body["subnet"]
            outSubnet = processor.createSubnet(inSubnet)
            if outSubnet is None:
                self.set_status(401)
                return
            else:
                self.set_status(200)
            resp = {
                "subnet":{
                    "name": outSubnet["name"],
                    "enable_dhcp": outSubnet["enable_dhcp"],
                    "network_id": outSubnet["network_id"],
                    "tenant_id": outSubnet["tenant_id"],
                    "dns_nameservers": outSubnet["dns_nameservers"],
                    "allocation_pools": outSubnet["allocation_pools"],
                    "host_routes": outSubnet["host_routes"],
                    "ip_version": outSubnet["ip_version"],
                    "gateway_ip": outSubnet["gateway_ip"],
                    "cidr": outSubnet["cidr"],
                    "id": outSubnet["id"]
                }
            }
            self.send_json(resp)
            return
        else:
            print "create subnets"
            inSubnets = []
            inSubnets.append(body["subnets"])
            outSubnets = processor.createSubnets(inSubnets)
            if outSubnets is None:
                self.set_status(401)
                return
            else:
                self.set_status(200)
            resp = {
                "subnets":[
                    {
                        "name": outSubnet["name"],
                        "enable_dhcp": outSubnet["enable_dhcp"],
                        "network_id": outSubnet["network_id"],
                        "tenant_id": outSubnet["tenant_id"],
                        "dns_nameservers": outSubnet["dns_nameservers"],
                        "allocation_pools": outSubnet["allocation_pools"],
                        "host_routes": outSubnet["host_routes"],
                        "ip_version": outSubnet["ip_version"],
                        "gateway_ip": outSubnet["gateway_ip"],
                        "cidr": outSubnet["cidr"],
                        "id": outSubnet["id"]
                    }
                    for outSubnet in outSubnets
                ]
            }
            self.send_json(resp)
            return

class SubnetHandler(NetworkingBaseHandler):
    def get(self, subnetID):
        print "[----------SubnetsHandler GET----------]"

        processor = self.get_processor()
        subset = processor.getSubnet(subnetID)

        if subset is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "subnet":{
                    "name": subset["name"],
                    "enable_dhcp": subset["enable_dhcp"],
                    "network_id": subset["network_id"],
                    "tenant_id": subset["tenant_id"],
                    "dns_nameservers": subset["dns_nameservers"],
                    "allocation_pools": subset["allocation_pools"],
                    "host_routes": subset["host_routes"],
                    "ip_version": subset["ip_version"],
                    "gateway_ip": subset["gateway_ip"],
                    "cidr": subset["cidr"],
                    "id": subset["id"]
                }
        }

        self.send_json(resp)

    def put(self, subnetID):
        print "[----------SubnetsHandler PUT----------]"

        inSubnet = json.loads(self.request.body)["subnet"]

        processor = self.get_processor()
        outSubnet = processor.updateSubnet(subnetID, inSubnet)

        if outSubnet is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)

        resp = {
            "subnet":{
                "name": outSubnet["name"],
                "enable_dhcp": outSubnet["enable_dhcp"],
                "network_id": outSubnet["network_id"],
                "tenant_id": outSubnet["tenant_id"],
                "dns_nameservers": outSubnet["dns_nameservers"],
                "allocation_pools": outSubnet["allocation_pools"],
                "host_routes": outSubnet["host_routes"],
                "ip_version": outSubnet["ip_version"],
                "gateway_ip": outSubnet["gateway_ip"],
                "cidr": outSubnet["cidr"],
                "id": outSubnet["id"]
            }
        }

        self.send_json(resp)

    def delete(self, subnetID):
        print "[----------SubnetsHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deleteSubnet(subnetID):
            self.set_status(200)
            return
        else:
            self.set_status(400)
            return

class PortsHandler(NetworkingBaseHandler):
    def get(self):
        status = self.get_argument("status", None)
        displayName = self.get_argument("display_name", None)
        adminState = self.get_argument("admin_state", None)
        networkID = self.get_argument("network_id", None)
        tenantID = self.get_argument("tenant_id", None)
        deviceOwner = self.get_argument("device_owner", None)
        macAddress = self.get_argument("mac_address", None)
        portID = self.get_argument("port_id", None)
        securityGroups = self.get_argument("security_groups", None)
        deviceID = self.get_argument("device_id", None)

        processor = self.get_processor()
        ports = processor.getPorts(status, displayName, adminState, networkID, tenantID, deviceOwner, macAddress, portID, securityGroups, deviceID)
        if ports is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "ports":[
                {
                    "status": p["status"],
                    "name": p["name"],
                    "allowed_address_pairs": p["allowed_address_pairs"],
                    "admin_state_up": p["admin_state_up"],
                    "network_id": p["network_id"],
                    "tenant_id": p["tenant_id"],
                    "extra_dhcp_opts": p["extra_dhcp_opts"],
                    "device_owner": p["device_owner"],
                    "mac_address": p["mac_address"],
                    "fixed_ips": p["fixed_ips"],
                    "id": p["id"],
                    "security_groups": p["security_groups"],
                    "device_id": p["device_id"]
                }
                for p in ports
            ]
        }

        self.send_json(resp)

    def post(self):
        print "[----------PortsHandler POST----------]"

        processor = self.get_processor()

        #print self.request.body
        body = json.loads(self.request.body)
        if "port" in body.keys():
            print "create port"
            inPort = body["port"]
            outPort = processor.createPort(inPort)
            if outPort is None:
                self.set_status(500)
                return
            else:
                self.set_status(200)
            resp = {
                "port" :{
                    "status": outPort["status"],
                    "name": outPort["name"],
                    "allowed_address_pairs": outPort["allowed_address_pairs"],
                    "admin_state_up": outPort["admin_state_up"],
                    "network_id": outPort["network_id"],
                    "tenant_id": outPort["tenant_id"],
                    "extra_dhcp_opts": outPort["extra_dhcp_opts"],
                    "device_owner": outPort["device_owner"],
                    "mac_address": outPort["mac_address"],
                    "fixed_ips": outPort["fixed_ips"],
                    "id": outPort["id"],
                    "security_groups": outPort["security_groups"],
                    "device_id": outPort["device_id"]
                }
            }
            self.send_json(resp)
            return
        else:
            print "create ports"
            inPorts = []
            inPorts.append(body["ports"])
            outPorts = processor.createPorts(inPorts)
            if outPorts is None:
                self.set_status(401)
                return
            else:
                self.set_status(200)
            resp = {
                "ports":[
                    {
                        "status": outPort["status"],
                        "name": outPort["name"],
                        "allowed_address_pairs": outPort["allowed_address_pairs"],
                        "admin_state_up": outPort["admin_state_up"],
                        "network_id": outPort["network_id"],
                        "tenant_id": outPort["tenant_id"],
                        "extra_dhcp_opts": outPort["extra_dhcp_opts"],
                        "device_owner": outPort["device_owner"],
                        "mac_address": outPort["mac_address"],
                        "fixed_ips": outPort["fixed_ips"],
                        "id": outPort["id"],
                        "security_groups": outPort["security_groups"],
                        "device_id": outPort["device_id"]
                    }
                    for outPort in outPorts
                ]
            }
            self.send_json(resp)
            return

class PortHandler(NetworkingBaseHandler):
    def get(self, portID):
        print "[----------PortHandler GET----------]"

        processor = self.get_processor()
        port = processor.getPort(portID)

        if port is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "port":{
                "status": port["status"],
                "name": port["name"],
                "allowed_address_pairs": port["allowed_address_pairs"],
                "admin_state_up": port["admin_state_up"],
                "network_id": port["network_id"],
                "tenant_id": port["tenant_id"],
                "extra_dhcp_opts": port["extra_dhcp_opts"],
                "device_owner": port["device_owner"],
                "mac_address": port["mac_address"],
                "fixed_ips": port["fixed_ips"],
                "id": port["id"],
                "security_groups": port["security_groups"],
                "device_id": port["device_id"]
                }
        }

        self.send_json(resp)

    def put(self, portID):
        print "[----------PortHandler PUT----------]"

        inPort = json.loads(self.request.body)["port"]

        processor = self.get_processor()
        outPort = processor.updatePort(portID, inPort)

        if outPort is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "port":{
                "status": outPort["status"],
                "binding:host_id":outPort["binding:host_id"],
                "allowed_address_pairs": outPort["allowed_address_pairs"],
                "extra_dhcp_opts": outPort["extra_dhcp_opts"],
                "device_owner": outPort["device_owner"],
                "binding:profile":outPort["binding:profile"],
                "fixed_ips": outPort["fixed_ips"],
                "id": outPort["id"],
                "security_groups": outPort["security_groups"],
                "device_id": outPort["device_id"],
                "name": outPort["name"],
                "admin_state_up": outPort["admin_state_up"],
                "network_id": outPort["network_id"],
                "tenant_id": outPort["tenant_id"],
                "binding:vif_details": outPort["binding:vif_details"],
                "binding:vnic_type": outPort["binding:vnic_type"],
                "binding:vif_type": outPort["binding:vif_type"],
                "mac_address": outPort["mac_address"],
            }
        }

        self.send_json(resp)

    def delete(self, portID):
        print "[----------PortHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deletePort(portID):
            self.set_status(200)
            return
        else:
            self.set_status(400)
            return

class LoadbalancersHandler(NetworkingBaseHandler):
    def get(self):
        print "[----------LoadbalancersHandler GET----------]"

        processor = self.get_processor()
        loadbalancers = processor.getLoadBalancers()
        if loadbalancers is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "loadbalancers":[
                {
                    "description": lb["description"],
                    "admin_state_up": lb["admin_state_up"],
                    "tenant_id": lb["tenant_id"],
                    "provisioning_status": lb["provisioning_status"],
                    "listeners": lb["listeners"],
                    "vip_address": lb["vip_address"],
                    "vip_subnet_id": lb["vip_subnet_id"],
                    "id": lb["id"],
                    "operating_status": lb["operating_status"],
                    "name": lb["name"]
                }
                for lb in loadbalancers
            ]
        }

        self.send_json(resp)

    def post(self):
        print "[----------LoadbalancersHandler POST----------]"

        inLoadbalancer = json.loads(self.request.body)["loadbalancer"]

        processor = self.get_processor()
        outLoadbalancer = processor.createLoadBalancer(inLoadbalancer)
        if outLoadbalancer is None:
            self.set_status(500)
            return
        else:
            self.set_status(201)

        resp = {
            "loadbalancer":{
                "description": outLoadbalancer["description"],
                "admin_state_up": outLoadbalancer["admin_state_up"],
                "tenant_id": outLoadbalancer["tenant_id"],
                "provisioning_status": outLoadbalancer["provisioning_status"],
                "listeners": outLoadbalancer["listeners"],
                "vip_address": outLoadbalancer["vip_address"],
                "vip_subnet_id": outLoadbalancer["vip_subnet_id"],
                "id": outLoadbalancer["id"],
                "operating_status": outLoadbalancer["operating_status"],
                "name": outLoadbalancer["name"],
                "provider" : outLoadbalancer["provider"]
            }
        }

        self.send_json(resp)

class LoadbalancerHandler(NetworkingBaseHandler):
    def get(self, lbID):
        print "[----------LoadbalancerHandler GET----------]"

        processor = self.get_processor()
        loadbalancer = processor.getLoadBalancer(lbID)
        if loadbalancer is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "loadbalancer": {
                "description": loadbalancer["description"],
                "admin_state_up": loadbalancer["admin_state_up"],
                "tenant_id": loadbalancer["tenant_id"],
                "provisioning_status": loadbalancer["provisioning_status"],
                "listeners": loadbalancer["listeners"],
                "vip_address": loadbalancer["vip_address"],
                "vip_subnet_id": loadbalancer["vip_subnet_id"],
                "id": loadbalancer["id"],
                "operating_status": loadbalancer["operating_status"],
                "name": loadbalancer["name"]
            }
        }

        self.send_json(resp)

    def put(self, lbID):
        print "[----------LoadbalancerHandler PUT----------]"

        inLoadBalancer = json.loads(self.request.body)["loadbalancer"]
        processor = self.get_processor()
        outLoadBalancer = processor.updateLoadBalancer(lbID, inLoadBalancer)
        if outLoadBalancer is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "loadbalancer": {
                "description": outLoadBalancer["description"],
                "admin_state_up": outLoadBalancer["admin_state_up"],
                "tenant_id": outLoadBalancer["tenant_id"],
                "provisioning_status": outLoadBalancer["provisioning_status"],
                "listeners": outLoadBalancer["listeners"],
                "vip_address": outLoadBalancer["vip_address"],
                "vip_subnet_id": outLoadBalancer["vip_subnet_id"],
                "id": outLoadBalancer["id"],
                "operating_status": outLoadBalancer["operating_status"],
                "name": outLoadBalancer["name"]
            }
        }

        self.send_json(resp)

    def delete(self, lbID):
        print "[----------LoadbalancerHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deleteLoadBalancer(lbID):
            self.set_status(204)
            return
        else:
            self.set_status(500)
            return

class LoadbalancerStatusesHandler(NetworkingBaseHandler):
    def get(self, lbID):
        print "[----------LoadbalancerStatusesHandler GET----------]"

        processor = self.get_processor()
        loadBalancerStatuses = processor.getLoadBalancerStatuses(lbID)
        if loadBalancerStatuses is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "statuses": {
                "loadbalancer": loadBalancerStatuses
            }
        }

        """
        loadbalancer
            |___listener1
            |       |_____pool1
            |       |       |_____member1
            |       |       |_____member2
            |       |______pool2
            |___listener2
        """
        self.send_json(resp)

class LbaasListenersHandler(NetworkingBaseHandler):
    def get(self):
        print "[----------LbaasListenersHandler GET----------]"

        processor = self.get_processor()
        listeners = processor.getListeners()
        if listeners is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "listeners":listeners
        }

        self.send_json(resp)

    def post(self):
        print "[----------LbaasListenersHandler POST----------]"

        inListener = json.loads(self.request.body)["listener"]

        processor = self.get_processor()
        outListener = processor.createListener(inListener)
        if outListener is None:
            self.set_status(500)
            return
        else:
            self.set_status(201)

        resp = {
            "listener":outListener
        }

        self.send_json(resp)

class LbaasListenerHandler(NetworkingBaseHandler):
    def get(self, listenerID):
        print "[----------LbaasListenerHandler GET----------]"

        processor = self.get_processor()
        listener = processor.getListener(listenerID)
        if listener is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "listener":listener
        }

        self.send_json(resp)

    def put(self, listenerID):
        print "[----------LbaasListenerHandler PUT----------]"

        inListener = json.loads(self.request.body)["listener"]

        processor = self.get_processor()
        outListener = processor.updateListener(listenerID, inListener)
        if outListener is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "listener":outListener
        }

        self.send_json(resp)

    def delete(self, listenerID):
        print "[----------LbaasListenerHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deleteListener(listenerID):
            self.set_status(204)
            return
        else:
            self.set_status(500)
            return

class LbaasPoolsHandler(NetworkingBaseHandler):
    def get(self):
        print "[----------LbaasPoolsHandler GET----------]"

        processor = self.get_processor()
        pools = processor.getPools()

        if pools is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "pools":pools
        }

        self.send_json(resp)

    def post(self):
        print "[----------LbaasPoolsHandler POST----------]"

        inPool = json.loads(self.request.body)["pool"]

        processor = self.get_processor()
        outPool = processor.createPool(inPool)
        if outPool is None:
            self.set_status(500)
            return
        else:
            self.set_status(201)

        resp = {
            "pool":outPool
        }

        self.send_json(resp)

class LbaasPoolHandler(NetworkingBaseHandler):
    def get(self, poolID):
        print "[----------LbaasPoolHandler GET----------]"

        processor = self.get_processor()
        pool = processor.getPool(poolID)
        if pool is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "pool":pool
        }

        self.send_json(resp)

    def put(self, poolID):
        print "[----------LbaasPoolHandler POST----------]"

        inPool = json.loads(self.request.body)["pool"]

        processor = self.get_processor()
        outPool = processor.updateListener(poolID, inPool)
        if outPool is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "pool":outPool
        }

        self.send_json(resp)

    def delete(self, poolID):
        print "[----------LbaasPoolHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deletePool(poolID):
            self.set_status(204)
            return
        else:
            self.set_status(500)
            return

class LbaasPoolMembersHandler(NetworkingBaseHandler):
    def get(self, poolID):
        print "[----------LbaasPoolMembersHandler GET----------]"

        processor = self.get_processor()
        members = processor.getPoolMembers(poolID)

        if members is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "members":members
        }

        self.send_json(resp)

    def post(self, poolID):
        print "[----------LbaasPoolMembersHandler POST----------]"

        inMember = json.loads(self.request.body)["member"]

        processor = self.get_processor()
        outMember = processor.createPoolMember(poolID, inMember)
        if outMember is None:
            self.set_status(500)
            return
        else:
            self.set_status(201)

        resp = {
            "member":outMember
        }

        self.send_json(resp)

class LbaasPoolMemberHandler(NetworkingBaseHandler):
    def get(self, poolID, memberID):
        print "[----------LbaasPoolMemberHandler GET----------]"

        processor = self.get_processor()
        member = processor.getPoolMember(poolID, memberID)
        if member is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "member":member
        }

        self.send_json(resp)


    def put(self, poolID, memberID):
        print "[----------LbaasPoolMemberHandler PUT----------]"

        inMember = json.loads(self.request.body)["member"]

        processor = self.get_processor()
        outMember = processor.updatePoolMember(poolID, memberID, inMember)
        if outMember is None:
            self.set_status(500)
            return
        else:
            self.set_status(200)

        resp = {
            "member":outMember
        }

        self.send_json(resp)

    def delete(self, poolID, memberID):
        print "[----------LbaasPoolMemberHandler DELETE----------]"

        processor = self.get_processor()

        if processor.deletePoolMember(poolID, memberID):
            self.set_status(204)
            return
        else:
            self.set_status(500)
            return

class LbaasHealthMonitorsHandler(NetworkingBaseHandler):
    def post(self):
        print "[----------LbaasHealthMonitorsHandler POST----------]"
        #TODO

        health_moniter = json.loads(self.request.body)["health_moniter"]

        health_moniter = self.p.createLbaasHealthMonitor(health_moniter["admin_state_up"],
                health_moniter["delay"],
                health_moniter["expected_codes"],
                health_moniter["http_method"],
                health_moniter["max_retries"],
                health_moniter["pool_id"],
                health_moniter["timeout"],
                health_moniter["type"],
                health_moniter["url_path"])

        if health_moniter:
            self.set_status(201)
        else:
            self.set_status(400)
            return

        resp = {
            "health_moniter":{
                "admin_state_up": health_moniter.admin_state_up,
                "delay": health_moniter.delay,
                "expected_codes": health_moniter.expected_codes,
                "http_method": health_moniter.http_method,
                "id": health_moniter.id,
                "max_retries": health_moniter.max_retries,
                "pools": health_moniter.pools,
                "tenant_id": health_moniter.tenant_id,
                "timeout": health_moniter.timeout,
                "type": health_moniter.type,
                "url_path": health_moniter.url_path 
            }
        }

        self.send_json(resp)

class LbaasHealthMonitorHandler(NetworkingBaseHandler):
    def get(self, health_moniter_id):
        print "[----------LbaasHealthMonitorHandler GET----------]"
        #TODO

        health_moniter = self.p.queryLbaasHealthMonitor(health_moniter_id)

        if health_moniter:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "health_moniter":{
                "admin_state_up": health_moniter.admin_state_up,
                "delay": health_moniter.delay,
                "expected_codes": health_moniter.expected_codes,
                "http_method": health_moniter.http_method,
                "id": health_moniter.id,
                "max_retries": health_moniter.max_retries,
                "pools": health_moniter.pools,
                "tenant_id": health_moniter.tenant_id,
                "timeout": health_moniter.timeout,
                "type": health_moniter.type,
                "url_path": health_moniter.url_path 
            }
        }

        self.send_json(resp)

    def put(self, health_moniter_id):
        print "[----------LbaasHealthMonitorHandler PUT----------]"
        #TODO

        health_moniter = json.loads(self.request.body)["health_moniter"]

        health_moniter = self.p.updateLbaasHealthMoniter(health_moniter_id,
                health_moniter["admin_state_up"],
                health_moniter["delay"],
                health_moniter["expected_codes"],
                health_moniter["http_method"],
                health_moniter["max_retries"],
                health_moniter["timeout"],
                health_moniter["url_path"])

        if health_moniter:
            self.set_status(200)
        else:
            self.set_status(400)
            return

        resp = {
            "health_moniter":{
                "admin_state_up": health_moniter.admin_state_up,
                "delay": health_moniter.delay,
                "expected_codes": health_moniter.expected_codes,
                "http_method": health_moniter.http_method,
                "id": health_moniter.id,
                "max_retries": health_moniter.max_retries,
                "pools": health_moniter.pools,
                "tenant_id": health_moniter.tenant_id,
                "timeout": health_moniter.timeout,
                "type": health_moniter.type,
                "url_path": health_moniter.url_path 
            }
        }

        self.send_json(resp)

    def delete(self, health_moniter_id):
        print "[----------LbaasHealthMonitorHandler DELETE----------]"
        #TODO

        if self.p.deleteLbaasHealthMonitor(health_moniter_id):
            self.set_status(204)
        else:
            self.set_status(400)
