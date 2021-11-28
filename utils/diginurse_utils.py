# Here we have utility functions to interact with Patient object
from db.patient import Patient
from db.patient import Timing
from logging import getLogger
from db.Prescription import *
from db.medicalLogger import *

logger = getLogger()
# this is a cache to store the Patients which are conversing
Cache = {}


def clearCache():
    Cache.clear()


def getPatient(name, mobile_no):
    """
    Function to fetch the Patient object from MongoDB or from the Cache.
    If object doesnt exists in the DB it will create one and add it to the DB and cache
    :param name:
    :param mobile_no:
    :return:
    """
    # logger.info(f'{__file__} : Inside getPatient {name} , {mobile_no}')
    key = name.lower()+str(mobile_no)
    # search the Patient first in the Cache, if not found then create it
    P = Cache.get(key)
    if P is None:
        rx = createPrescription(name, "Dr. Nitin", mobile_no, "High B P")
        # Patient not found in Cache, now create/add patient to DB
        P = Patient(name, mobile_no, rx=rx)
        Cache[key] = P
        # logger.info(str(P))
    return P


def getPrescription(name, mobile_no):
    logger.info(f'{__file__} : Inside getPrescription {name} , {mobile_no} ')
    p = getPatient(name, mobile_no)
    return p.prescription


def updateRoundTimings(name, mobile_no, **kwargs):
    """
    Function to update and add/modify the complete Patient timings and rounds in the MongoDB
    :param name:
    :param mobile_no:
    :param kwargs:
    :return:
    """
    logger.info(f'{__file__} : Inside updateRoundTimings {name}, {mobile_no} ,{kwargs}')
    # update the Patient in the Cache and in the DB
    p = getPatient(name, mobile_no)
    p.updateSchedule(**kwargs)
    p.setNursingRounds()
    ret = p.addToDB()
    if ret:
        print("\n Patient record updated successfully !!! ")
    else:
        print("\n Unable to update !!! ")


def updateSchedule(name, mobile_no, **kwargs):
    """
    Function to update and add/modify the complete Patient object in the MongoDB
    :param name:
    :param mobile_no:
    :param kwargs:
    :return:
    """
    logger.info(f'{__file__} : Inside updateSchedule {name} , {mobile_no} , {kwargs}')
    # update the Patient in the Cache and in the DB
    p = getPatient(name, mobile_no)
    p.updateSchedule(**kwargs)
    ret = p.addToDB()
    if ret:
        print("\n Patient record updated successfully !!! ")
    else:
        print("\n Unable to update !!! ")

    return ret


def showSchedule(name, mobile_no):
    """
    Function to print the days schedule of the patient
    :param name:
    :param mobile_no:
    :return:
    """
    logger.info(f'{__file__} : Inside showSchedule {name} , {mobile_no}')
    p = getPatient(name, mobile_no)
    s = p.showTimings()
    return s


def showPrescription(name, mobile_no):
    """
    Function to print the prescription set by the doctor
    :param name:
    :param mobile_no:
    :return:
    """
    logger.info(f'{__file__} : Inside showPrescription {name} , {mobile_no}')
    rx = getPrescription(name, mobile_no)
    if rx is not None:
        s = rx.get()
    else:
        s = "There is no prescription added !!"
    return s


def addToDB(name, mobile_no):
    """
    Function to add the complete patient object to the MongoDB
    :param name:
    :param mobile_no:
    :return:
    """
    logger.info(f'{__file__} : Inside addToDB {name} , {mobile_no}')
    p = getPatient(name, mobile_no)
    s = p.addToDB()
    return s


def checkScheduleNoSet(name, mobile_no):
    """
    Function to check whether schedule for the patient is set or not ?
    :param name:
    :param mobile_no:
    :return:  returns False if any timing of schedule is not set
    """
    logger.info(f'{__file__} : Inside checkScheduleNoSet {name} , {mobile_no}')
    p = getPatient(name, mobile_no)
    ret = False
    print(p)
    if p.wakeup_time is None \
            or p.breakfast_time is None \
            or p.lunch_time is None \
            or p.dinner_time is None \
            or p.smoke is None \
            or p.drink is None \
            or p.workout is None:
        ret = True

    return ret


def checkNursingRoundNoSet(name, mobile_no):
    """
    Function to check whether nursing rounds are set for the patient is set or not ?
    :param name:
    :param mobile_no:
    :return:  returns False if any nursing round is not set
    """
    logger.info(f'{__file__} : Inside checkNursingRoundNoSet {name} , {mobile_no}')
    p = getPatient(name, mobile_no)
    ret = False
    if p.wakeup_round is None \
            or p.pre_breakfast_round is None \
            or p.post_breakfast_round is None \
            or p.pre_lunch_round is None \
            or p.post_lunch_round is None \
            or p.pre_dinner_round is None \
            or p.post_dinner_round is None \
            or p.mid_day_round is None \
            or p.evening_round is None \
            or p.workout_round is None:
        ret = True

    return ret


def checkTimeOverlap(name, mobile_no, time_type, time1):
    """
    Function to check if the input time overlaps with patient already added schedule
    :param name:        name of the patient
    :param mobile_no:   mobile no of the patient
    :param time_type:   phase/round/type of the time it is eg. lunch, breakfast or dinner
    :param time1:       time
    :return:            Return True if there is a clash between neighbouring phases/round/time_type
    """
    logger.info(f'{__file__} : Inside checkTimeOverlap {name} , {mobile_no}, {time_type}, {time1}')
    p = getPatient(name, mobile_no)
    t = Timing(time1)
    # TODO : Irfan : need to make changes in this function to return the name of the overlap timing instead of true or flase
    s = "No"
    if time_type is None:
        return 'No'
    if time_type == 'wakeup':
        ret = t.checkOverlap(p.breakfast_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with breakfast_time = {p.breakfast_time}')
            s = 'breakfast'

    if time_type == 'breakfast':
        ret = t.checkOverlap(p.wakeup_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with wakeup_time = {p.wakeup_time}')
            s = 'wakeup'

    if time_type == 'breakfast':
        ret = t.checkOverlap(p.lunch_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with lunch = {p.lunch_time}')
            s = 'lunch'

    if time_type == 'lunch':
        # check overlap with breakfast and dinner_time
        ret = t.checkOverlap(p.breakfast_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with breakfast_time = {p.breakfast_time}')
            s = 'breakfast'

    if time_type == 'dinner':
        # check overlap with bed_time and lunch_time
        ret = t.checkOverlap(p.bed_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with bed_time = {p.bed_time}')
            s = 'bed'

    if time_type == 'bed' or time_type == 'sleep':
        # check overlap with dinner time
        ret = t.checkOverlap(p.dinner_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with dinner_time = {p.dinner_time}')
            s = 'dinner'

    return s


def showNursingRounds(name,  mobile_no):
    logger.info(f'{__file__} : Inside showNursingRounds {name}, {mobile_no}')
    p = getPatient(name, mobile_no)
    p.setNursingRounds()
    s = p.showNursingRounds()

    return s


def createPrescription(patient_name, dr_name, mobile_no, diagnosis):
    logger.info(f'{__file__} : Inside createPrescription {patient_name}, {mobile_no}')
    rx = Prescription(patient_name=patient_name, dr_name=dr_name, mobile_no=mobile_no, diagnosis=diagnosis, diet_considerations='no-Alcohol no-Smoke')
    med1 = Medicine(name='Med1', comment=' for fever', timing='breakfast', quantity=1, duration=5, frequency=1)
    med2 = Medicine(name='Med1', comment=' for fever', timing='lunch', quantity=1, duration=5, frequency=1)
    med3 = Medicine(name='Med2', comment=' for fever', timing='dinner', quantity=1, duration=5)
    med4 = Medicine(name='Med3', comment=' for fever', timing='dinner', quantity=1, duration=30, frequency=7)
    rx.addMedicines(med1)
    rx.addMedicines(med2)
    rx.addMedicines(med3)
    rx.addMedicines(med4)

    test1 = Test(name='Sugar Test', comment=' test for Diabetes', timing='breakfast')
    test2 = Test(name='Sugar Test', comment=' test for Diabetes', timing='Lunch')
    rx.addTest(test1)
    rx.addTest(test2)

    s1 = Symptom(name='Nausea', comment=' feel like vomiting', timing='breakfast')
    s2 = Symptom(name='Weakness', comment=' feeling low', timing='Lunch')
    rx.addSymptoms(s1)
    rx.addSymptoms(s2)

    v1 = Vital(name='BP', comment=' blood pressure', timing='breakfast', limit='140')
    v2 = Vital(name='Temperature', comment=' fever', timing='Lunch', limit='98.6 C')
    rx.addVital(v1)
    rx.addVital(v2)

    e1 = Excercise(name='Morning Walk', comment=' walking', timing='breakfast', reps=10)
    e2 = Excercise(name='Evening Walk', comment=' walking', timing='dinner', reps=10)
    rx.addExcercise(e1)
    rx.addExcercise(e2)

    return rx


def getCurrentRound(name, mobile_no):
    """
    Function to return the which is current round of the day, pre-breakfast, breakfast, post-breakfast, pre-lunch, lunchetc...
    :param name:        name of the patient
    :param mobile_no:   mobile no. of the patient
    :return:            name of current round/phase of the day going on as per the patient schedule and nursing rounds
    """
    logger.info(f'{__file__} : Inside getCurrentRound {name}, {mobile_no}')
    p = getPatient(name, mobile_no)
    s = p.getCurrentRound()
    return s


def updateMedItems(item, status):
    """
    Function to update the status of the MedItem , it can be MEdicine / Test  / Symmptoms / Vitals etc.
    :param item:
    :param status:
    :return:
    """
    item.setStatus(status)


def getMedItemName(item):
    """
    Function to return the name of the item, it can be Medicine / Test  / Symptom / Vitals etc.
    :param item:
    :return:
    """
    return item[0].name


def getMedication(name, mobile_no, item_type, round_type=None):
    '''
    Function to fetch the current dates medication from the Prescription plan
    :param name:
    :param mobile_no:
    :param item_type: type of item eg. Medicine / Test / Symptom / Vital / Excercise  etc.
    :param round_type:   its time/round of that day we need medication eg.  pre-breakfast ,post-breakfast etc.
    :return: a list of tuple with item and its current status
    '''
    # logger.info(f'{__file__} : Inside getMedication {name}, {mobile_no}, {item_type} , {round_type}')
    p = getPatient(name, mobile_no)
    plan = p.prescription.getPlan(datetime.date.today())
    lst = []
    for i in plan:
        item = i[0]     # 0th element is Medicine/Test/Vital/Symptom/Excercise

        if item.typeName() == item_type and item.timing == round_type:
            lst.append(i)
    return lst


def getMedicines(name, mobile_no, round_type=None):
    logger.info(f'{__file__} : Inside getMedicines {name}, {mobile_no}')
    lst = getMedication(name, mobile_no, 'Medicine', round_type)
    return lst


def getVitals(name, mobile_no, round_type=None):
    logger.info(f'{__file__} : Inside getVitals {name}, {mobile_no}')
    lst = getMedication(name, mobile_no, 'Vital', round_type)
    return lst


def getExcercises(name, mobile_no, round_type=None):
    logger.info(f'{__file__} : Inside getExcercises {name}, {mobile_no}')
    lst = getMedication(name, mobile_no, 'Excercise', round_type)
    return lst


def getSymptoms(name, mobile_no, round_type=None):
    logger.info(f'{__file__} : Inside getSymptoms {name}, {mobile_no}')
    lst = getMedication(name, mobile_no, 'Symptom', round_type)
    return lst


def getTests(name, mobile_no, round_type=None):
    logger.info(f'{__file__} : Inside getTests {name}, {mobile_no}')
    lst = getMedication(name, mobile_no, 'Test', round_type)
    return lst


def getDietRecomendation(name, mobile_no):
    logger.info(f'{__file__} : Inside getDietRecomendation {name}, {mobile_no}')
    p = getPatient(name, mobile_no)
    diet = p.prescription.getDietRecomendation()
    return diet


def createMedicalLogs(patient_name, mobile_no):
    logger.info(f'{__file__} : Inside createMedicalLogs {patient_name}, {mobile_no}')
    m = MedicalLogs(name=patient_name, mobile_no=mobile_no)
    data = {'item': 'Medicine1', 'item_type': 'Medicine', 'round_type': 'pre_lunch', 'status': 'Taken'}
    log = Log(**data)
    m.addLog(log)
    data = {'item': 'Medicine1', 'item_type': 'Medicine', 'round_type': 'pre_dinner', 'status': 'Taken'}
    log = Log(**data)
    m.addLog(log)

    return m


def startingFlow(name, mobile_no):
    """
    Function to decide which needs to be executed by the chatbot
    :param name:  name of the patient
    :param mobile_no: mobile_no of the patient
    :return:        name of the flow needs to be initiated by the chatbot
    """
    type_of_flow = ""

    if checkScheduleNoSet(name, mobile_no):
        type_of_flow = "configure"
    elif checkNursingRoundNoSet(name, mobile_no):
        type_of_flow = "new_treatment"
    else:
        type_of_flow = getCurrentRound(name, mobile_no)
        if type_of_flow is None:
            type_of_flow = "nothing_to_do"

    return type_of_flow


def getTreatmentLevel(name, mobile_no):
    """
    function to compare the current date with start of treatment+duration of treatment
    to check how much of treatement (in percentage) is done so far
    :param name:
    :param mobile_no:
    :return:
    """
    logger.info(f'{__file__} : Inside getTreatmentLevel {name}, {mobile_no}')
    return 20


def getPatientStatus(name, mobile_no):
    """
    Function to get last recorded feeling from the plan
    :param name:
    :param mobile_no:
    :return: return the last stored condition
    """
    logger.info(f'{__file__} : Inside getPatientStatus {name}, {mobile_no}')
    p = getPatient(name, mobile_no)
    # yesterday = datetime.date.today() - datetime.timedelta(days=1)
    # lst = p.prescription.getPlan(yesterday)
    # for item in lst:
    #     if item.typeName() == 'Symptoms' and item.status == 'Not well':
    #         return True
    # return False

    # Get the last stored feeling from the prescription
    feeling = p.prescription.getFeeling()
    return feeling


def updatePatientStatus(name, mobile_no, feeling):
    """
    function to update the patients current condition , this detail will be updated in the prescription.feeling
    :param name:
    :param mobile_no:
    :param feeeling:
    :return:
    """
    logger.info(f'{__file__} : Inside updatePatientStatus {name}, {mobile_no} {feeling}')
    p = getPatient(name, mobile_no)
    p.prescription.addFeeling(feeling)
    p.addToDB()
