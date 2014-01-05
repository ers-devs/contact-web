'''
@author: cgueret
'''

class Controller(object):
	def __init__(self, view, model):
		'''
		Constructor
		'''
		# Keep a pointer to the view and the model
		self._model = model
		self._view = view

		# Local variables
		self._selected_entity_name = None
		
		# Add a timeout to update contacts and force first call
		self._previous_contact_list = None
		
	def _contact_selected_cb(self, identifier):
		'''
		Called when a contact is selected
		'''		
		# Get the entity description from the model
		self._selected_entity_name = identifier
		
		# Refresh the display of the description
		entity_descriptions = self.refresh_entity_description()
		
		# Refresh the activation of the buttons
        # TODO
        # self.refresh_toolbar_buttons()
        
		return entity_descriptions

	def _new_prop_clicked_cb(self, params):
		'''
		Called when the button to add a new property/value is pressed
		'''
		# Get the selected property and value (return if blank)
		if params['property'] == '' or params['value'] == '':
			return
		
		# Add the property/value to the description of the entity
		self._model.add_property(self._selected_entity_name, params['property'], params['value'])
		
		# Refresh the display
		entity_descriptions = self.refresh_entity_description()
		
		return entity_descriptions

	def _delete_prop_clicked_cb(self, params):
		'''
		Called when the button to delete a property/value is pressed
		'''
		# Delete the property/value to the description of the entity
		self._model.delete_property(self._selected_entity_name, params['property'], params['value'])
		
		# Refresh the display
		entity_descriptions = self.refresh_entity_description()
		
		return entity_descriptions
        
	def _update_contacts_cb(self):
		'''
		Called on a regular basis to update the list of contacts available
		'''
		contacts = sorted(self._model.get_contacts())
        # if self._previous_contact_list == None or self._previous_contact_list != contacts:
		self._previous_contact_list = contacts
		contacts_list = []
		print "CONTACTS: ",contacts
		for contact in contacts:
			# By default, show the URN
			contact_display_name = contact
			# If the contact is ourselves, display "Me"
			if contact == self._model.get_own_contact_name():
				contact_display_name = 'Me'
			# Add the entry
			contacts_list.append({ "contact": contact, "name": contact_display_name })
		return contacts_list

	def _keep_clicked_cb(self):
		'''
		Called then the keep button is pressed
		'''
		self._model.cache_entity(self._selected_entity_name)
        # TODO
        # self.refresh_toolbar_buttons()

	def refresh_entity_description(self):
		'''
		Display all the properties of an entity in a grid
		'''
		# Get the description
		entity = self._model.get_entity_description(self._selected_entity_name)
		
		entity_descriptions = []
        
		for key, values in entity.iteritems():
			for value in values:
				entity_descriptions.append({'property' : key, 'value' : value});
        
		return entity_descriptions
		
	def refresh_toolbar_buttons(self):
		'''
		Update the status of the buttons in the toolbar depending on the contact selected
		'''
        # VIEW
		# Keep button is enabled by default...
		keep_button_obj = self._view.get_object('button_keep')
		keep_button_obj.set_sensitive(True)
		
		# disabled for the owner profile
		if self._selected_entity_name == self._model.get_own_contact_name():
			keep_button_obj.set_sensitive(False)
			
		# and disabled for contacts that are already in cache
		if self._model.is_cached(self._selected_entity_name):
			keep_button_obj.set_sensitive(False)