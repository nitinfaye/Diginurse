# Here we connect with MONGODB and create a sample DB
from pymongo import MongoClient
from random import randint


client = None
db = None
MONGODB_URL = 'mongodb://localhost:27017/'
# MONGODB_URL = "mongodb://localhost:5017/"


def getDB():
    global db
    global client
    if db == None:
        client = MongoClient(MONGODB_URL)
        db = client.business
    return db


def closeDB():
    global client

    if client is not None:
        client.close()


def removeAll():
    db = getDB()

    db.patient.remove({})


def removeOne(mobile_no):
    db = getDB()
    db.patient.delete_one({'mobile_no': mobile_no})
    print('Deleted Entry from DB')


def findAll():
    ' returns all the records( a dictionary) in the form of a list '
    db = getDB()

    cursor = db.patient.find({} , {'_id' : 0 })
    lst = []
    for record in cursor:
        lst.append(record)
    return lst


def findOne(input : dict):
    ' input is dictionary with all the parameter and its value'
    ' returns a single record if found else None'
    db = getDB()
    record = db.patient.find( input, {'_id': 0})
    if record.count():
        return record[0]
    else:
        return None


def count():
    db = getDB()
    return db.patient.count_documents({})


def addOne(input : dict):
    db = getDB()
    res = db.patient.update_one({'name': input['name']}, {"$set": input}, upsert=True)
    if res.matched_count or res.modified_count:
        return True
    elif res.upserted_id is not None:
        return True
    else:
        return False

def createSampleDB():
    db = getDB()

    names = ['Irfan','Saba','Prasanta', 'Nitin', 'Azra','Ramesh','Mahesh', 'Suresh','Dinesh', 'Rakesh','Rajesh']
    dr_name = ['Dr. Prasanta','Dr. Nitin','Dr. Khan','Dr. Gupta', 'Dr. Dutta']
    diagnosed = ['Diagnosis 1', 'Diagnosis 2', 'Diagnosis 3', 'Diagnosis 4']
    hospital_name = ['Apollo Hospital' , 'Nawaz Hospital' , 'Pulse Hospital' , 'Greater Kailaash Hospital' , 'Bombay Hospital']
    for x in range(1, 501):
        name = names[randint(0, (len(names)-1))]
        email = name.lower() + "@gmail.com"
        patient = {
            'name' : name ,
            'dr_name' : dr_name[randint(0, (len(dr_name)-1))] ,
            'hospital_name' : hospital_name[randint(0, (len(hospital_name)-1))] ,
            'diagnosed' : diagnosed[randint(0, (len(diagnosed)-1))] ,
            'date_of_admission': '01-09-2021',
            'wakeup_time': '07:00 - 08:00',
            'bed_time': '22:00 - 23:00',
            'breakfast_time': '10:00 - 10:30',
            'lunch_time': '13:00 - 14:00',
            'dinner_time': '20:00 - 21:00',
            'smoke': False,
            'drink': False,
            'workout': False,
            'mobile_no': int (str( randint(1,9))+str( randint(0,9))+str( randint(0,9))+str( randint(0,9))+str( randint(0,9))+str( randint(0,9))+str( randint(0,9))+str( randint(0,9))+str( randint(0,9))+str( randint(0,9)) ),
            'email_id': email
        }

        print(patient)
        #Step 3: Insert business object directly into MongoDB via insert_one
        result=db.patient.insert_one(patient)
        #Step 4: Print to the console the ObjectID of the new document
        print('Created {0} of 500 as {1}'.format(x,result.inserted_id))
    #Step 5: Tell us that you are done
    print(f'finished creating {db.patient.count()} patient entries in the DB.')

#
# def find_a_rating(db, rating):
#     rat = db.reviews.find_one({'rating': rating})
#     print(rat)
#     return rat['name']
#
#
# def find_count_of_a_rating(db, rating):
#     print('The number of 5 star reviews:')
#     count = db.reviews.find({'rating': rating}).count()
#     print(count)
#     return count
#
#
#
# def list_all_reviews(db):
#     # To find() all the entries inside collection name 'myTable'
#     cursor = db.reviews.find()
#     s = ""
#     for record in cursor:
#         s = s + record['name'] + " - " + record['cuisine'] + "\n"
#         print(record['name'] + " - " + record['cuisine'])
#     return s


if __name__ == "__main__":
    createSampleDB()
