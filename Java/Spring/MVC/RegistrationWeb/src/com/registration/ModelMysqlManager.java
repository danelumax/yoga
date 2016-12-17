package com.registration;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
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
	    
		Date date1 = new Date();
		String nowTime1 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(date1);
//		Thread.sleep(1000);
//		
//		Date date2 = new Date();
//		String nowTime2 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(date2);
//
//		Timestamp goodsC_date1 =Timestamp.valueOf(nowTime1);
//		Timestamp goodsC_date2 =Timestamp.valueOf(nowTime2);
//		long time = goodsC_date2.getTime() - goodsC_date1.getTime();
//		System.out.println(goodsC_date2.getTime() + " " + goodsC_date1.getTime() + " " + time);
		student.setTime(nowTime1);
	    
	    
	    this.studentDAOImpl.update(1, student.getName(), student.getAge(), student.getTime());
	}
	
	public void showView(ModelMap model) {
		System.out.println("---- Query Student from Mysql Database -----" );
		List<Student> list = this.studentDAOImpl.listStudents();
		model.addAttribute("list", list); 
	}
	
	public List<Student> getStudentList() {
		return this.studentDAOImpl.listStudents();
	}
	
	public void deleteTimeoutDate() {
		
	}
}
