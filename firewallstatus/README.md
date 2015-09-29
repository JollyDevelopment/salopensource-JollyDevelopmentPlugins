# Firewall Status

This plugin polls for the current status of a MAC OSX firewall. It requires the custom Fact "mac_firewall_status" (found in the folder "facter_fact") to be deployed first.

## Installation 

This is based on an install of SAL on an Ubuntu 14.04 system. Instructions found here: https://github.com/salopensource/sal/blob/master/docs/Installation_on_Ubuntu_14.md

Note: The templates are expecting the folder path to be /sal_plugins_folder/jollydevelopment/file_name.html. If you are having "Page not found" type errors, check the templates and make sure the path they expect matches your environment.

Copy (or clone) the following files to your SAL plugins folder:
* firewallstatus/
* firewallstatus/firewallstatus.py
* firewallstatus/firewallstatus.yapsy-plugin
* firewallstatus/templates/
* firewallstatus/templates/traffic_lights_front.html
* firewallstatus/templates/traffic_lights_id.html

Set permissions for your files to be 755 saluser:salgroup


