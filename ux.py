import time

correct_username = "Abhinow"
correct_password = "1234"

attempt = 3

while attempt > 0:
    username = input("Enter the name: ")
    password = input("Enter the password: ")
    
    if username == correct_username and password == correct_password:
        print("Welcome to my website", username)
        
    else:
        attempt -= 1
        print(f"Wrong! {attempt} attempts remaining.")
        
        if attempt == 0:
            print("Too many failed attempts. Please wait 60 seconds.")
            time.sleep(60)