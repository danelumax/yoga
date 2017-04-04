package com.tree.array;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class Test {

	private class Node {  
		
		public Node left;  
		public Node right;  
		public int value;  
		
		public Node(int value) {  
			this.value = value;  
		}  
	}  
	
	private int[] array;
	private static List<Node> nodeLIst = new ArrayList<>();
	private boolean isFinished = false;
	private List<String> resultList;
	
	public Test(int[] array) {
		this.array = array;
	}
	
    public void pathSumInner(Node node, int sum, List<String> record) {
    	//ensure just print one result
    	if(isFinished) {
    		return;
    	}
    	
    	record.add("Node:" + node.value);
        if(node.left == null && node.right == null) {
        	if(sum == node.value) {
        		resultList = new ArrayList<String>(record);
        		isFinished = true;
        	}
        }
        //DFS
        if(node.left != null) {
        	pathSumInner(node.left, (sum - node.value), record);
        }
        if(node.right != null) {
        	pathSumInner(node.right, (sum - node.value), record);
        }
        //if this node and its children are not match sum, remove this node in the record
        record.remove(record.size()-1);
    }
    
    public List<String> findPath(Node rootNode, int sum) {
    	
        if(rootNode == null) {
        	return resultList;
        }
        List<String> record = new ArrayList<>();
        pathSumInner(rootNode, sum, record);
        return resultList;
    }
	
//    public void createBintree() {
//        for (int i = 0; i < array.length; i++) {  
//        	if (array[i] != -1) {
//        		nodeLIst.add(new Node(array[i]));
//        	} else {
//        		nodeLIst.add(null);
//        	}
//        }  
//  
//        if (nodeLIst.size() > 0) {  
//            for (int i = 0; i<=array.length / 2 - 1; i++) {
//            	if (null != nodeLIst.get(i)) {
//	                //left  
//	                if ((2 * i + 1) < array.length && null != nodeLIst.get(2 * i + 1)) {  
//	                    nodeLIst.get(i).left = nodeLIst.get(2 * i + 1);  
//	                }  
//	                //right  
//	                if ((2 * i + 2) < array.length && null != nodeLIst.get(2 * i + 2)) {  
//	                    nodeLIst.get(i).right = nodeLIst.get(2 * i + 2);  
//	                }  
//            	}
//            }
//        }  
//    } 
    
    
    public void createBintree() throws InterruptedException {
    	
    	//array to List
    	for (int i = 0; i < array.length; i++) {  
    		if (array[i] != 65535) {
    			nodeLIst.add(new Node(array[i]));
    		} else {
    			nodeLIst.add(null);
    		}
    	}  
    	int index = 0;
    	BlockingQueue<Node> queue = new ArrayBlockingQueue<Node>(10);
    	//like BFS
    	queue.put(nodeLIst.get(index++));
    	while(!queue.isEmpty() && index < nodeLIst.size()) {
    		Node node = queue.take();
    		if(null != nodeLIst.get(index)) {
    			node.left = nodeLIst.get(index++);
    			queue.put(node.left);
    		} else {
    			//if current node is null, just skip
    			index++;
    		}
    		if(null != nodeLIst.get(index)) {
    			node.right = nodeLIst.get(index++);
    			queue.put(node.right);
    		} else {
    			//if current node is null, just skip
    			index++;
    		}
    	}
    }
  
    public static void main(String[] args) throws InterruptedException {  
    	
    	// 65535 : null node
    	int nullNode = 65535;
    	int[] array = {5, -2, -3, nullNode, 1, 5, 9, 10, nullNode, 8, nullNode, 4, 4};
    	int sum  = 15;
    	Test tree = new Test(array);  
        tree.createBintree();  
        //find from root
        List<String> list = tree.findPath(nodeLIst.get(0), sum);
        System.out.print(list.toString());
    }  
}
