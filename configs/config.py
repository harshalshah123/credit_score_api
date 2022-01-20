import os
import socket
DIR_PATH = os.getcwd()
CONFIG_PATH = os.path.join(DIR_PATH, "configs/")
LOGGER_PATH = os.path.join(DIR_PATH, 'log')
MODEL_PATH = os.path.join(DIR_PATH, 'modelling/')

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

mode = 1
if mode == 1:
    conn_str = "mongodb://rd_0508:tqyi1ydxqRTk3T3v@line-prod-shard-00-00.qswq9.mongodb.net:27017,line-prod-shard-00-01.qswq9.mongodb.net:27017,line-prod-shard-00-02.qswq9.mongodb.net:27017/line_prod?authSource=admin&replicaSet=atlas-oqfnm1-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"
    dbname = "line_prod"
else:
    conn_str = "mongodb+srv://vibe:F9WBJ0Vvx4bT44Ps@vibe-dev.uocnt.mongodb.net/line?retryWrites=true&w=majority"
    dbname = "line"


