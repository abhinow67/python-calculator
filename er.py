print("Welcome to my calculator")
num=(int(input("enter the number:")))
num2=(int(input("enter the number:")))
choice=(input("eneter(+,-,/,//:)"))
if choice=="+":
    print(num+num2)
if choice=="-":
    print(num-num2)
if choice=="/":
    print(num/num2)

if choice=="//":
    print(num//num2)
else:
    print("you have entered wrong sign" ,end='')