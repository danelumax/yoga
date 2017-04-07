package com.sort;

public class HeapSort {

	public static void HeapAdjust(int[] array, int root, int end) {
		int tmp = 0;
		int i = 0;
		//不管从哪一个子树的root开始，只要在边界范围内，还有左节点，就比较
		while (2 * root + 1 < end) {
			//移动到左节点
			i = 2 * root + 1;
			//如果有右节点
			if ((i+1) < end) {
				//左右比较，谁大，谁来做代表，和root比较
				if (array[i] < array[i+1]) {
					//右节点是代表
					i++;
				}
			}
			if (array[root] < array[i]) {
				tmp = array[i];
				array[i] = array[root];
				array[root] = tmp;
				//root下沉
				root = i;
			} else { //如果root最大，那么这个root的调整就结束了
				break;
			}
		}
	}
	
	public static void sort(int[] array) {
		int tmp = 0;
		//从最后一个子树的root开始，自下而上，调整为大根堆
		for (int i=array.length/2-1; i>=0; i--) {
			HeapAdjust(array, i, array.length);
		}
		//第一个大根堆构建成功
		
		//最大的数，一个个拿掉，大根堆慢慢变小
		for (int i=array.length-1; i>0; i--) {
			tmp = array[0];
			array[0] = array[i];
			array[i] = tmp;
			//从头开始调整堆，并且堆在慢慢变小，i是堆的边界
			HeapAdjust(array, 0, i);
		}
	}
	
	public static void main(String[] args) {
		int[] array = new int[] {9,8,7,6,5,4,3,2,1};
		HeapSort.sort(array);
		for (int i=0; i<array.length; i++) {
			System.out.print(array[i] + " ");
		}
	}
}
