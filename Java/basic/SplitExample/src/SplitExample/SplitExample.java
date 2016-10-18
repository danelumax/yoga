package SplitExample;

public class SplitExample 
{
	public static void main(String[] args) 
	{
		String InputStr = "      1      14     358";
		String[] arrays = InputStr.trim().split("\\s+");
		String s0 = arrays[0];
		String s1 = arrays[1];
		String s2 = arrays[2];
		int num0 = Integer.parseInt(s0);
		int num1 = Integer.parseInt(s1);
		int num2 = Integer.parseInt(s2);
		System.out.println("Split result: " + num0 + ", " + num1 + ", " + num2);
	}
}
