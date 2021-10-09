from utils import diginurse_utils as DGN

if __name__ == "__main__":
    # try:
        name = 'Quasim Ali'
        mobile_no = 1234567890
        p = DGN.getPatient(name, mobile_no)
        s = DGN.showSchedule(name, mobile_no)
        print(s)
        # DGN.updateSchedule(name, mobile_no, wakeup_time="06:30 - 07:30",
        #                  breakfast_time='07:30 - 08:00',
        #                  lunch_time='13:00 -13:30',
        #                  smoke=False,
        #                  drink=False,
        #                  workout=True)
        DGN.updateSchedule(name, mobile_no, kargs = {'lunch_time': '13:00 -13:30'})

        s = DGN.showSchedule(name, mobile_no)
        print(s)
        s = DGN.showNursingRounds(name, mobile_no)
        print(s)
        # DGN.addToDB(name, mobile_no)

        ret = DGN.checkTimeOverlap(name, mobile_no, 'break_fast', '7:31 - 7:45')
        print("\n\n Overlap ") if ret else print("\n\n No Overlap")
    # except Exception as e:
    #     print(e)
