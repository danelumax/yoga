package com.Mybatis.Mapper;

import java.util.List;

import com.pojo.Orders;
import com.pojo.OrdersCustom;
import com.pojo.User;

public interface OrdersMapperCustom {
	
	//查询订单关联查询用户信息
	public List<OrdersCustom> findOrdersUser()throws Exception;
	
}
