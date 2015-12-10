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
            t = loader.get_template('jollydevelopment/firewallstatus/templates/traffic_lights_front.html')
        
        if page == 'bu_dashboard':
            t = loader.get_template('jollydevelopment/firewallstatus/templates/traffic_lights_id.html')
        
        if page == 'group_dashboard':
            t = loader.get_template('jollydevelopment/firewallstatus/templates/traffic_lights_id.html')
            
        #This checks to see if the machines list is populated, then
        #this looks at the list of machines, selects the machines that have a "mac_firewall_status" fact, from the custom 
        #facter fact "mac_firewall_status"
        #then checks for the ones in that list that have the contents "Firewall is enabled." and counts them
        #then it assigns that count to the "firewall_status" variable
        #if there are no machines it sets the variable to 0
        if machines:
		firewall_status_on = machines.filter(fact__fact_name='mac_firewall_status', fact__fact_data__contains='Firewall is enabled.').count()
	else:
		firewall_status_on = 0

	#This checks to see if the list of machines is populated, then
        #This looks at the list of machines, selects the machines that have a "mac_firewall_status" fact 
        #then it checks for the ones that have "disabled in the contents and counts them
	#then it assigns that count to the "firewall_Status_off" variable
	#if there are no machines it sets the variable to 0
	if machines:
		firewall_status_off = machines.filter(fact__fact_name='mac_firewall_status', fact__fact_data__contains='disabled').count()
	else:
		firewall_status_off = 0

        #This is the data sent from this code to be displayed on the page. 
        #title = the title of the plugin
        #firewallstatus_on = the number displayed in the "Enabled" button
        #firewallstatus_off = the number displayed in the "Disabled" button
        #page and theid are used the same as was passed to this plugin from SAL, so it knows where to display the plugin
        c = Context({
            'title': 'Firewall Status',
            'firewallstatus_on': firewall_status_on,
            'firewallstatus_off': firewall_status_off,
            'page': page,
            'theid': theid
        })
        return t.render(c), 3

    #This next part will allow SAL to build a new page and display the list of the machines that match our criteria
    def filter_machines(self, machines, data):
        if data == 'firewallstatus_on':
            machines = machines.filter(fact__fact_name='mac_firewall_status', fact__fact_data__contains='Firewall is enabled.')
            title = 'Macs with enabled Firewalls'
        elif data == 'firewallstatus_off':
            machines = machines.filter(fact__fact_name='mac_firewall_status', fact__fact_data__contains='disabled')
            title = 'Macs with disabled Firewalls'
        else:
            machines = None
            titles = None
 
        return machines, title
