from mpi4py import MPI
import json
import math
import time
import os

import re
import couchdb

# def process(json_stirng,db):
#     data = json.loads(json_stirng)
#     if data["doc"]['data']['geo']:
#         my_id = data["doc"]["_id"]
#         if db.get(my_id):
#             return 0 
#         else:
#             data["_id"] = my_id
#         doc_id,doc_rev = db.save(data)
#         #print(f"ID:{doc_id}rev:{doc_rev}")
#         return 1 
#     else:
#         return 0

def process(json_string, db):
    data = json.loads(json_string)
    try:
        # Check if the required keys exist in the data
        if  data["doc"]["data"]["geo"]:
            my_id = data["doc"]["_id"]
            if db.get(my_id):
                return 0
            else:
                data["_id"] = my_id
            doc_id, doc_rev = db.save(data)
            print(f"ID:{doc_id}rev:{doc_rev}")
            return 1
        else:
            return 0
    except KeyError:
        pass



def process_twitter_data(file_address: str, comm: object, size: int, rank: int,db,count):
    f = None
    try:
        f = open(file_address, "r", encoding="utf-8")
        # Skip the first "[" in the json file.
        next(f)
        
        total_byte_size = os.path.getsize(file_address)
        byte_chunk_size = math.ceil(total_byte_size / size)
        end_location = byte_chunk_size * (rank + 1)
        current_line = ""

        f.seek(rank * byte_chunk_size)

        while 1:
                current_line = f.readline()
                if current_line.startswith("{"):
                    if current_line.endswith(",\n"):
                        current_line = current_line[:-2]
                        #print(current_line)
                    if "geo" in current_line:
                        process(current_line,db)
                    #now it is a string include a whole tweet.
                    current_line = ""
                else:
                    current_line = ""
                    if f.tell() > end_location:
                        print("done!")
                        break
                    pass             
        return 

    except FileNotFoundError as e:
        pass
    
    finally:
        if f:
            f.close()



if __name__ == "__main__":
    record_count = 0
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    twitter_data_address = "twitter-huge.json"
    admin_username = 'admin'
    admin_password = '666'
    couch = couchdb.Server('http://{0}:{1}@172.26.135.41:5984/'.format(admin_username, admin_password))
    db_name = "new_twitter"

    if db_name not in couch:  
        db = couch.create(db_name)
    else:
        db = couch[db_name]

    if rank == 0:
        start = time.time()
    process_twitter_data(twitter_data_address,comm, size, rank,db,record_count)
    

    if rank == 0:
        end = time.time()
        print("time:",end-start)
