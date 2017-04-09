package com.tree;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Stack;

/*
 * 二叉树类
 */
public class Tree {
	//根节点
	public Node root;
	
	/**
	 * 插入节点
	 * 1. 如果root为空，插入节点就是root
	 * 2. parent作为头，current不断地下探
	 * 		不断查看插入的value与current的大小
	 * 			如果value小，往左走；
	 * 			如果value大，往右走；
	 * 		一旦那个方向为null，说明到底了，就往那个方向插入即可
	 */
	public void insert(long value) {
		//封装节点
		Node newNode = new Node(value);
		//引用当前节点
		Node current = root;
		//引用父节点
		Node parent = root;
		//如果root为null，也就是第一插入的时候
		if(root == null) {
			root = newNode;
			return;
		} else {
			while(true) {
				//父节点指向当前节点
				parent = current;
				//如果当前指向的节点数据比插入的要大,则向左子树寻找
				if(value < current.data) {
					current = current.leftChild;
					//如果左子树为空，找不下去了，到点了
					if(current == null) {
						//直接插入
						parent.leftChild = newNode;
						return;
					}
				} else {
					//向右子树寻找
					current = current.rightChild;
					//如果右子树为空，找不下去了，到点了
					if(current == null) {
						//直接插入
						parent.rightChild = newNode;
						return;
					}
				}
			}
		}
	}
	
	/**
	 * 查找节点
	 * 1. 用current代理root，从头开始
	 * 2. 只要没找到，那就一直找
	 * 		如果value小，那就往左找
	 * 		如果value大，那就往右找
	 * 3. 找到了，跳出while，返回节点
	 */
	public Node find(long value) {
		//引用当前节点，从根节点开始
		Node current = root;
		//循环，只要查找值不等于当前节点的数据项
		while(current.data != value) {
			//进行比较，比较查找值和当前节点的大小
			if(value < current.data) {
				current = current.leftChild;
			} else {
				current = current.rightChild;
			}
			//如果查找不到
			if(current == null) {
				return null;
			}
		}
		return current;
	}
	
	/**
	 * 删除节点
	 * 先查找节点
	 * 1. 用current代理root，从头开始
	 * 2. parent作为头，current不断地下探
	 * 3. 只要没找到，那就一直找
	 * 		如果value小，那就往左找，并暂时认定该节点是左节点
	 * 		如果value大，那就往右找，并暂时认定该节点不是左节点
	 * 4. 找到了，跳出while，返回节点
	 * 
	 * 然后是删除部分
	 * 三种情况：
	 * 1. 该节点是叶子节点
	 * 2. 该节点有一个子节点
	 * 3. 该节点有两个子节点
	 * 
	 * 1. 该节点是叶子节点（左右子节点都是null）
	 * 	1> 判断是左节点，还是右节点
	 *  2> 然后直接用parent，把节点设置为null，一了百了
	 *  
	 * 2. 该节点有一个子节点
	 * 	1> 如果该节点只有左节点（右节点为空）
	 * 		1） 如果是root，直接把左子节点作为root
	 * 		2） 如果该节点是父节点的左节点，那么该节点的左节点直接就是父节点的左节点（因为肯定比父节点小）
	 * 		3） 如果该节点是父节点的右节点，那么该节点的左节点直接就是父节点的右节点（因为肯定比父节点大）
	 * 	2> 如果该节点只有右节点（左节点为空）
	 * 		1） 如果是root，直接把右子节点作为root
	 * 		2） 如果该节点是父节点的左节点，那么该节点的右节点直接就是父节点的左节点（因为肯定比父节点小）
	 * 		3） 如果该节点是父节点的右节点，那么该节点的右节点直接就是父节点的右节点（因为肯定比父节点大）
	 * 
	 * 3. 该节点有两个子节点
	 * 	1> 调整一下，获得一个该位置的新节点
	 * 	2> 如果这个要删除的节点是root，那么新节点作为root
	 * 	3> 如果这个要删除的节点是左子节点，那么parent用新节点作为新的左子节点
	 * 	4> 如果这个要删除的节点是右子节点，那么parent用新节点作为新的右子节点
	 * 
	 */
	public boolean delete(long value) {
		//引用当前节点，从根节点开始
		Node current = root;
		
		//应用当前节点的父节点
		Node parent = root;
		//是否为左节点
		boolean isLeftChild = true;
		
		while(current.data != value) {
			parent = current;
			//进行比较，比较查找值和当前节点的大小
			if(current.data > value) {
				current = current.leftChild;
				isLeftChild = true;
			} else {
				current = current.rightChild;
				isLeftChild = false;
			}
			//如果查找不到
			if(current == null) {
				return false;
			}
		}
		
		//删除叶子节点，也就是该节点没有子节点
		if(current.leftChild == null && current.rightChild == null) {
			if(current == root) {
				root = null;
			} else if(isLeftChild) {
				parent.leftChild = null;
			} else {
				parent.rightChild = null;
			}
		} else if(current.rightChild == null) { //该节点只有左节点
			if(current == root) {
				root = current.leftChild;
			}else if(isLeftChild) {
				parent.leftChild = current.leftChild;
			} else {
				parent.rightChild = current.leftChild;
			}
		} else if(current.leftChild == null) {  //该节点只有右节点
			if(current == root) {
				root = current.rightChild;
			} else if(isLeftChild) {
				parent.leftChild = current.rightChild;
			} else {
				parent.rightChild = current.rightChild;
			}
		} else {
			Node successor = getSuccessor(current);
			if(current == root) {
				root = successor;
			} else if(isLeftChild) {
				parent.leftChild = successor;
			} else{
				parent.rightChild = successor;
			}
			successor.leftChild = current.leftChild;
		}
		
		return true;
		
		
	}
	
	/*
	 *  1. 从右子节点入手
	 *  2. 从第一个的右子节点开始， 不断下探左子节点，直到找不到左子树（那个节点可以有右节点）
		      保证比左子树大， 比右子树小，并且比右子树的左子树也都要小
	 *	3. 如果不是第一次拿到的右子节点（右子节点有左子树）
	 *		1> 托付右子节点，再是右，也比父节点小
	 *		2> 托付老右子节点给新节点
	 */ 
	public Node getSuccessor(Node delNode) {
		Node successor = delNode;
		Node successorParent = delNode;
		//从右子节点入手
		Node current = delNode.rightChild;
		
		//从第一个的右子节点开始， 不断下探左子节点，直到找不到左子树（那个节点可以有右节点）
		//保证比左子树大， 比右子树小，并且比右子树的左子树也都要小
		while(current != null) {
			successorParent = successor;
			successor = current;
			current = current.leftChild;
		}
		
		//如果不是第一次拿到的右子节点（右子节点有左子树）
		if(successor != delNode.rightChild) {
			//托付右子节点，再是右，也比父节点小
			successorParent.leftChild = successor.rightChild;
			//托付老右子节点给新节点
			successor.rightChild = delNode.rightChild;
		}
		return successor;
	}
	
	/**
	 * 前序遍历
	 */
	public void frontOrder(Node localNode) {
		if(localNode != null) {
			//访问根节点
			System.out.println(localNode.data);
			//前序遍历左子树
			frontOrder(localNode.leftChild);
			//前序遍历右子树
			frontOrder(localNode.rightChild);
		}
	}
	
	/**
	 * 中序遍历
	 */
	public void inOrder(Node localNode) {
		if(localNode != null) {
			//中序遍历左子树
			inOrder(localNode.leftChild);
			//访问根节点
			System.out.println(localNode.data);
			//中旬遍历右子树
			inOrder(localNode.rightChild);
		}
	}
	
	/**
	 * 后序遍历
	 */
	public void afterOrder(Node localNode) {
		if(localNode != null) {
			//后序遍历左子树
			afterOrder(localNode.leftChild);
			//后序遍历右子树
			afterOrder(localNode.rightChild);
			//访问根节点
			System.out.println(localNode.data);
		}
	}
	
	
	
	
	
	/**
	 * 先序遍历（非递归）
	 */
    public void postorderTraversal(Node root) {
        Stack<Node> s = new Stack<>();
        Node current = root;
        
	    while (current!=null || !s.isEmpty())
	    {
	        if (current != null)
	        {
	        	System.out.println(current.data);
	            s.push(current);
	            current = current.leftChild;
	        } else {
	            Node node = s.pop();
	            current = node.rightChild;
	        }
	    }
    }
	
	/**
	 * 中序遍历（非递归）
	 */
	public void inTraverse(Node root) {
		Stack<Node> s = new Stack<>();
		Node current = root;
		
		while(current!=null || !s.isEmpty()) {
			if (current != null) {
				s.push(current);
				current = current.leftChild;
			} else {
				current = s.pop();
				System.out.println(current.data);
				//中间get到了，开始考虑往右边走了
				current = current.rightChild;
			}
		}
	}
	
	/**
	 * 后序遍历（非递归）
	 */
	public void afterTraverse(Node root) {
		Stack<Node> s = new Stack<>();
		Node current = root;
		// pre 标记最近出栈的节点，用于判断是否是 current 节点的右孩子，如果是的话，就可以访问 current 节点
		Node pre = current;
		//isNeedPush 标记是出栈还是继续将左孩子进栈
		boolean isNeedPush = true;
		
		while(current != null || !s.isEmpty()) {
			if (current != null && isNeedPush) {
				s.push(current);
				current = current.leftChild;
			} else {
				if (s.isEmpty()) {
					return;
				}
				current = s.peek();
				if (current.rightChild!=null && current.rightChild != pre) {
					current = current.rightChild;
					isNeedPush = true;
				} else {
					current = s.pop();
					System.out.println(current.data);
					isNeedPush = false;
					pre = current;
				}
			}
		}
	}
	
	/*
	 * 获取高度
	 */
	public int getDepth(Node node) {
        if (node == null) {  
            return 0;  
        } else {
        	int result = 0;
            int leftDepth = getDepth(node.leftChild);  
            int rightDepth = getDepth(node.rightChild);
            if (leftDepth < rightDepth) {
            	result = rightDepth + 1;
            } else {
            	result = leftDepth + 1;
            }
            return result;
        }  
	}
	
    // 层次遍历  
    public void levelOrder(Node node) {  
        if (node == null) {
            return;  
        }
        Deque<Node> queue = new ArrayDeque<Node>();  
        queue.add(node);  
        while (!queue.isEmpty()) {  
            Node outNode = queue.pop();  
            System.out.println(outNode.data);  
            if (outNode.leftChild != null) {
                queue.add(outNode.leftChild); 
            }
            if (outNode.rightChild != null) { 
                queue.add(outNode.rightChild);
            }
        }  
    }  
}
