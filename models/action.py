from plugins.database.includes import database
from core.models import action
from core import helpers, auth

class _databaseSearch(action._action):
    host = str()
    username = str()
    password = str()
    connectionDetails = dict()
    dbType = str()
    timeout = int()
    search = str()

    def run(self,data,persistentData,actionResult):
        import pyodbc
        host = helpers.evalString(self.host,{"data" : data})
        username = helpers.evalString(self.username,{"data" : data})
        connectionDetails = helpers.evalDict(self.connectionDetails,{"data" : data})
        dbType = helpers.evalString(self.dbType,{"data" : data})
        search = helpers.evalString(self.search,{"data" : data})
        password = auth.getPasswordFromENC(self.password)

        timeout = 30
        if self.timeout != 0:
            timeout=self.timeout

        dbControl = database.control(dbType,host,username,password,connectionDetails,timeout)
        dbControl.isConnected()

        actionResult["result"] = True
        actionResult["rc"] = 0
        actionResult["msg"] = "done"

        return actionResult

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "password" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.password = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_databaseSearch, self).setAttribute(attr,value,sessionData=sessionData)