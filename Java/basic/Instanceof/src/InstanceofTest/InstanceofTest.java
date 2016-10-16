package InstanceofTest;

public class InstanceofTest 
{
	public static void main(String[] args) 
	{
		Object hello = "Hello";
		System.out.println("string is the instance of Object Class: " + (hello instanceof Object));
		System.out.println("string is the instance of String Class: " + (hello instanceof String));
		System.out.println("string is the instance of Math Class: " + (hello instanceof Math));
		System.out.println("string is the instance of Comparable Class: " + (hello instanceof Comparable));
		
		//String a = "Hello";
		//System.out.println("string is the instance of Math Class: " + (a instanceof Math));
	}
}
