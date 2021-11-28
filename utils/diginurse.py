from utils import diginurse_utils as DGN

if __name__ == "__main__":
    # try:
    #     name = 'Irfan'
    #     mobile_no = 1234567890
        name = "Sofi1234567a"
        mobile_no = 7989898989
        rx = DGN.createPrescription(patient_name=name, dr_name='Dr. Mehta', mobile_no=mobile_no, diagnosis='Fever')
        p = DGN.getPatient(name, mobile_no)
        s = DGN.showSchedule(name, mobile_no)
        print(s)
        DGN.updateSchedule(name, mobile_no, wakeup_time="06:30 - 07:30",
                         dinner_time='19:00-19:30',
                         lunch_time='13:00 -13:30',
                         smoke=False,
                         drink=False,
                         workout=True)
        # DGN.updateSchedule(name, mobile_no, kwargs={'lunch_time': '13:00 -13:30', 'dinner_time': '19:00-19:30'})

        s = DGN.showSchedule(name, mobile_no)
        print(s)
        s = DGN.showNursingRounds(name, mobile_no)
        print(s)
        # DGN.addToDB(name, mobile_no)
        s = DGN.showPrescription(name, mobile_no)
        print(s)

        DGN.updateSchedule(name, mobile_no, wakeup_time="06:30 - 07:30",
                         breakfast_time='07:30 - 08:00',
                         lunch_time='13:00 -13:30',
                         smoke=False,
                         drink=False,
                         workout=True)
        s = DGN.showSchedule(name, mobile_no)
        print(s)
        p.prescription = rx
        DGN.addToDB(name, mobile_no)

        ret = DGN.checkTimeOverlap(name, mobile_no, 'breakfast', '7:29 - 7:45')
        print(f"\n Overlap with {ret}")

        s = DGN.showNursingRounds(name, mobile_no)
        print(s)
        s = DGN.getCurrentRound(name, mobile_no)
        print(s)

        ml = DGN.createMedicalLogs(name, mobile_no)
        s = ml.get()
        print(s)

        print("Get Medicines for breakfast")
        for item in DGN.getMedicines(name, mobile_no, round_type='breakfast'):
            print(str(item[0]), item[1])
        print("Get Vitals for breakfast")
        for item in DGN.getVitals(name, mobile_no, round_type='breakfast'):
            print(str(item[0]), item[1])
        print("Get Symptoms for lunch")
        for item in DGN.getSymptoms(name, mobile_no, round_type='lunch'):
            print(str(item[0]), item[1])

    # except Exception as e:
    #     print(e)
