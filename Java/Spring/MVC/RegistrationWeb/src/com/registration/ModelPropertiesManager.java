package com.registration;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Properties;

import com.pojo.RentData;

public class ModelPropertiesManager {
	private Properties pps;
	private String filePath;
	private static ModelPropertiesManager instance;
	
	private ModelPropertiesManager(String filePath) {
		pps = new Properties();
		this.filePath = filePath;
		
		File file = new File(this.filePath);
		if(!file.exists()) {
			System.out.println("no file");
		} else {
			System.out.println("file");
		}
	}
	
	public static ModelPropertiesManager getInstance() {
		if (null == instance) {
			instance = new ModelPropertiesManager("C://Users//eliwech//Desktop//OS//yoga//Java//Spring//MVC//RegistrationWeb//resource//store.properties");
		}
		return instance;
	}
	
	public String getFilePath() {
		return filePath;
	}

	public void setFilePath(String filePath) {
		this.filePath = filePath;
	}

	public void initProperties() throws FileNotFoundException, IOException {
		try(InputStream in = new BufferedInputStream(new FileInputStream(this.filePath))) {
			this.pps.load(in);
		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}
	
	public void writeProperties(String key, String value) 
			throws FileNotFoundException, IOException {
		try(OutputStream out = new FileOutputStream(this.filePath)) {
			this.pps.setProperty(key, (String)value);
			this.pps.store(out, "Update" + key);
		} 
	}
	
	public void saveStudent(RentData student) throws IOException {
		try {
			writeProperties("HostName", student.getHostName());
			writeProperties("eid", student.getEid());
			writeProperties("Duration", Integer.toString(student.getDuration()));
		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}
	
	public void saveModeltoProperties(RentData student) throws FileNotFoundException, IOException {
		initProperties();
		saveStudent(student);
	}
}
