package com.ajax.pojo;

import java.util.ArrayList;
import java.util.List;

import com.thoughtworks.xstream.annotations.XStreamAlias;
import com.thoughtworks.xstream.annotations.XStreamAsAttribute;
import com.thoughtworks.xstream.annotations.XStreamImplicit;
import com.thoughtworks.xstream.annotations.XStreamOmitField;
@XStreamAlias("province")
public class Province {
	@XStreamAsAttribute
	private int code;// 10 37 42 41
	@XStreamAsAttribute
	private String name;
	
	
	public Province(){}
	
	public Province(int code, String name) {
		super();
		this.code = code;
		this.name = name;
	}
	@XStreamImplicit(itemFieldName="city")
	private List<City> citys = new ArrayList<City>();

	public int getCode() {
		return code;
	}

	public void setCode(int code) {
		this.code = code;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public List<City> getCitys() {
		return citys;
	}

	public void setCitys(List<City> citys) {
		this.citys = citys;
	}
	
}
