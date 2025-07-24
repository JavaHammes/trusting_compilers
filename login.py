def login():
    user_input = input("Password: ")

    if user_input == "1234":
        print("Access granted")
    else:
        print("Access denied")

login()
