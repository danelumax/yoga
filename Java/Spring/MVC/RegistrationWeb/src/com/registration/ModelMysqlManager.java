package com.registration;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
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
		return new Student();
	}

	public void saveModeltoMysql(Student student) {
	    System.out.println("---- Save Web input into Mysql Database -----" );
	    
		Date date1 = new Date();
		String nowTime1 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(date1);
		student.setTime(nowTime1);
	    
	    this.studentDAOImpl.insert(student.getName(), student.getAge(), student.getTime());
	}
	
	public void showView(ModelMap model) {
		System.out.println("---- Query Student from Mysql Database -----" );
		List<Student> list = this.studentDAOImpl.listStudents();
		model.addAttribute("list", deleteTimeoutStudent(list)); 
	}
	
	public List<Student> getStudentList() {
		return this.studentDAOImpl.listStudents();
	}
	
	public List<Student> deleteTimeoutStudent(List<Student> students) {
		Iterator<Student> it = students.iterator();
		while(it.hasNext()) {
			Student tmpStudent = (Student)it.next();
			if(TimeUtils.isTimeout(tmpStudent.getTime())) {
				System.out.println(tmpStudent.getName() + " is timeout!");
				this.studentDAOImpl.delete(tmpStudent.getId());
				it.remove();
				tmpStudent = null;
			} else {
				String leaseTime = TimeUtils.getFormatLeaseTime(tmpStudent.getTime());
				tmpStudent.setLeaseTime(leaseTime);
			}
		}
		
		return students;
	}
}
