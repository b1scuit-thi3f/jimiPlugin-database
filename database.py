from core import plugin, model

class _database(plugin._plugin):
    version = 0.1

    def install(self):
        # Register models
        model.registerModel("databaseSearch","_databaseSearch","_action","plugins.database.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("databaseSearch","_databaseSearch","_action","plugins.database.models.action")
        return True
    