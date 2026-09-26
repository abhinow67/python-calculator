import time
correct_username="Abhinow"
correct_password="1234"
username=input("enter the name:")
password=input("enter the password:")
if username==correct_username and password==correct_password:
    print("welcome to my website",username)
attempt=3
while attempt>=3:
 print("wait check is happen")
time.sleep(60)
attempt=-60
