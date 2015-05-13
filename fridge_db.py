'''
Created on 13/mag/2015

@author: Fabio
'''

class FridgeDb(object):
    connection = None
    cursor = None
    log_calls = False

    def __init__(self, connection):
        '''
        Constructor
        '''
        self.connection = connection
        self.cursor = connection.cursor()

    def commit(self):
        self.connection.commit()

    def log_execute(self, query):
        if self.log_calls:
            print "[Q]", query
        return self.cursor.execute(query)
    
    def get_all(self):
        all_list = []
        self.log_execute('SELECT * FROM stocks')
        
        while True:
            fetched_item = self.cursor.fetchone()
            if fetched_item is None:
                break
            all_list.append(fetched_item)
            
        return all_list
    
    def get_item(self, item_id):
        self.log_execute('SELECT * FROM stocks WHERE id="%s"' % item_id)
        fetched_item = self.cursor.fetchone()
        return fetched_item
    
    def add_item(self, item_id, quantity=1, name="new item"):
        fetched = self.get_item(item_id)
        if fetched is None:
            # create
            self.log_execute('''INSERT INTO stocks VALUES
                     ('%s', '%s', %i)''' % (item_id, name, quantity))
        else:
            # update
            new_quantity = fetched[2] + quantity
            self.log_execute("UPDATE stocks SET quantity=%i WHERE id='%s'" % (new_quantity, item_id))
    
    def create_schema(self):
        self.log_execute('''CREATE TABLE stocks
                 (id text, name text, quantity integer)''')
