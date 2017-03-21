package com.sort;

public class BubbleSort {

	/*
	 *  冒泡法像海浪一样，把最小的那个数，推到岸上。
	 *  i就是海岸，随着i后移，海岸不断往后移。
	 *   i的左边是已经排序完毕的子数组。
	 */
	public static void sort(int[] array) {
		
		int temp = 0;
		boolean flag = false;
		
		/*
		 * 为什么i的最后一个位置是array.length-2?
		 * 因为最后一次比较是array.length-2 与 array.length-1之间的，如果i的最后一个是array.length-1， 就不需要比较了
		 */
		for(int i=0; i<array.length-1; i++) {
			/*
			 * 为什么j>i?
			 * j的移动边界就是i， 潮水不会上岸
			 */
			for(int j=array.length-1; j>i; j--) {
				if (array[j-1] > array[j]) {
					temp = array[j-1];
					array[j-1] = array[j];
					array[j] = temp;
					flag =true;
				}
			}
			if (flag == true) {
				flag = false;
			}
			else {
				//如果一轮中，没有任何需要交换，说明排序已经结束
				break;
			}
		}
	}
	
	public static void main(String[] args) {
		
		int[] array = new int[] {9,8,7,6,5,4,3,2,1};
		BubbleSort.sort(array);
		for(int i=0; i<array.length; i++) {
			System.out.print(array[i] + " ");
		}
	}
}
