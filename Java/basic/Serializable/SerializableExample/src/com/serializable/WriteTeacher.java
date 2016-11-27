package com.serializable;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;

public class WriteTeacher {

	public static void main(String[] args) throws Exception {
		try(ObjectOutputStream oos = new ObjectOutputStream (new FileOutputStream("teacher.txt"))) {
			Person per = new Person("Sun Wukong", 500);
			Teacher t1 = new Teacher("TangSeng", per);
			Teacher t2 = new Teacher("Puti", per);
			
			oos.writeObject(t1);
			oos.writeObject(t2);
			oos.writeObject(per);
			oos.writeObject(t2);
			
			System.out.println("Serializable Ouput Done ...");
			
		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}
}
