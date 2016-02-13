#www.aliyun.com/product/ram
from cloudGate.modules.identity.process_base import *
from cloudGate.config import *
from aliyunsdkcore import client

from aliyunsdkram.request.v20150501 import ListUsersRequest
from aliyunsdkram.request.v20150501 import GetUserRequest
from aliyunsdkram.request.v20150501 import ListRolesRequest

import json

class AliyunIdentityProcessor(IdentityProcessorBase):
    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]

        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)

    def queryUsers(self, domian_id, name, enabled):
        request = ListUsersRequest.ListUsersRequest()
        request.set_accept_format('json')

        response = self.clt.do_action(request)

        print response

        resp = json.loads(response)

        users = []

        for u in resp["Users"]["User"]:
            r = GetUserRequest.GetUserRequest()
            r.set_UserName(u["UserName"])
            r.set_accept_format('json')
            user = json.loads(self.clt.do_action(r))

            users.append(user["User"])

        return users

    def queryRolesByName(self, name):
        request = ListRolesRequest.ListRolesRequest()
        request.set_accept_format('json')

        response = self.clt.do_action(request)

        print response

        resp = json.loads(response)

