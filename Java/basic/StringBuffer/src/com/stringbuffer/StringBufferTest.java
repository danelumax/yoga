package com.stringbuffer;
/*
如果需要频繁修改字符串 的内容，建议使用字符串缓冲 类（StringBuffer）。


StringBuffer 其实就是一个存储字符 的容器。

笔试题目：使用Stringbuffer无 参的构造函数创建 一个对象时，默认的初始容量是多少？ 如果长度不够使用了，自动增长多少倍？
	StringBuffer 底层是依赖了一个字符数组才能存储字符数据 的，该字符串数组默认 的初始容量是16， 如果字符数组的长度不够使用 死，自动增长1倍。


StringBuffer 是一个存储字符的容器 

容器的具备 的行为
	
	String 
	
	增加
		append(boolean b)    可以添加任意类型 的数据到容器中
		insert(int offset, boolean b)  指定插入的索引值，插入对应 的内容。 

	删除
		delete(int start, int end)  根据指定的开始与结束的索引值删除对应的内容。
		deleteCharAt(int index)   根据指定 的索引值删除一个字符。
	
	
	修改
	
		replace(int start, int end, String str) 根据指定 的开始与结束索引值替代成指定的内容。
		reverse()   翻转字符串缓冲类的内容。  abc--->cba
		
        setCharAt(int index, char ch)  把指定索引值的字符替换指定的字符。 
        substring(int start, int end)  根据指定的索引值截取子串。
		ensureCapacity(int minimumCapacity)  指定StringBuffer内部的字符数组长度的。
		
	查看
		indexOf(String str, int fromIndex) 查找指定的字符串第一次出现的索引值,并且指定开始查找的位置。
		lastIndexOf(String str) 
		
		capacity() 查看当前字符数组的长度。 
		length() 
		
		charAt(int index) 
		toString()   把字符串缓冲类的内容转成字符串返回。
		

StringBuffer 与 StringBuilder的相同处与不同处：
	
	相同点：
		1. 两个类都是字符串缓冲类。
		2. 两个类的方法都是一致的。
	不同点：
		1. StringBuffer是线程安全的,操作效率低 ，StringBuilder是线程非安全的,操作效率高。
		2. StringBuffer是jdk1.0出现 的，StringBuilder 是jdk1.5的时候出现的。
		
推荐使用： StringBuilder，因为操作效率高。
		


		
		
		
		
*/

public class StringBufferTest {
	
	public static void main(String[] args) {
		//先使用StringBuffer无参的构造函数创建一个字符串缓冲类。
		StringBuffer sb = new StringBuffer(); 
		sb.append("abcjavaabc");
		/*
		添加 
		sb.append(true);
		sb.append(3.14f);
		插入
		
		sb.insert(2, "小明");
		*/
		
		/*
		删除
		sb.delete(2, 4); //  删除的时候也是包头不包尾
		sb.deleteCharAt(3); //根据指定 的索引值删除一个字符
		
		修改	
		sb.replace(2, 4, "陈小狗");
		
		sb.reverse(); // 翻转字符串的内容
		
		sb.setCharAt(3, '红');
		
		String subString = sb.substring(2, 4);
		System.out.println("子串的内容："+ subString);
		
		查看
	
		int index = sb.indexOf("abc", 3);
		System.out.println("索引值为："+index);
			
		sb.append("javajava");
		System.out.println("查看字符数组的长度："+ sb.capacity());   //32 = 16*2 + 2
		*/
		
		System.out.println("存储的字符个数："+sb.length());
		System.out.println("索引指定的索引值查找字符："+sb.charAt(2) );
		System.out.println("字符串缓冲类的内容："+ sb);
		
		String content = sb.toString();
		test(content);
	}
	
	public static void test(String str){
		
	}
	
}
