package com.linkedlist;

public class TestLinkList {
	public static void main(String[] args) {
		LinkList linkList = new LinkList();
		// 1. 向链表中插入数据
		linkList.insert(34);
		linkList.insert(23);
		linkList.insert(23);
		linkList.insert(12);
		linkList.insert(0);
		linkList.insert(-1);
		linkList.ListAll();   //34 23 23 12 0 -1 
		
		linkList.removeDuplicates();
		linkList.ListAll();   //34 23 12 0 -1 
		
//		// 2. 显示链表长度
//		System.out.println("Link list length : " + linkList.Length());
//		
//		// 3. 删除最后一个结点
//		linkList.deleteEnd();
//		linkList.ListAll();
//		
//		// 4. 查找指定结点
//		Node node = linkList.find(23);
//		node.display();
//		System.out.println();
//		
//		// 4. 删除指定结点
//		node = linkList.delete(0);
//		node.display();
	}
}
