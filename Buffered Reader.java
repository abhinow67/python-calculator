import java.io.BufferedReader;
import java.io.IOExpectation;
import java.io. Input Stream Reader;
Public class Read Data Example
{
public static void main(String[] args) throws IOException
{
Buffered Reader br=new Buffered Reader(new InputStreamReader (System.in));
System.out.println("enter your name:");
String str=br.readLine();
System.out.println("enter your age:"); 
int age= Integer. parseInt (br.readLine());
System.out.print\n("Are you male/female(type M or F:");
Char Ch=(char) br.read();
System.out.print\n(" Name is:"+str);
System.out.print\n(" Age is:"+age);
System.out.print\n(" gender is:"+Ch);
}
}