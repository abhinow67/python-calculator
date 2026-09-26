
a=int (input("enter the first number:"))
b=int (input("enter the second number:"))
c=int(input("enter the third number:"))
d=int(input("enter the fourth number:"))
if a>b and a>c and a>d:
 print("first number is largest")
elif b>c and b>d:
 print("second number is largest")
elif c>d:
 print("thrid number is largest")
else:
 print("fourth number is largest")