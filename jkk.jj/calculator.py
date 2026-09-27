a=(int(input("enter the number:")))
b=(int(input("enter the number:")))
choice=(input("enter the sign('+','-','/','//','%',):"))
if choice == "+":
    print(a+b)
if choice=="-":
    print(a-b)
if choice =="/":
    print (a/b)
if choice== "//":
    print(a//b)
if choice == "%":
    print(a%b)
else:
    print("you have entered wrong sign")