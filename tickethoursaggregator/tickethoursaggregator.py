#!/bin/env python


"""

This will update the target aggregation custom field.

On trac.ini, just insert the following lines:

[tickethoursaggregator]
add_hours_fields = add_dev_hours, add_qa_hours
add_dev_hours = total_dev_hours
add_qa_hours = total_qa_hours
 
"""

import os,sys,urllib,urllib2,time,re
from logbook import Logger,FileHandler
from trac.core import *
from trac.ticket.api import ITicketChangeListener
from trac.web import IRequestHandler
from json import dumps, loads


try:
    
    from urllib.parse import urlparse,parse_qs

except ImportError:
    
    from urlparse import urlparse,parse_qs
    
    
class TicketHoursAggregator(Component):

    implements(ITicketChangeListener,IRequestHandler)

    def __init__(self):
        pass

    def match_request(self,req):
        pass

    def process_request(self,req):
	pass
           
    def ticket_created(self,ticket):
        pass

    def ticket_changed(self,ticket,comment,author,old_values):
        self.ticket = ticket
        self.ticket_id = ticket.id
        self.old_values = old_values
        ticket_id = ticket.id
        config = self.config
        env = self.env
	entry_fields = [entry_field.strip() for entry_field in self.get_entry_fields().split(',')]

	changes_on_monitored_fields = False
	for field in self.old_values.keys():
            if field in entry_fields:
                changes_on_monitored_fields = True
        
	total_hours_fields = []
	if changes_on_monitored_fields:
            for entry_field in entry_fields:
                total_entry_field = self.get_target_fields(entry_field)
                total_hours_fields.append(total_entry_field)
                ticket_field_value = ticket.get_value_or_default(entry_field)
                self.aggregate_on_custom_field(total_entry_field,ticket_field_value)
                self.update_custom_field(entry_field,0)
              
    def ticket_deleted(self,ticket):
        pass
        
    def ticket_comment_modified(self,ticket,cdate,author,comment,old_comment):
        pass

    def ticket_change_deleted(self,ticket,cdate,changes):
        pass
    def set_old_values(self,old_values):
        self.old_values = old_values

    def get_entry_fields(self):
        parser = self.config.parser
	if parser.has_section('tickethoursaggregator'):
            if parser.has_option('tickethoursaggregator','add_hours_fields'):
		self._entry_fields = parser.get('tickethoursaggregator','add_hours_fields')
	return self._entry_fields 

    def get_target_fields(self,entry_field_str):
        parser = self.config.parser
	entry_field = None
	if parser.has_section('tickethoursaggregator'):
            if parser.has_option('tickethoursaggregator', entry_field_str):
		entry_field =  parser.get('tickethoursaggregator',entry_field_str)
	return entry_field

    def aggregate_on_custom_field(self,field_name,field_value):
        with self.env.db_transaction as db:
            cursor = db.cursor()
            sql = """
                UPDATE ticket_custom set value=value+%s WHERE ticket=%s and name="%s"
            """ % (field_value,self.ticket_id,field_name)
            cursor.execute(sql)
    def update_custom_field(self,field_name,field_value):
        with self.env.db_transaction as db:
            cursor = db.cursor()
            sql = """
                UPDATE ticket_custom set value=%s WHERE ticket=%s and name="%s"
            """ % (field_value,self.ticket_id,field_name)
            cursor.execute(sql)


if __name__ == "__main__":
    
    logger = Logger("TicketHoursAggregator")
    logfile = "tickethoursaggregator.log"
    fh = FileHandler(logfile,"a")
    fh.applicationbound()
    fh.push_application()
    
    print("This is just a test.")
    logger.info("Testing logging.")
