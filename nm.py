import time

# Preset credentials
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "1234"

MAX_ATTEMPTS = 
FREEZE_SECONDS = 300  # 5 minutes

print("=" * 35)
print("       Welcome to My Website")
print("=" * 35)

attempts = 0

while attempts < MAX_ATTEMPTS:
    username = input("\nEnter username: ")
    if username != CORRECT_USERNAME:
        print(" Wrong username! Please try again.")
        attempts += 1
        remaining = MAX_ATTEMPTS - attempts
        if remaining > 0:
            print(f"   {remaining} attempt(s) left.")
        continue
    password = input("Enter password: ")
    if password != CORRECT_PASSWORD:
        print(" Wrong password! Please try again.")
        attempts += 1
        remaining = MAX_ATTEMPTS - attempts
        if remaining > 0:
            print(f"   {remaining} attempt(s) left.")
        continue
    print("\n Welcome to my website, admin!")
    print("   Login successful.")
    break

else:

    print("\n Too many wrong attempts!")
    print(f"   Your account is frozen for {MAX_ATTEMPTS * 100 // 60} minutes.")
    print("   Please wait...", end="", flush=True)

    for remaining in range(FREEZE_SECONDS, 0, -1):
        mins, secs = divmod(remaining, 60)
        print(f"\r   Time remaining: {mins:02d}:{secs:02d} ", end="", flush=True)
        time.sleep(1)

    print("\n\n Account unfrozen! Restarting login...\n")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
        print("\n Welcome to my website, admin!")
        print("   Login successful.")
    else:
        print("\n Wrong credentials again. Exiting.")