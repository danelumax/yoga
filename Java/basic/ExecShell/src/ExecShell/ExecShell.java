package ExecShell;

import java.io.*;

public class ExecShell 
{
	public static void main(String[] args) 
	{
		String[] cmd = new String[]{"/bin/bash", "-c", "whoami"};
		String line = "";
		String Result = "";
		try
		{
			Process ps = Runtime.getRuntime().exec(cmd);
			InputStream fis = ps.getInputStream();
			BufferedReader input = new BufferedReader(new InputStreamReader(fis));
			while((line = input.readLine()) != null)
			{
				Result = Result + line;
			}
			System.out.println("cmd result: " + Result);
			input.close();
		} catch (IOException e){
		}
	}

}
