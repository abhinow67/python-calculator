correct_password = "1234"

login = input("Enter username: ")
print("Username:", login)

attempts = 0

while attempts < 3:
    password = input("Enter password: ")

    if password == correct_password:
        print("Welcome to my website!")
        break
    else:
        print("Wrong password")
        attempts += 1

if attempts == 3:
    print("Account locked for 5 minutes") 