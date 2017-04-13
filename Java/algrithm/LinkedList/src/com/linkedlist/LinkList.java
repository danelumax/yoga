package com.linkedlist;

import java.util.HashMap;
import java.util.Map;

/*
 * 链表，相当于火车
 * 
 * 提供方法：
 * 1.向前插入结点
 * 2.向后插入结点
 * 3.删除一个头结点
 * 4.删除一个尾结点
 * 5.列出链表所有结点
 * 6.查找一个指定结点
 * 7.删除一个指定结点
 * 8.得到链表长度
 */

public class LinkList {
	//头结点
	private Node head;
	
	public LinkList() {
		head = null;
	}
	
	/**
	 * 插入一个结点，在头结点后进行插入
	 */
	public void inserthead(int value) {
		Node node = new Node(value);
		//把head接到后面
		node.next = head;
		//head改指向
		head = node;
	}
	
	/**
	 * 插入一个结点，在尾结点后进行插入
	 */
	public void insert(int value) {
		Node node = new Node(value);
		Node current = head;
		if (head == null) {
			head = node;
			return;
		}
		while(current.next != null) {
			current = current.next;
		}
		current.next = node;
	}
	
	/**
	 * 删除一个结点，在头结点后进行删除
	 */
	public Node deletehead() {
		Node current = head;
		head = current.next;
		return current;
	}
	
	/**
	 * 删除一个结点，在尾结点后进行删除
	 */
	public void deleteEnd() {
		Node current = head;
		Node previous = head;
		
		while(current.next != null) {
			previous = current;
			current = current.next;
		}
		previous.next = null;
	}
		
	/**
	 * 显示方法
	 */
	public void ListAll() {
		Node current = head;
		//从head开始输出
		while(current != null) {
			current.display();
			current = current.next;
		}
		System.out.println();
	}
	
	/**
	 * 查找方法
	 */
	public Node find(long value) {
		Node current = head;
		while(current.data != value) {
			if(current.next == null) {
				return null;
			}
			current = current.next;
		}
		return current;
	}
	
	/**
	 * 删除方法，根据数据域来进行删除
	 */
	public Node delete(long value) {
		Node current = head;
		Node previous = head;
		//如果不相等，一直找
		while(current.data != value) {
			//如果找到最后一个了，那么说明没有
			if(current.next == null) {
				return null;
			}
			previous = current;
			current = current.next;
		}
		
		//如果找到了
		
		if(current == head) {
			//把后面一个当head
			head = head.next;
		} else {
			//直接跳过current
			previous.next = current.next;
		}
		
		return current;
	}
	
	public int Length() {
		int count = 0;
		Node current = head;
		//从head开始计算
		while(current != null) {
			count++;
			current = current.next;
		}
		
		return count;
	}
	
    public void removeDuplicates() {
        //Write your code here
          Node current = head;
          Node pre = current;
          Map<Integer, Integer> map = new HashMap<>();
          while(current != null) {
              if(map.containsKey(current.data)) {
                  pre.next = current.next;
              } else {
                  map.put(current.data, 1);
                  pre = current;
              }
              current = current.next;
          }
    }
}
