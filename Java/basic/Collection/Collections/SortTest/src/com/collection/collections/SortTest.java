package com.collection.collections;

import java.util.ArrayList;
import java.util.Collections;

public class SortTest {

	public static void main(String[] args) {
		ArrayList<Integer> nums = new ArrayList<>();
		nums.add(2);
		nums.add(-5);
		nums.add(3);
		nums.add(0);
		System.out.println("Initial:\t" + nums);

		Collections.reverse(nums);
		System.out.println("After Reverse:\t" + nums);
		
		Collections.sort(nums);
		System.out.println("After Sort:\t" + nums);
		
		Collections.shuffle(nums);
		System.out.println("After Shuffle:\t" + nums);
	}
}
