package com.sort;

public class ShellSort {

	public static void sort(int[] array) {
		int i = 0;
		int j = 0;
		int tmp = 0;
		int d = array.length/2;
		while (d >= 1) {
			for(i=d; i<array.length; i++) {
				tmp = array[i];
				for(j=i-d; j>=0 && tmp<array[j]; j-=d) {
					array[j+d] = array[j];
				}
				array[j+d] = tmp;
			}
			d /= 2;
		}
		
	}
	
	public static void main(String[] args) {
		int[] array = new int[] {9,8,7,6,5,4,3,2,1};
		ShellSort.sort(array);
		for(int i=0; i<array.length; i++) {
			System.out.print(array[i] + " ");
		}
	}
}
