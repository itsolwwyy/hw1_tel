import schedule_test

def  helo_world():
    print("Hello WOrld")

schedule_test(1).seconds.do(helo_world)

while True:
    schedule_test.run_pending()
