import time
correct_username="abhiniow"
correct_password="1234"
username=input("enter the userame",correct_username)
password=input("enter the password",correct_password)
attempt=3
if correct_username == username and correct_password == password :
 print("you have entered sucessfully")
else:
 print("you have frez")
while attempt >=3:
 time.sleep (60)