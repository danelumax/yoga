package TestProperties;

import java.util.Enumeration;
import java.util.Properties;
import java.io.*;

public class TestProperties {

	public static String getValueByKey(String filePath, String key) {
		Properties pps = new Properties();
		try {
			InputStream in = new BufferedInputStream (new FileInputStream(filePath));
			pps.load(in);
			String value = pps.getProperty(key);
			System.out.println(key + " = " + value);
			return value;
		}catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}
	
	public static void getAllProperties(String filePath)
		throws IOException {
		Properties pps = new Properties();
		InputStream in = new BufferedInputStream(new FileInputStream(filePath));
		pps.load(in);
		Enumeration<?> en = pps.propertyNames();
		
		while(en.hasMoreElements()) {
			String strKey = (String)en.nextElement();
			String strValue = pps.getProperty(strKey);
			System.out.println(strKey + "=" + strValue);
		}
	}
	
	public static void WriteProperties(String filePath, String pKey, String pValue)
		throws IOException {
		Properties pps = new Properties();
		InputStream in = new BufferedInputStream(new FileInputStream(filePath));
		pps.load(in);
		
		OutputStream out = new FileOutputStream(filePath);
		pps.setProperty(pKey, pValue);
		
		/* add comment
		 * #Update long name
		 * #Thu Oct 27 13:47:35 CST 2016
		 */
		pps.store(out, "Update " + pKey + " name");
	}
	
	public static void main(String[] args) 
		throws IOException {
		String fileName = "Test.properties";
		System.out.println("\nTest Get Single Value ...");
		String value = getValueByKey(fileName, "name");
		System.out.println(value);
		
		System.out.println("\nTest Get All Values ...");
		getAllProperties(fileName);
		
		System.out.println("\nTest Add one Single Value ...");
		WriteProperties(fileName, "long", "212");
			
	}
	
}
