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

# def process(json_string, db):
#     data = json.loads(json_string)
#     try:
#         # Check if the required keys exist in the data
#         if  data["doc"]["data"]["geo"]:
#             my_id = data["doc"]["_id"]
#             if db.get(my_id):
#                 return 0
#             else:
#                 data["_id"] = my_id
#             doc_id, doc_rev = db.save(data)
#             print(f"ID:{doc_id}rev:{doc_rev}")
#             return 1
#         else:
#             return 0
#     except KeyError:
#         pass



def process(json_string,transport_string,housing_string,income_string,transport_db,income_db,housing_db,total_db):
    data = json.loads(json_string)
    try:
        # Check if the required keys exist in the data
        if  data["doc"]["data"]["geo"] and data["doc"]["data"]["lang"] == "en":
            my_id = data["doc"]["_id"]
            if total_db.get(my_id) or transport_db.get(my_id) or income_db.get(my_id) or housing_db.get(my_id):
                return 0
            else:
                data["_id"] = my_id
            token_list = data["value"]["tokens"].split('|')
            for item in token_list:
                if item.lower() in transport_string:
                    data["topic"] = "transport"
                    transport_db.save(data)
                    print("t")
                    #doc_id, doc_rev = total_db.save(data)
                    #print(f"ID:{doc_id}rev:{doc_rev}")
                    return 1
                elif item.lower() in income_string:
                    data["topic"] = "income"
                    income_db.save(data)
                    print("i")
                    #doc_id, doc_rev = total_db.save(data)
                    #print(f"ID:{doc_id}rev:{doc_rev}")
                    return 1
                elif item.lower() in housing_string:
                    data["topic"] = "housing"
                    housing_db.save(data)
                    print("h")
                    #doc_id, doc_rev = total_db.save(data)
                    #print(f"ID:{doc_id}rev:{doc_rev}")
                    return 1
                else:
                    return 0
        else:
            return 0
    except KeyError:
        pass   

# def tranport_in(json_string, tran_string):
#     data = json.loads(json_string)
#     token_list = data["value"]["tokens"].split('|')
    
#     for item in token_list:
#         if item.lower() in tran_string:
#             return True
#     return False




def process_twitter_data(file_address: str, comm: object, size: int, rank: int,count,transport_db,income_db,housing_db,total_db):
    transport_string = ['taxi','airplane','walk','bus','car', 'bike', 'tram', 'metro', 
                        'publictransport', 'lightrail', 'traffic jam', 
                        'public transport', 'uber', 'railway', 'train', 'transit','airport','signal','parking lot','travel','safety']
    
    housing_string = ["rent","renting","rental","neighborhood","room","real estate", "house","housing","eviction",
                     "construction","shelter","apartment", "lease", "tenant", "landlord","building", 
                     "deposit", "utilities", "sublet", "roommate", "vacancy", "property"]
    
    income_string = ["income", "salary", "wage", "earnings","money","paycheck", "benefits", "bonus", "commission", 
                    "taxes", "deductions", "payroll", "financial", "investment", "profit", "revenue","earn","budget","savings"]

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
                        process(current_line,transport_string,housing_string,income_string,transport_db,income_db,housing_db,total_db)
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
    db_name = "test_transport_twitter"

    db_transport_name = "test_transport_twitter"
    db_income_name = "test_income_twitter"
    db_housing_name = "test_housing_twitter"
    db_total_name = "test_total_twitter"
    # if db_name not in couch:  
    #     db = couch.create(db_name)
    # else:
    #     db = couch[db_name]
    transport_db = couch[db_transport_name]
    income_db = couch[db_income_name]
    housing_db = couch[db_housing_name]
    total_db = couch[db_total_name]

    if rank == 0:
        start = time.time()
    process_twitter_data(twitter_data_address,comm, size, rank,record_count,transport_db,income_db,housing_db,total_db)
    

    if rank == 0:
        end = time.time()
        print("time:",end-start)
