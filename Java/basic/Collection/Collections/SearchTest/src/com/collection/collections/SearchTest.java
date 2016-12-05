package com.collection.collections;

import java.util.ArrayList;
import java.util.Collections;

public class SearchTest {

	public static void main(String[] args) throws Exception {
		ArrayList<Integer> nums = new ArrayList<>();
		nums.add(2);
		nums.add(-5);
		nums.add(6);
		nums.add(0);
		System.out.println("Initial: " + nums);
		
		System.out.println("Max: " + Collections.max(nums));
		
		System.out.println("Min: " + Collections.min(nums));
		
		Collections.replaceAll(nums, 0, 1);
		System.out.println("After replace 0 to 1: " + nums);
		
		System.out.println("Get -5 Frequency: " + Collections.frequency(nums, -5));
		
		Collections.sort(nums);
		System.out.println("Using Binary Search to get the index of value 6: " + Collections.binarySearch(nums, 6));
	}
}
