import minqlx
import requests
import os
import ast

class plugin_updater(minqlx.Plugin):

    def __init__(self):
        self.add_command("plugin_updater", self.cmd_update, 5)
        self.set_cvar_once("qlx_plugin_updater_auto", "")
        if self.get_cvar("qlx_plugin_updater_auto"):
            self.cmd_update()

    #lil helper function to send update messages just to admin
    def admin_msg(self, message):
        for p in self.players():
            if self.db.get_permission(p) == 5:
                p.tell(message)

    @minqlx.thread
    def cmd_update(self, player = None, msg = None, channel = None):
        try:
            enabled_plugins = self.get_cvar("qlx_plugins").replace("plugin_updater", "")
            plugin_status = dict()
            #Loop through plugins user has enabled in qlx_plugins cvar
            for plugin in enabled_plugins.split(','):
                plugin = plugin.strip();

                if plugin:
                    #check if plugin has plugin_updater_url variable set (this URL should have the plugin's raw .py)
                    plugin_updater_url = None

                    try: plugin_updater_url = self.plugins[plugin].plugin_updater_url
                    except: pass

                    if plugin_updater_url:
                        res = requests.get(plugin_updater_url)

                        if res.status_code == requests.codes.ok:
                            valid_python = True
                            #Check if returned text is valid python
                            try: ast.parse(res.text)
                            except: valid_python = False

                            if valid_python:
                                script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
                                abs_file_path = os.path.join(script_dir, "{}.py".format(plugin))

                                with open(abs_file_path,"r") as f:
                                    local_plugin_content = f.read()

                                if local_plugin_content == res.text:
                                    plugin_status[plugin] = "Current"
                                else: #If local plugin content is not current, replace plugin file with latest version
                                    with open(abs_file_path,"w") as f:
                                        f.write(res.text)
                                    plugin_status[plugin] = "Updated"
                                    minqlx.reload_plugin(plugin)
                            else:
                                plugin_status[plugin] = "Invalid python returned"
                        else: #If there was an error retrieving the file
                            plugin_status[plugin] = "Error code: {}".format(res.status_code)

            if plugin_status: #Return results of updater
                update_results = ""
                for plugin_name, update_status in plugin_status.items():
                    if update_status == "Current": status_color = "^6"
                    else:
                        if update_status == "Updated": status_color = "^2"
                        else: status_color = "^1"

                    update_results += "^3{}: {}{} - ".format(plugin_name, status_color, update_status)

                update_results = update_results[:-3] #Remove last hyphen/spaces
                #self.msg("^1Plugin Updater Results: " + update_results)
                self.admin_msg("^1Plugin Updater Results: " + update_results)
            else:
                self.admin_msg("^1Plugin Updater Results: ^1No eligible plugins found.")
                #self.msg("^1Plugin Updater Results: ^1No eligible plugins found.")

            return True

        except Exception as e:
            self.admin_msg("^1Plugin Updater failed with exception: ^6{}".format(e))
            return False