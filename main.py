'''
Created on 13/mag/2015

@author: Fabio
'''
import config
import fridge_db
import sqlite3
import sys

def require_args(num):
    if len(sys.argv) < (num + 1):
        print "[E] not enough arguments (need", num, ")"
        return False
    return True

if not require_args(1):
    exit()

conn = sqlite3.connect(config.DB_FILE)
db = fridge_db.FridgeDb(conn)
db.log_calls = config.LOG_SQL_CALLS

cmd_to_execute = sys.argv[1]

if cmd_to_execute == "get_quantity":
    item_id = sys.argv[2]
    item = db.get_item(item_id)
    if item is None:
        print "0"
    else:
        print item[2] 
        
elif cmd_to_execute == "add":
    item_id = sys.argv[2] 
    quantity = int(sys.argv[3])
    
    if len(sys.argv) >= 5:
        name = sys.argv[4]
    else:
        name = ""
        
    db.add_item(item_id, quantity, name)
    db.commit()
    
    item = db.get_item(item_id)
    print item[2]

elif cmd_to_execute == "get_all":
    l = db.get_all()
    for el in l:
        print str(el[0])+"|"+str(el[1])+"|"+str(el[2])
        
elif cmd_to_execute == "get_all_human":
    l = db.get_all()
    for el in l:
        print str(el[1])+"\t\tid="+str(el[0])+"\t\tquantity="+str(el[2])

else:
    print "[E], invalid command"

db.commit()
conn.close()
