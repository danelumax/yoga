package com.tree;

/*
 *                     10
 *                3          20
 *                   4    15     90
 */

public class TestTree {
	public static void main(String[] args) {
		Tree tree = new Tree();
		tree.insert(10);
		tree.insert(20);
		tree.insert(15);
		tree.insert(3);
		tree.insert(4);
		tree.insert(90);
		
//		Node node = tree.find(3);
//		System.out.println(node.data + ", " + node.sData);
		
//		tree.frontOrder(tree.root);   // 10 3 4 20 15 90
		
//		tree.inOrder(tree.root);      // 3 4 10 15 20 90
//		tree.afterOrder(tree.root);   // 4 3 15 90 20 10
		//tree.delete(90);
		//tree.inOrder(tree.root);
		//tree.postorderTraversal(tree.root);
		tree.inTraverse(tree.root);
	}
}
