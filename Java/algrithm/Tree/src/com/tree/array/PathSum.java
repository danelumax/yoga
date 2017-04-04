package com.tree.array;

import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

public class PathSum {

	private class Node {
		public Node left;
		public Node right;
		public int value;
	}
	
    private List<List<Integer>> resultList = new ArrayList<>();
    
    public void pathSumInner(Node root, int sum, Stack<Integer>path) {
    	
        path.push(root.value);
        if(root.left == null && root.right == null) {
        	if(sum == root.value) {
        		resultList.add(new ArrayList<Integer>(path));
        	}
        }
        if(root.left != null) {
        	pathSumInner(root.left, sum - root.value, path);
        }
        if(root.right != null) {
        	pathSumInner(root.right, sum - root.value, path);
        }
        path.pop();
    }
    
    public List<List<Integer>> findPath(Node rootNode, int sum) {
    	
        if(rootNode == null) {
        	return resultList;
        }
        Stack<Integer> path = new Stack<Integer>();
        pathSumInner(rootNode, sum, path);
        return resultList;
    }
}
