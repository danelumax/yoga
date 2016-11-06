package ProxyTest;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class MyInvokationHandler implements InvocationHandler {
	public Object invoke(Object Proxy, Method method, Object[] args) {
		System.out.println("----Running way: " + method);
		if (args != null) {
			System.out.println("Input Parameters:");
			for(Object val : args) {
				System.out.println(val);
			}
		} else {
			System.out.println("No Parameter");
		}
		return null;
	}
}
