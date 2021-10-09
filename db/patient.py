# Here we have the Patient object that intract with the database for updating and getting the patient data
import pandas as pd
import sys

sys.path.append('../')
from db import DB_utils as DB


class Timing:
    def __init__(self, s):
        if s is None or s == 'None':
            self.timing = None
        else:
            self.timing = self.set_time(s)

    def left(self):
        fmt = '%H:%M'
        return self.timing.left.strftime(fmt) if self.timing else None

    def right(self):
        fmt = '%H:%M'
        return self.timing.right.strftime(fmt) if self.timing else None

    def set_time(self, s):
        """
        :param s: is expected in the format as :  <start time H:M> - <end time H:M>
        :return:  object of Timestamp
        """
        lst = s.split("-")
        T = pd.Interval(pd.Timestamp(lst[0].strip()), pd.Timestamp(lst[1].strip()), closed='neither')
        return T

    def get_time(self):
        """
        :return: returns the Timestamp in string format or None
        """
        if self.timing is None:
            return 'None'
        T = self.timing
        fmt = '%H:%M'
        s = T.left.strftime(fmt) + " - " + T.right.strftime(fmt)
        return s

    def __str__(self):
        s = self.get_time()
        return s

    def checkOverlap(self, other):
        if self.timing is None:
            return True
        if other.timing is None:
            return False
        return self.timing.overlaps(other.timing)


class Patient:
    def __init__(self, name, mobile_no, **kwargs):

        self.name = name
        self.mobile_no = mobile_no
        self.dr_name = None
        self.hospital_name = None
        self.diagnosed = None
        self.date_of_admission = None
        self.wakeup_time = None
        self.breakfast_time = None
        self.lunch_time = None
        self.dinner_time = None
        self.bed_time = None
        self.smoke = None
        self.drink = None
        self.workout = None
        self.email_id = None

        # Nursing rounds timings of the day
        self.wakeup_round = None
        self.mid_day_round = None
        self.evening_round = None
        self.workout_round = None
        self.bed_round = None
        self.pre_breakfast_round = None
        self.post_breakfast_round = None
        self.pre_lunch_round = None
        self.post_lunch_round = None
        self.pre_dinner_round = None
        self.post_dinner_round = None

        # Search the DB with the name and mobile no.
        # if found then fetch up all the members from DB
        # else create a new object and add it to DB
        entry = DB.findOne({'name': name, 'mobile_no': mobile_no})
        if entry is not None:
            print(f'{name} and {mobile_no} exists in DB, fetch it !')
            self.name = name
            self.mobile_no = entry.get('mobile_no')
            self.dr_name = entry.get('dr_name')
            self.hospital_name = entry.get('hospital_name')
            self.diagnosed = entry.get('diagnosed')
            self.date_of_admission = entry.get('date_of_admission')
            self.email_id = entry.get('email_id')
            self.updateSchedule(wakeup_time = entry.get("wakeup_time"),
                                breakfast_time = entry.get("breakfast_time"),
                                lunch_time = entry.get("lunch_time"),
                                dinner_time = entry.get("dinner_time"),
                                bed_time = entry.get("bed_time"),
                                smoke = entry.get("smoke"),
                                drink = entry.get("drink"),
                                workout = entry.get("workout"),
                                )
        else:
            print(f'{name} and {mobile_no} do not exists in DB, so create an entry')
            self.name = name
            self.mobile_no = mobile_no
            self.dr_name = kwargs.get('dr_name')
            self.hospital_name = kwargs.get('hospital_name')
            self.diagnosed = kwargs.get('diagnosed')
            self.date_of_admission = kwargs.get('date_of_admission')
            self.wakeup_time = Timing(kwargs.get('wakeup_time')) if kwargs.get('wakeup_time') is not None else None
            self.breakfast_time = Timing(kwargs.get('breakfast_time')) if kwargs.get('breakfast_time') is not None else None
            self.lunch_time = Timing(kwargs.get('lunch_time')) if kwargs.get('lunch_time') is not None else None
            self.dinner_time = Timing(kwargs.get('dinner_time')) if kwargs.get('dinner_time') is not None else None
            self.bed_time = Timing(kwargs.get('bed_time')) if kwargs.get('bed_time') is not None else None
            self.smoke = kwargs.get('smoke')
            self.drink = kwargs.get('drink')
            self.workout = kwargs.get('workout')
            self.email_id = kwargs.get('email_id')
            self.addToDB()

        self.setNursingRounds()

    def showTimings(self):
        s = self.name + " \n"
        s += "Dr. : " + str(self.dr_name) + " \n"
        s += "Wakeup Time    : " + str(self.wakeup_time) + " \n"
        s += "Breakfast Time : " + str(self.breakfast_time) + " \n"
        s += "Lunch Time     : " + str(self.lunch_time) + " \n"
        s += "Dinner Time    : " + str(self.dinner_time) + " \n"
        s += "Bed Time       : " + str(self.bed_time) + " \n"
        s += "Smokes         : " + str(self.smoke) + " \n"
        s += "Drinks         : " + str(self.drink) + " \n"
        s += "WorkOut        : " + str(self.workout) + " \n"
        return s

    def setNursingRounds(self):
        self.wakeup_round = self.wakeup_time.left() if self.wakeup_time else '8:00'
        self.mid_day_round = "12:00"
        self.evening_round = '17:00'
        self.workout_round = '18:00'
        if self.bed_time is not None:
            self.bed_round = self.bed_time.left()
        else:
            self.bed_round = '21:00'

        if self.breakfast_time is not None:
            self.pre_breakfast_round = self.breakfast_time.left()
            self.post_breakfast_round = self.breakfast_time.right()
        else:
            self.pre_breakfast_round = '8:30'
            self.post_breakfast_round = '9:00'

        if self.lunch_time is not None:
            self.pre_lunch_round = self.lunch_time.left()
            self.post_lunch_round = self.lunch_time.right()
        else:
            self.pre_lunch_round = '13:00'
            self.post_lunch_round = '14:00'

        if self.dinner_time is not None:
            self.pre_dinner_round = self.dinner_time.left()
            self.post_dinner_round = self.dinner_time.right()
        else:
            self.pre_dinner_round = '20:00'
            self.post_dinner_round = '21:00'

    def showNursingRounds(self):
        # Nursing rounds timings of the day
        s = self.name + " Nursing Round Details \n"
        s += " Morning Round :" + str(self.wakeup_round) + ' \n'
        s += " Mid Day Round :" + str(self.mid_day_round) + ' \n'
        s += " Evening Round :" + str(self.evening_round) + ' \n'
        s += " Workout Round :" + str(self.workout_round) + ' \n'
        s += " BedTime Round :" + str(self.bed_round) + ' \n'
        s += " Pre Breakfast :" + str(self.pre_breakfast_round) + ' \n'
        s += " Post Breakfast:" + str(self.post_breakfast_round) + ' \n'
        s += " Pre Lunch     :" + str(self.pre_lunch_round) + ' \n'
        s += " Post Lunch    :" + str(self.post_lunch_round) + ' \n'
        s += " Pre Dinner    :" + str(self.pre_dinner_round) + ' \n'
        s += " Post Dinner   :" + str(self.post_dinner_round) + ' \n'

        return s

    def __str__(self):
        s = self.showTimings()
        return s

    def updateSchedule(self, **kwargs):
        if kwargs.get('wakeup_time') is not None and kwargs.get('wakeup_time') != 'None':
            self.wakeup_time = Timing(kwargs.get('wakeup_time'))
        if kwargs.get('breakfast_time') is not None and kwargs.get('breakfast_time') != 'None':
            self.breakfast_time = Timing(kwargs.get('breakfast_time'))
        if kwargs.get('lunch_time') is not None and kwargs.get('lunch_time') != 'None':
            self.lunch_time = Timing(kwargs.get('lunch_time'))
        if kwargs.get('bed_time') is not None and kwargs.get('bed_time') != 'None':
            self.bed_time = Timing(kwargs.get('bed_time'))
        if kwargs.get('dinner_time') is not None and kwargs.get('dinner_time') != 'None':
            self.dinner_time = Timing(kwargs.get('dinner_time'))
        if kwargs.get('smoke') is not None and kwargs.get('smoke') != 'None':
            self.smoke = kwargs.get('smoke')
        if kwargs.get('drink') is not None and kwargs.get('drink') != 'None':
            self.drink = kwargs.get('drink')
        if kwargs.get('workout') is not None and kwargs.get('workout') != 'None':
            self.workout = kwargs.get('workout')

    def addToDB(self):
        entry = {'name': self.name, 'dr_name': self.dr_name,
                 'hospital_name': self.hospital_name,
                 'diagnosed': self.diagnosed,
                 'date_of_admission': self.date_of_admission,
                 'wakeup_time': str(self.wakeup_time),
                 'breakfast_time': str(self.breakfast_time),
                 'lunch_time': str(self.lunch_time),
                 'dinner_time': str(self.dinner_time),
                 'bed_time': str(self.bed_time),
                 'workout': str(self.workout),
                 'smoke': self.smoke,
                 'drink': self.drink,
                 'mobile_no': self.mobile_no,
                 'email_id': self.email_id
                 }
        try:
            ret = DB.addOne(entry)
            print('Patient updated into DB')
            return ret
        except Exception as e:
            print(f"Exception while inserting into db!! {e}")
            return False

    def checkOverlap(self, time1, time2):
        t1 = Timing(time1)
        t2 = Timing(time2)

        ret = t1.Timing(t2)
        return ret


if __name__ == "__main__":
    # try:

    P = Patient('Irfan Ali', 1234567890)
    P.addToDB()
    print(P.showTimings())
    print(f'Total entries in DB = {DB.count()}')

    P1 = Patient('Irfan Ali Chandurwala', 1234567890, bed_time='20:00 - 21:00')
    P1.showTimings()
    P1.addToDB()
    print(f'Total entries in DB = {DB.count()}')

    # db = DB.getDB()
    # DB.removeAll(db)
    # DB.createDB(db)

    # DB.findAll(db)

    entry = {'name': 'Irfan Ali', 'modile_no': 1234567890}
    record = DB.findOne(entry)
    if record is not None:
        print(record)
    else:
        print('Record not found')
    # except Exception as e:
    #     print(e)

    DB.closeDB()
