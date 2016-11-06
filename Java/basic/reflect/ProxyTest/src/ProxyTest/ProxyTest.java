package ProxyTest;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;

public class ProxyTest {

	public static void main(String[] args) 
		throws Exception {
		InvocationHandler handler = new MyInvokationHandler();
		Person p = (Person)Proxy.newProxyInstance(Person.class.getClassLoader(), 
				new Class[]{Person.class}, handler);
		p.walk();
		p.sayHello("Monkey");
	}

}
