import couchdb
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict

#need to download the stopwords for the first time running 
#nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
word_count = defaultdict(int)

#remove the common stop words in the input string
def clean_count(input_str,stop_words,word_count:dict):
    words = word_tokenize(input_str.lower())
    filtered_words = [word for word in words if word not in stop_words]
    for word in filtered_words:
        word_count[word]+=1
    # output_str = " ".join(filtered_words)
    # print(output_str)
    return 

# remove the punctuations and all useless symbols
def clean_string(input_str):
    # Remove "@" and "#" symbols
    input_str = re.sub(r'[@#]', '', input_str)
    
    # Remove "http://" substrings
    input_str = re.sub(r'http://\S+', '', input_str)
    
    # Remove emojis
    input_str = input_str.encode('ascii', 'ignore').decode('ascii')
    
    # Remove remaining punctuations
    input_str = re.sub(r'[^\w\s]', '', input_str)
    
    return input_str
# sort and print the top n word after the word count.
def get_top(num,input_dict):
    sorted_dict = dict(sorted(input_dict.items(), key=lambda item: item[1], reverse=True))
    # Print the top 10 items in the sorted dictionary
    count = 0
    for key, value in sorted_dict.items():
        print(f"{key}: {value}")
        count += 1
        if count == num:
            break

admin_username = 'admin'
admin_password = '666'
couch = couchdb.Server('http://{0}:{1}@172.26.135.41:5984/'.format(admin_username, admin_password))

#change here to the db want to check(slow if db large)
#db_name = "new_twitter"
#db_name = "just4test"
db_name = "big_test"
db = couch[db_name]

# # Fetch all documents in the database
all_docs = db.view('_all_docs')

#loop and get the result
for doc in all_docs:
    #print(doc.id)
    now = db[doc.id]
    if now["doc"]["data"]["lang"] == "en":
        text = clean_string(now["doc"]["data"]["text"])
        clean_count(text,stop_words,word_count)

print("done!")
get_top(10,word_count)


