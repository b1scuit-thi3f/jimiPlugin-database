import pyodbc
from core import helpers, auth, settings

databaseSettings = settings.config["databasePlugin"]

class control():
    def __init__(self,dbType,host,username,password,connectionDetails,timeout):
        self.connection = False
        try:
            if dbType == "mssql":
                if "mssqlDriver" in databaseSettings and databaseSettings["mssqlDriver"] != "":
                    self.connection = pyodbc.connect("driver={0};server={1};uid={2};pwd={3};{4}".format(databaseSettings["mssqlDriver"],host,username,password,";".join(["{}={}".format(x,connectionDetails[x]) for x in connectionDetails])),timeout=timeout)
            if dbType == "oracle":
                if "oracleDriver" in databaseSettings and databaseSettings["oracleDriver"] != "":
                    self.connection = pyodbc.connect("drive={0};dbq={1};uid={2};pwd={3};{4}".format(databaseSettings["oracleDriver"],host,username,password,";".join(["{}={}".format(x,connectionDetails[x]) for x in connectionDetails])),timeout=timeout)
                    
        except Exception as e:
            print(e)

    def isConnected(self):
        if self.connection != False:
            return True
        return False

    def query(self,query):
        return (True, 0, "")