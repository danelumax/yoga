package com.zhenti.factorial;

public class Factorial {

	public static long fac(int n) {
		if (n > 1) {
			return (n* fac(n-1));
		} else {
			return 1;
		}
	}
	
	public static void main(String[] args) {
		System.out.println(Factorial.fac(6));
	}

}
