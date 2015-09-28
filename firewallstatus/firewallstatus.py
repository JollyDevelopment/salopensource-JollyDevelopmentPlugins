#Imports

from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *

#Class
class MavCompatibility(IPlugin):
    
    #SAL sends at least two, possibly three pieces of info to the plugin
    #-"page" the page the plugin will be shown on ("front", "bu_dashboard", or "group_dashboard"
    #-"machines" the list of machines to pull information from/about
    #-"theid" the id of the Business Unit/Machine Group page
    def show_widget(self, page, machines=None, theid=None):

        if page == 'front':
            t = loader.get_template('xperteks/firewallstatus/templates/traffic_lights_front.html')
        
        if page == 'bu_dashboard':
            t = loader.get_template('xperteks/firewallstatus/templates/traffic_lights_id.html')
        
        if page == 'group_dashboard':
            t = loader.get_template('xperteks/firewallstatus/templates/traffic_lights_id.html')
            
        #this looks at the list of machines, sellects the machines that have a "mac_firewall_status" fact (from the custom 
        #facter fact "mac_firewall_status
        #then checks for the ones in that list that have the contents "Firewall is enabled." and counts them
        #then it assigns that count to the "firewall_status" variable
        firewall_status = machines.filter(fact__fact_name='mac_firewall_status', fact__fact_data__contains='Firewall is enabled.').count()


        #This is the data sent from this code to be displayed on the page. 
        #title = the title of the plugin
        #firewallstatus = the number displayed in the button in the plugin
        #page and theid are used the same as was passed to this plugin from SAL, so it knows where to display the plugin
        c = Context({
            'title': 'Firewall Status',
            'firewallstatus': firewall_status,
            'page': page,
            'theid': theid
        })
        return t.render(c), 3

    #This next part will allow SAL to build a new page and display the list of the machines that match our criteria
    def filter_machines(self, machines, data):
        if data == 'firewallstatus':
            machines = machines.filter(fact__fact_name='mac_firewall_status', fact__fact_data__contains='Firewall is enabled.')
            title = 'Macs with enabled Firewalls'
        else:
            machines = None
            titles = None
 
        return machines, title



