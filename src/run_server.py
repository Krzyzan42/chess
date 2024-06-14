from networking.server.server import Server
from networking.server.models import *
import time
        
init_db()
server = Server()
time.sleep(2)
server.run()