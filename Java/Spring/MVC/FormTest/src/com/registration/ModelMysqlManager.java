package com.registration;

import java.util.ArrayList;
import java.util.List;

import org.springframework.ui.ModelMap;

public class ModelMysqlManager {
	private StudentDAOImpl studentDAOImpl;
	
	public StudentDAOImpl getStudentDAOImpl() {
		return this.studentDAOImpl;
	}

	public void setStudentDAOImpl(StudentDAOImpl studentDAOImpl) {
		this.studentDAOImpl = studentDAOImpl;
	}
	
	public Student getInitialStudent() {
		return this.studentDAOImpl.getStudent(1);
	}

	public void saveModeltoMysql(Student student) {
	    System.out.println("---- Save Web input into Mysql Database -----" );
	    this.studentDAOImpl.update(1, student.getAge());
	    this.studentDAOImpl.update(1, student.getName());
	}
	
	public void showView(ModelMap model) {
		System.out.println("---- Query Student from Mysql Database -----" );
		Student studentData = this.studentDAOImpl.getStudent(1);
		
		List<Student> list = new ArrayList<>();
		list.add(studentData);
		
		model.addAttribute("list", list); 
	}
	
	public List<Student> getStudentList() {
		Student studentData = this.studentDAOImpl.getStudent(1);
		
		List<Student> list = new ArrayList<>();
		list.add(studentData);
		
		return list;
	}
}
