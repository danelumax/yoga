package com.sort;

public class QuickSort {

	public static void sort(int[] array, int left, int right) {
		if(left < right) {
			int i = Division(array, left, right);   //分割    找出第一个中心点 
			sort(array, left, i-1);     //将两部分分别排序
			sort(array, i+1, right);
		}
	}
	
	private static int Division(int[] array, int left, int right) {
		int base = array[left];    //基准元素
		while(left < right) { //这一轮，能以base作为中心，base左小于base，base右大于base
			while(left<right && array[right]>=base) {  //先做右边    一定要找到比base小的
				--right;     //右边找不到比base小的，往前找
			}
			if(left < right) {
				array[left] = array[right];  //有比base大的,前后互填
			}
			while(left<right && array[left]<=base ) {   //一定要找到比base大的
				++left;      //左边找不到比base大的，往后找
			}
			if(left < right) {
				array[right] = array[left];  //有比base小的,前后互填
			}
		}
		//left==right
		array[left] = base;//base 的最终位置
		return left;//把这个位置传出去，就能划分出两个区域
	}
	
	public static void main(String[] args) {
		int[] array = new int[] {9,8,7,6,5,4,3,2,1};
		QuickSort.sort(array, 0, array.length-1);
		for(int num : array) {
			System.out.print(num + " ");
		}
	}
}
	
