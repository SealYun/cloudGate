class IdentityProcessorBase():

    def queryUsers(self, domian_id, name, enabled):
        pass

    def queryRolesByName(self, name):
        pass

    def createUser(self, default_project_id, description, domian_id, email, 
            enabled, name, password):
        pass

    def queryUserById(self, user_id):
        pass

    def updateUser(self, user_name, default_project_id, description, email, enabled):
        pass

    def deleteUserById(self, user_name):
        pass

    def queryUserGroups(self, user_name):
        pass

    def createRole(self, name):
        pass

    def queryRoleByid(self, role_id):
        pass

    def deleteRoleById(self, role_id):
        pass

    def queryGroups(self, domian_id, name):
        pass

    def createGroup(self, description, domian_id, name):
        pass

    def updateGroup(self, group_id, description, name):
        pass

    def queryGroup(self, group_id):
        pass

    def deleteGroupById(self, group_id):
        pass

    def queryUsersInGroup(self, group_id, domain_id, description, name, enabled):
        pass

    def addUserInGroup(self, group_id, user_id):
        pass

    def checkUserBelongsToGroup(self, group_id, user_id):
        pass

    def deleteUserFromGroup(self, group_id, user_id):
        pass

    def queryPolicies(self, type_):
        pass

    def createPolicy(self, blob, project_id, type_, user_id):
        pass

    def queryPolicy(self, policy_id):
        pass

    def updatePolicy(self, policy_id, blob, project_id, type_, user_id):
        pass

    def deletePolicy(self, policy_id):
        pass


