package com.sort;

public class InsertSort {

	public static void sort(int[] array) {
		int tmp = 0;
		int i=0;
		int j=0;
		for (i=1; i<array.length; i++) {
			tmp = array[i];
			for (j=i-1; j>=0 && tmp < array[j]; j--) {
				array[j+1] = array[j];
			}
			array[j+1] = tmp;
		}
	}
	
	public static void main(String[] args) {
		int[] array = new int[] {9,8,7,6,5,4,3,2,1};
		InsertSort.sort(array);
		for (int i=0; i<array.length; i++) {
			System.out.print(array[i] + " ");
		}
	}
}
