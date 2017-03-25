package com.nio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Set;

public class NIOServer {

	private static boolean stop = false;
	private int blockSize = 4096;
	private ByteBuffer sendbuffer = ByteBuffer.allocate(blockSize);
	private ByteBuffer receiveBuffer = ByteBuffer.allocate(blockSize);
	Selector selector;
	
	//server初始化
	public NIOServer(int port) throws IOException {
		
		//打开server端的channel
		ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
		//设置非阻塞
		serverSocketChannel.configureBlocking(false);
		//获得server的socket
		ServerSocket serverSocket = serverSocketChannel.socket();
		//绑定IP和端口
		serverSocket.bind(new InetSocketAddress(port));
		//打开选择器
		selector = Selector.open();
		//将channel注册到selector上
		serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
		System.out.println("[Server] start->" + port);
	}
	
	//监听
	public void listen() throws IOException{
		
		while(!stop) {
			//轮询selector,查看是否有client的消息
			selector.select();
			Set<SelectionKey> selectionKeys = selector.selectedKeys();
			Iterator<SelectionKey> iterator = selectionKeys.iterator();
			while(iterator.hasNext()) {
				SelectionKey selectionKey = iterator.next();
				iterator.remove();
				//业务逻辑
				handleKey(selectionKey);
			}
		}
	}
	
	public void handleKey(SelectionKey selectionKey) throws IOException{
		
		ServerSocketChannel server = null;
		SocketChannel client = null;
		String receiveText;
		String sendText;
		int count = 0;
		if (selectionKey.isAcceptable()) {
			server = (ServerSocketChannel) selectionKey.channel();
			client = server.accept();
			client.configureBlocking(false);
			client.register(selector, selectionKey.OP_READ);
			System.out.println("[Server] Server is connected to client " +client.toString());
		} else if (selectionKey.isReadable()) {
			client = (SocketChannel) selectionKey.channel();
			count = client.read(receiveBuffer);
			if (count > 0) {
				receiveText = new String(receiveBuffer.array(), 0, count);
				System.out.println("[Server] Receive msg from client : " + receiveText);
				client.register(selector, selectionKey.OP_WRITE);
			}
		} else if (selectionKey.isWritable()) {
			sendbuffer.clear();
			client = (SocketChannel) selectionKey.channel();
			sendText = "< Sever msg >";
			sendbuffer.put(sendText.getBytes());
			sendbuffer.flip();
			
			client.write(sendbuffer);
			System.out.println("[Server] Send to client : " + sendText);
			System.out.println("[Server] Closing client");
			
			client.close();
			stop = true;
		}
	}
	
	public static void main(String[] args) throws IOException {
		
		int port = 7080;
		NIOServer server = new NIOServer(port);
		server.listen();
	}
}
