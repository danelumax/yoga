package com.collection;

import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

public class JavaCollection {
	List<BeanParent> addressList;
	Set<String> addressSet;
	Map<Integer, String> addressMap;
	Properties addressProp;
	
	public void setAddressList(List<BeanParent> addressList) {
		this.addressList = addressList;
	}
	public List<BeanParent> getAddressList() {
		return this.addressList;
	}
	
	public void setAddressSet(Set<String> addressSet) {
		this.addressSet = addressSet;
	}
	public Set<String> getAddressSet() {
		return this.addressSet;
	}
	
	public void setAddressMap(Map<Integer, String> addressMap) {
		this.addressMap = addressMap;
	}
	public Map<Integer, String> getAddressMap() {
		return this.addressMap;
	}
	
	public void setAddressProp(Properties addressProp) {
		this.addressProp = addressProp;
	}
	public Properties getAddressProp() {
		return this.addressProp;
	}
}
