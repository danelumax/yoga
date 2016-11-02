package RandomAccessFileTest;

import java.io.IOException;
import java.io.RandomAccessFile;

public class RandomAccessFileTest {

	public static void main(String[] args) {
		try(
			RandomAccessFile raf = new RandomAccessFile(
					"RandomAccessFileTest.java", "r")){
			System.out.println("\nRandomAccessFile File Pointer Initial Position: " 
				+ raf.getFilePointer());
			raf.seek(300);
			byte[] bbuf = new byte[1024];
			int hasRead = 0;
			
			System.out.println("\nThen Output java file: ");
			while((hasRead = raf.read(bbuf)) > 0) {
				System.out.println(new String(bbuf, 0, hasRead));
			}
		}
		catch(IOException ex) {
			ex.printStackTrace();
		}
	}

}
