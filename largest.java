import java.util.Scanner;

public class largest{
public static void main(String[] args){
// create scanner object to read input
Scanner  sc = new Scanner(System.in);

// Read three numbers from the user
System.out.print("enter first number:");
int a = sc.nextInt();

System.out.print("enter second number:");
int b = sc.nextInt();

System.out.print("enter third number:");
int c = sc.nextInt();

// Determine the largest number using if-else-if ladder
if (a>=b && a>=c)
System.out.println(a + " is the largest number.");
else if(b>=c)
System.out.println(b + "is the largest number.");
else
System.out.println(c + 
+"is the largest number.");

// close the scanner
 sc.close();
}