from plugins.database.includes import database
from core.models import action, webui
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

    class _properties(webui._properties):
        def generate(self,classObject):
            formData = []
            formData.append({"type" : "break", "start" : True, "schemaitem": "Database Options"})
            formData.append({"type" : "dropdown", "schemaitem" : "dbType", "dropdown" : classObject.dbType, "dropdown" : ["oracle","mssql"], "label" : "database type", "tooltip" : "The type of database (e.g. mysql, oracle)"})
            formData.append({"type" : "input", "schemaitem" : "host", "textbox" : classObject.host, "tooltip" : "The name of the host"})
            formData.append({"type" : "input", "schemaitem" : "username", "textbox" : classObject.username, "tooltip" : "The username for the database"})
            formData.append({"type" : "input", "schemaitem" : "password", "textbox" : classObject.password, "tooltip" : "The password for the database"})
            formData.append({"type" : "json-input", "schemaitem" : "connectionDetails", "textbox" : classObject.connectionDetails, "tooltip" : "Additional KVs for the db connection string"})
            formData.append({"type" : "input", "schemaitem" : "search", "textbox" : classObject.search, "label" : "query", "tooltip" : "The search query"})
            formData.append({"type" : "input", "schemaitem" : "timeout", "textbox" : classObject.timeout, "tooltip" : "How long to attempt connecting before timing out. Default 30s"})
            formData.append({"type" : "input", "schemaitem" : "limit", "textbox" : classObject.limit, "tooltip" : "The number of results to return. 0 returns all"})
            formData.append({"type" : "checkbox", "schemaitem" : "count", "checked" : classObject.count, "tooltip" : "Return a count of the results, not the results themselves"})
            formData.append({"type" : "break", "start" : False, "schemaitem": "Database Options"})
            formData.append({"type" : "break", "start" : True, "schemaitem": "Core Options"})
            formData.append({"type" : "input", "schemaitem" : "_id", "textbox" : classObject._id})
            formData.append({"type" : "input", "schemaitem" : "name", "textbox" : classObject.name})
            formData.append({"type" : "checkbox", "schemaitem" : "enabled", "checked" : classObject.enabled})
            formData.append({"type" : "json-input", "schemaitem" : "varDefinitions", "textbox" : classObject.varDefinitions})
            formData.append({"type" : "input", "schemaitem" : "logicString", "textbox" : classObject.logicString})
            formData.append({"type" : "checkbox", "schemaitem" : "log", "checked" : classObject.log})
            formData.append({"type" : "input", "schemaitem" : "comment", "textbox" : classObject.comment})
            return formData

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