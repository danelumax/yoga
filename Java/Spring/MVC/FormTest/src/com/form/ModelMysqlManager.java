package com.form;

import org.springframework.ui.ModelMap;

public class ModelMysqlManager {
	private StudentDAOImpl studentDAOImpl;
	
	public StudentDAOImpl getStudentDAOImpl() {
		return this.studentDAOImpl;
	}

	public void setStudentDAOImpl(StudentDAOImpl studentDAOImpl) {
		this.studentDAOImpl = studentDAOImpl;
	}

	public void saveModeltoMysql(Student student) {
	    System.out.println("---- Save Web input into Mysql Database -----" );
	    this.studentDAOImpl.update(1, student.getAge());
	    this.studentDAOImpl.update(1, student.getName());
	}
	
	public void showView(ModelMap model) {
		System.out.println("---- Query Student from Mysql Database -----" );
		Student studentData = this.studentDAOImpl.getStudent(1);
		
		model.addAttribute("name", "Liwei: " + studentData.getName());
		model.addAttribute("age", studentData.getAge());
		model.addAttribute("id", studentData.getId());  
	}
}
