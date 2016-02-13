# -*- encoding: utf-8 -*-
from cloudGate.httpbase import HttpBaseHandler
from cloudGate.config import *

import sys
import json

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class IdentityBaseHandler(HttpBaseHandler):
    def get(self):
        resp = {
            "versions":{
                "values":[
                    {
                        "id": "v3",
                        "links": [
                            {
                                "href": "http://" + HOST + ":" + PORT + "/v3/",
                                "rel": "self"
                            }
                        ],
                        "media-types": [
                            {
                                "base": "application/json",
                            }
                        ],
                        "status": "stable",
                        "updated": "2015-04-17T00:00:00Z"
                    }
                ]
            }
        }

        self.send_json(resp)

class TokensHandler(IdentityBaseHandler):
    def post(self):
        pass

class AuthTokensHandler(IdentityBaseHandler):
    def post(self):
        print self.request.body

        auth = json.loads(self.request.body)

        if "auth" not in auth:
            return

        if "token" in auth["auth"]["identity"]:
            user = self.parse_token(auth["auth"]["identity"]["token"]["id"])
        else:
            user = auth["auth"]["identity"]["password"]["user"]

        if user["name"] == IDENTITY["aliyun"]["user_name"] and \
                user["password"] == IDENTITY["aliyun"]["passwd"]:
            self.add_header('X-Auth-Token', self.create_tocken(user["name"] + user["password"]))
            self.add_header('X-Subject-Token', self.create_tocken(user["name"] + user["password"]))
        else:
            self.set_status(403)
            return

        resp = {
            "token": {
                "methods": [
                    "password"
                ],
                "expires_at": "2915-11-06T15:32:17.893769Z",
                "extras": {},
                "user": {
                    "domain": {
                        "id": "default",
                        "name": "Default"
                    },
                    "id": "423f19a4ac1e4f48bbb4180756e6eb6c",
                    "name": user["name"]
                },
                "audit_ids": [
                    "ZzZwkUflQfygX7pdYDBCQQ"
                ],
                "issued_at": "2015-11-06T14:32:17.893797Z"
            }
        }

        self.send_json(resp)

class UsersHandler(IdentityBaseHandler):
    def get(self):
        domian_id = self.get_argument("domain_id", None)
        name = self.get_argument("name", None)
        enabled = self.get_argument("enabled", None)

        users = self.p.queryUsers(domian_id, name, enabled)

        resp = {
            "links": {
                "next":null,
                "previous":null,
                "self":"http://"
            },
            "users":[
                {
                    "domian_id":domian_id,
                    "email":u.email,
                    "enabled":u.enabled,
                    "id":u.id,
                    "links":{
                        "self":"http://",
                    },
                    "name":u.name,
                } 
                for u in users
            ]
        }

        self.send_json(resp)

    def post(self):
        user = json.loads(self.request.body)["user"]

        user = self.p.createUser(user["default_project_id"], 
                user["description"], 
                user["domian_id"], 
                user["email"], 
                user["enabled"], 
                user["name"], 
                user["password"])

        resp = {
            "user":{
                "default_project_id":user.default_project_id,
                "description":user.description,
                "domian_id":user.domian_id,
                "email":user.email,
                "enabled":user.enabled,
                "id":user.id,
                "links":{
                    "self":"https://"
                },
                "name":user.name
            }
        }

        self.send_json(resp)

class UserHandler(IdentityBaseHandler):
    def get(self, user_id):
        user = self.p.queryUserById(user_id)

        resp = {
            "user":{
                "default_project_id":user.default_project_id,
                "description":user.description,
                "domian_id":user.domian_id,
                "email":user.email,
                "enabled":user.enabled,
                "id":user.id,
                "links":{
                    "self":"https://"
                },
                "name":user.name
            }
        }

        self.send_json(resp)


    def patch(self, user_id):
        user = json.loads(self.request.body)["user"]

        user = self.p.updateUser(user_id, 
                user["default_project_id"],
                user["description"],
                user["email"],
                user["enabled"])

        resp = {
            "user":{
                "default_project_id":user.default_project_id,
                "description":user.description,
                "domian_id":user.domian_id,
                "email":user.email,
                "enabled":user.enabled,
                "id":user.id,
                "links":{
                    "self":"https://"
                },
                "name":user.name
            }
        }

        self.send_json(resp)

    def delete(self, user_id):
        self.p.deleteUserById(user_id)

class UserPasswordHandler(IdentityBaseHandler):
    def post(self, user_id):
        user = json.loads(self.request.body)["user"]
        self.p.changeUserPasswd(user_id, user["password"],
                user["original_password"])

class UserGroupsHandler(IdentityBaseHandler):
    def get(self, user_id):
        groups = self.p.queryUserGroups(user_id)

        resp = {
            "groups":[
                {
                    "description":g.description,
                    "domian_id":g.domian_id,
                    "id":g.id,
                    "links":{
                        "self":"http://"
                    },
                    "name":g.name
                }
                for g in groups
            ],
            "links":{
                "self":"http://",
                "previous":null,
                "next":null
            }
        }

        self.send_json(resp)

class UserProjectsHandler(IdentityBaseHandler):
    def get(self, user_id):
        resp = {
            "projects": [
                {
                    "description": "description of this project",
                    "domain_id": "161718",
                    "enabled": True,
                    "id": "456788",
                    "parent_id": "212223",
                    "links": {
                        "self": "http://identity:35357/v3/projects/456788"
                    },
                    "name": "a project name"
                },
                {
                    "description": "description of this project",
                    "domain_id": "161718",
                    "enabled": True,
                    "id": "456789",
                    "parent_id": "212223",
                    "links": {
                        "self": "http://identity:35357/v3/projects/456789"
                    },
                    "name": "another domain"
                }
            ], 
            "links": {
                "self": "http://identity:35357/v3/users/313233/projects",
                "previous": None,
                "next": None 
            }
        }

        self.send_json(resp)

class RolesHandler(IdentityBaseHandler):
    def get(self):
        name = self.get_argument("name", None)

        roles = self.p.queryRolesByName(name)

        resp = {
            "links": {
                "next":null,
                "previous":null,
                "self":"http://"
            },
            "roles":[
                {
                    "id":r.id,
                    "links":{
                        "self":"http://"
                    },
                    "name":r.name
                }
                for r in roles
            ]
        }

        self.send_json(resp)

    def post(self):
        role = json.loads(self.request.body)["role"]

        role = self.p.createRole(role["name"])

        resp = {
            "role": {
                "id":role.id,
                "links":{
                    "self":"http://",
                },
                "name":role.name
            }
        }

        self.send_json(resp)

class RoleHandler(IdentityBaseHandler):
    def get(self, role_id):
        role = self.p.queryRoleByid(role_id)

        resp = {
            "role": {
                "id":role.id,
                "links":{
                    "self":"http://",
                },
                "name":role.name
            }
        }

        self.send_json(resp)

    def patch(self, role_id):
        name = json.loads(self.request.body)["role"]["name"]
        role = self.p.updateRole(role_id, name)

        resp = {
            "role": {
                "id":role.id,
                "links":{
                    "self":"http://",
                },
                "name":role.name
            }
        }

        self.send_json(resp)

    def delete(self, role_id):
        self.p.deleteRoleById(role_id)

class GroupsHandler(IdentityBaseHandler):
    def get(self):
        domian_id = self.get_argument("domian_id", None)
        name = self.get_argument("name", None)

        groups = self.p.queryGroups(domian_id, name)

        resp = {
            "links": {
                "next":null,
                "previous":null,
                "self":"http://"
            },
            "groups":[
                {
                    "domian_id":g.domian_id,
                    "description":g.description,
                    "id":g.id,
                    "links":{
                        "self":"http://"
                    },
                    "name":g.name
                }
                for g in groups
            ]
        }

        self.send_json(resp)

    def post(self):
        group = json.loads(self.request.body)["group"]

        group = self.p.createGroup(group["description"],
                group["domian_id"],
                group["name"])

        resp = {
            "group": {
                "domian_id":group.domian_id,
                "description":group.description,
                "id":group.id,
                "links":{
                    "self":"http://"
                },
                "name":group.name
            }
        }

        self.send_json(resp)

class GroupHandler(IdentityBaseHandler):
    def get(self, group_id):
        group = self.p.queryGroup(group_id)

        resp = {
            "group": {
                "domian_id":group.domian_id,
                "description":group.description,
                "id":group.id,
                "links":{
                    "self":"http://"
                },
                "name":group.name
            }
        }

        self.send_json(resp)

    def patch(self, group_id):
        group = json.loads(self.request.body)["group"]

        group = self.p.updateGroup(group_id, 
                group["description"],
                group["name"])

        resp = {
            "group": {
                "domian_id":group.domian_id,
                "description":group.description,
                "id":group.id,
                "links":{
                    "self":"http://"
                },
                "name":group.name
            }
        }

        self.send_json(resp)

    def delete(self, group_id):
        self.p.deleteGroupById(group_id)

class GroupUsersHandler(IdentityBaseHandler):
    def get(self, group_id):
        domian_id = self.get_arguments("domian_id",None)
        description = self.get_arguments("description",None)
        name = self.get_arguments("name",None)
        enabled = self.get_arguments("enabled",None)

        users = self.p.queryUsersInGroup(group_id, domian_id, description, name, enabled)

        resp = {
            "users":[
                {
                    "name":u.name,
                    "links":{
                        "self":"http://"
                    },
                    "domian_id":u.domian_id,
                    "enabled":u.enabled,
                    "email":u.email,
                    "id":u.id
                }
                for u in users
            ],
            "links":{
                "self":"http://",
                "previous":null,
                "next":null
            }
        }

        self.send_json(resp)

class GroupUserHandler(IdentityBaseHandler):
    def put(self, group_id, user_id):
        self.p.addUserInGroup(group_id, user_id)

    def head(self, group_id, user_id):
        res = self.p.checkUserBelongsToGroup(group_id, user_id)
        if res:
            #HTTP 204
            pass
        else:
            pass

    def delete(self, group_id, user_id):
        self.p.deleteUserFromGroup(group_id, user_id)

class PoliciesHandler(IdentityBaseHandler):
    def get(self):
        type = self.get_argument("type", None)

        policies = self.p.queryPolicies(type)

        resp = {
            "links": {
                "next":null,
                "previous":null,
                "self":"http://"
            },
            "policies":[
                {
                    "blob":json.loads(p.blob),
                    "id":p.id,
                    "links":{
                        "self":"http://"
                    },
                    "project_id":p.project_id,
                    "type":p.type,
                    "user_id":p.user_id
                }
                for p in policies
            ]
        }

        self.send_json(resp)

    def post(self):
        policy = json.loads(self.request.body)["policy"]

        policy = self.p.createPolicy(policy["blob"],
                policy["project_id"],
                policy["type"],
                policy["user_id"])

        resp = {
            "policy":{
                "blob":json.loads(policy.blob),
                "project_id":policy.project_id,
                "type":policy.type,
                "user_id":policy.user_id
            }
        }

        self.send_json(resp)

class PolicyHandler(IdentityBaseHandler):
    def get(self, policy_id):
        policy = self.p.queryPolicie(policy_id)

        resp = {
            "policy":{
                "blob":json.loads(policy.blob),
                "id":policy.id,
                "project_id":policy.project_id,
                "links":{
                    "self":"http://"
                },
                "type":policy.type,
                "user_id":policy.user_id
            }
        }

        self.send_json(resp)

    def patch(self, policy_id):
        policy = json.loads(self.request.body)["policy"]

        policy = self.p.updatePolicy(policy_id,
                policy["blob"],
                policy["project_id"],
                policy["type"],
                policy["user_id"])

        resp = {
            "policy":{
                "blob":json.loads(policy.blob),
                "id":policy.id,
                "project_id":policy.project_id,
                "links":{
                    "self":"http://"
                },
                "type":policy.type,
                "user_id":policy.user_id
            }
        }

        self.send_json(resp)

    def delete(self, policy_id):
        self.p.deletePolicy(policy_id)
