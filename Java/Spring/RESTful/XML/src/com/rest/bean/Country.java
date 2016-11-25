package com.rest.bean;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement(name="country")
public class Country{
	
	private int id;
	private String countryName;	

	public Country() {
	}
	public Country(int i, String countryName) {
		this.id = i;
		this.countryName = countryName;
	}
	
	@XmlElement
	public int getId() {
		return this.id;
	}
	public void setId(int id) {
		this.id = id;
	}
	
	@XmlElement
	public String getCountryName() {
		return this.countryName;
	}
	public void setCountryName(String countryName) {
		this.countryName = countryName;
	}		
}