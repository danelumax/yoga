package com.ajax.servlet;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.ajax.pojo.City;
import com.ajax.pojo.Province;
import com.thoughtworks.xstream.XStream;

public class ServletDemo4 extends HttpServlet {

	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		List<Province> provinces = new ArrayList<Province>();
		Province sd = new Province(37, "山东省");
		Province hb = new Province(42, "湖北省");
		Province hn = new Province(41, "河南省");
		
		sd.getCitys().add(new City(01, "济南市"));
		sd.getCitys().add(new City(02, "青岛市"));
		sd.getCitys().add(new City(03, "淄博市"));
		
		hb.getCitys().add(new City(01, "武汉市"));
		hb.getCitys().add(new City(02, "黄冈市"));
		hb.getCitys().add(new City(03, "襄阳市"));
		
		hn.getCitys().add(new City(01, "郑州市"));
		hn.getCitys().add(new City(02, "开封市"));
		hn.getCitys().add(new City(03, "洛阳市"));
		
		provinces.add(sd);
		provinces.add(hb);
		provinces.add(hn);
		
		XStream xs = new XStream();
		xs.autodetectAnnotations(true);//使用注解生成别名
		xs.alias("provinces", List.class);
		String xml = xs.toXML(provinces);
		
		//输出xml文件
		response.setContentType("text/xml;charset=UTF-8");
		response.getWriter().write(xml);
	}

	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);
	}

}
