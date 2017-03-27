package com.spring.aop.exception.aspect;

import org.aspectj.lang.JoinPoint;
import org.springframework.stereotype.Component;

/*
 * 如果要在xml或context代码中使用bean id，那么@Component必须标明bean id，而且大小写要一致
 */
@Component("exceptionAspect")
public class ExceptionAspect {

	public void throwingException(JoinPoint joinPoint, Throwable ex) {
		System.out.println(ex.getMessage());
	}
}
