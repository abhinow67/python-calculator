import time

correct_username = "Abhinow"
correct_password = "1234"
attempts = 3

# We start the loop here
while attempts > 0:
    print(f"\nAttempts remaining: {attempts}")
    username = input("enter the username: ")
    password = input("enter the password: ")

    if username == correct_username and password == correct_password:
        print("you have entered right")
        # Since they got it right, we use 'break' to jump out of the loop
        break 
    else:
        attempts -= 1 # This subtracts 1 from your 3 attempts
        if attempts > 0:
            print("you have entered invalid password. Try again.")
        else:
            print("No attempts left. Access Denied.")

# The program continues here after a successful login or running out of tries