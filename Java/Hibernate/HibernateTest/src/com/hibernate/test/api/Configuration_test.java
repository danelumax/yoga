package com.hibernate.test.api;

import org.hibernate.cfg.Configuration;
import org.junit.Test;

import com.hibernate.test.helloworld.User;
//详解Configuration对象
public class Configuration_test {
	@Test
	//Configuration 用户加载配置文件
	public void fun1(){
		//1.1 调用configure() 方法=> 加载src下名为hibernate.cfg.xml
		Configuration  conf = new Configuration().configure();
		//1.2 如果配置文件不符合默认加载规则.我们可以调用
			//new Configuration().configure(file); 通过file加载
			//new Configuration().configure(path);	通过路径加载
		//1.3 可以通过Configuration对象加载 映射文件(不推荐)
			//推荐hibernate.cfg.xml 使用 mapping 属性引入配置文件
		//规范: 1>orm映射文件名称与实体的简单类名一致
		//	   2>orm映射文件 需要与实体的类在同一包下
		conf.addClass(User.class);
	}
}
