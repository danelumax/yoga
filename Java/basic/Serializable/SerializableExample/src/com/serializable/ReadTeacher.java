package com.serializable;

import java.io.FileInputStream;
import java.io.ObjectInputStream;

public class ReadTeacher {

	public static void main(String[] args) throws Exception {
		try(ObjectInputStream ois = new ObjectInputStream(new FileInputStream("teacher.txt"))) {
			Teacher t1 = (Teacher)ois.readObject();
			Teacher t2 = (Teacher)ois.readObject();
			Person p = (Person)ois.readObject();
			Teacher t3 = (Teacher)ois.readObject();
			
			System.out.println("t1 is " + t1.getName() + ", " + t1.getStudent().getName());
			System.out.println("t2 is " + t2.getName() + ", " + t2.getStudent().getName());
			System.out.println("p is " + p.getName() + ", " + p.getAge());
			System.out.println("t3 is " + t3.getName() + ", " + t3.getStudent().getName());
		}
	}

}
