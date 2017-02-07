package com.ajax.servlet;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ServletDemo2 extends HttpServlet {
	private String usernames[] = {"admin","wzhting"};

	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		String username = request.getParameter("username");
		boolean b = false;//是否可用
		for(String s:usernames){
			if(s.equals(username)){
				b = true;
				break;
			}
		}
		
		response.setContentType("text/html;charset=UTF-8");
		if(b){
			response.getWriter().write("<font color='red'>用户名不可用</font>");
		}else{
			response.getWriter().write("<font color='green'>用户可用</font>");
		}
		
	}

	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);
	}

}
