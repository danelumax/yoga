package com.tree.array;

import java.util.ArrayList;
import java.util.List;


public class ArrayTree {

	private class Node {  
		
		public Node leftChild;  
		public Node rightChild;  
		public int data;  
		
		public Node(int data) {  
			this.data = data;  
		}  
	}  
	
	private int[] array;
	private static List<Node> nodeLIst = new ArrayList<>();  
	
	public ArrayTree(int[] array) {
		this.array = array;
	}
	
    public void createBintree() {
        for (int i = 0; i < array.length; i++) {  
        	if (array[i] != -1) {
        		nodeLIst.add(new Node(array[i]));
        	} else {
        		nodeLIst.add(null);
        	}
        }  
  
        if (nodeLIst.size() > 0) {  
            for (int i = 0; i<=array.length / 2 - 1; i++) {
            	if (null != nodeLIst.get(i)) {
	                //leftChild  
	                if ((2 * i + 1) < array.length && null != nodeLIst.get(2 * i + 1)) {  
	                    nodeLIst.get(i).leftChild = nodeLIst.get(2 * i + 1);  
	                }  
	                //rightChild  
	                if ((2 * i + 2) < array.length && null != nodeLIst.get(2 * i + 2)) {  
	                    nodeLIst.get(i).rightChild = nodeLIst.get(2 * i + 2);  
	                }  
            	}
            }
        }  
    }  
  
    /** 
     * 先序遍历 
     * 
     * @param node 
     */  
    public static void preOrderTraver(Node node) {  
        if (null != node) {  
        	System.out.println("node:" + node.data);  
            preOrderTraver(node.leftChild);  
            preOrderTraver(node.rightChild);  
        } else {  
            return;  
        }  
    }  
  
    public static void main(String[] args) {  
    	
    	// -1 : null node
    	int[] array = {1, 2, 3, 4, -1, 6, 7, 8, 9, 10};
    	ArrayTree tree = new ArrayTree(array);  
        tree.createBintree();  
        preOrderTraver(nodeLIst.get(0));  
    }  
	
}
