from plugins.database.includes import database
from core.models import action
from core import helpers, auth, db

class _databaseSearch(action._action):
    host = str()
    username = str()
    password = str()
    connectionDetails = dict()
    dbType = str()
    timeout = int()
    search = str()
    limit = int()
    count = bool()

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
        
        actionResult["result"] = False
        actionResult["rc"] = 404
        actionResult["msg"] = "could not connect"

        dbControl = database.control(dbType,host,username,password,connectionDetails,timeout)
        if dbControl.isConnected():
            rc, results = dbControl.query(search,self.limit)
            if rc:
                if self.limit == 1:
                    if self.count:
                        actionResult["result"] = 1
                    else:
                        actionResult["result"] = results[0]
                else:
                    if self.count:
                        actionResult["result"] = len(results)
                    else:
                        actionResult["results"] = results
                actionResult["rc"] = 0
                actionResult["msg"] = "success"
            else:
                actionResult["msg"] = results

        return actionResult

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "password" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.password = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_databaseSearch, self).setAttribute(attr,value,sessionData=sessionData)