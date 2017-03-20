package com.sort;

public class SelectSort {

	/*
	 * 每次以array[i]为基准，从i后面找出一个最小的，并记住下标min。
	 * 把这个最小的直接和array[i]交换
	 * 保证前i个子数组都是排序好的
	 */
	public static void sort(int[] array) {
		
		int min = 0;
		int temp = 0;
		/*
		 * 为什么i<array.length-1
		 * 因为最后一遍时，从倒数2个数字中找出一个小的，那么剩下来的就是最大的，所以不需要再进行选择了
		 */
		for (int i=0; i<array.length-1; i++) {
			min = i;
			for (int j=i+1; j<array.length; j++) {
				if (array[min] > array[j]) {
					//永远指向最小的那个下标
					min = j;
				}
			}
			//min与i交换
			temp = array[i];
			array[i] = array[min];
			array[min] = temp;
		}
	}
	
	public static void main(String[] args) {
		
		int[] array = new int[] {9,8,7,6,5,4,3,2,1};
		SelectSort.sort(array);
		for(int i=0; i<array.length; i++) {
			System.out.print(array[i] + " ");
		}
	}
}
