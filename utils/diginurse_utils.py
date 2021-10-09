# Here we have utility functions to  intract with Patient object
from db.patient import Patient
from db.patient import Timing
from logging import getLogger
logger = getLogger()
# this is a cache to store the Patients which are conversing
Cache = {}


def clearCache():
    Cache.clear()


def getPatient(name, mobile_no):
    logger.info(f'{__file__} : Inside getPatient {name} , {mobile_no}')
    key = name.lower()+str(mobile_no)
    # search the Patient first in the Cache, if not found then create it
    P = Cache.get(key)
    if P is None:
        # Patient not found in Cache, now create/add patient to DB
        P = Patient(name, mobile_no)
        Cache[key] = P
        # logger.info(str(P))
    return P


def updateSchedule(name, mobile_no, **kwargs):
    logger.info(f'{__file__} : Inside updateSchedule {name} , {mobile_no} , {kwargs}')

    # update the Patient in the Cache and in the DB
    p = getPatient(name, mobile_no)
    p.updateSchedule(**kwargs)
    ret  = p.addToDB()
    return ret


def showSchedule(name, mobile_no):
    logger.info(f'{__file__} : Inside showSchedule {name} , {mobile_no}')
    p = getPatient(name, mobile_no)
    s = p.showTimings()
    return s


def addToDB(name, mobile_no):
    logger.info(f'{__file__} : Inside addToDB {name} , {mobile_no}')
    p = getPatient(name, mobile_no)
    s = p.addToDB()
    return s


def checkScheduleNoSet(name, mobile_no):
    """
    :param name:
    :param mobile_no:
    :return:  returns False if any timing of schedule is not set
    """
    logger.info(f'{__file__} : Inside checkScheduleNoSet {name} , {mobile_no}')
    p = getPatient(name, mobile_no)
    ret = False
    if p.wakeup_time is None \
            or p.breakfast_time is None \
            or p.lunch_time is None \
            or p.dinner_time is None \
            or p.smoke is None \
            or p.drink is None \
            or p.workout is None:
        ret = True

    return ret


def checkTimeOverlap(name, mobile_no, time_type, time1):
    logger.info(f'{__file__} : Inside checkTimeOverlap {name} , {mobile_no}, {time_type}, {time1}')
    p = getPatient(name, mobile_no)
    t = Timing(time1)
    # TODO : Irfan : need to make changes in this function to return the name of the overlap timing instead of true or flase
    str = "No"
    if time_type is None:
        return 'No'
    if time_type == 'wakeup':
        ret = t.checkOverlap(p.breakfast_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with breakfast_time = {p.breakfast_time}')
            str = 'breakfast'

    if time_type == 'breakfast':
        ret = t.checkOverlap(p.wakeup_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with wakeup_time = {p.wakeup_time}')
            str = 'wakeup'

    if time_type == 'breakfast':
        ret = t.checkOverlap(p.lunch_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with lunch = {p.lunch_time}')
            str = 'lunch'

    if time_type == 'lunch':
        # check overlap with breakfast and dinner_time
        ret = t.checkOverlap(p.breakfast_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with breakfast_time = {p.breakfast_time}')
            str = 'breakfast'

    if time_type == 'dinner':
        # check overlap with bed_time and lunch_time
        ret = t.checkOverlap(p.bed_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with bed_time = {p.bed_time}')
            str = 'bed'

    if time_type == 'bed' or time_type == 'sleep':
        # check overlap with dinner time
        ret = t.checkOverlap(p.dinner_time)
        if ret:
            logger.info(f'{__file__} : \t {time_type} Overlaps with dinner_time = {p.dinner_time}')
            str = 'dinner'

    return str


def showNursingRounds(name,  mobile_no):
    """
        Returns the recommendation based on the persons health status given by doctor
    """
    logger.info(f'{__file__} : Inside getNursingRounds {name}, {mobile_no}')
    p = getPatient(name, mobile_no)
    s = p.showNursingRounds()

    return s
