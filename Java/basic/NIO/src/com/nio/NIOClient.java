package com.nio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Set;

public class NIOClient {

	private static boolean isStop = false;
	private static int blockSize = 4096;
	private static ByteBuffer sendbuffer = ByteBuffer.allocate(blockSize);
	private static ByteBuffer receiveBuffer = ByteBuffer.allocate(blockSize);
	private final static InetSocketAddress serverAddress = new InetSocketAddress("127.0.0.1", 7080);
	
	public static void main(String[] args) throws IOException {
		
		SocketChannel socketChannel = SocketChannel.open();
		socketChannel.configureBlocking(false);
		//打开选择器
		Selector selector = Selector.open();
		socketChannel.register(selector, SelectionKey.OP_CONNECT);
		socketChannel.connect(serverAddress);
		
		Set<SelectionKey> selectionKeys;
		Iterator<SelectionKey> iterator;
		SelectionKey selectionKey;
		SocketChannel client;
		String receiveText;
		String sendText;
		int count;
		
		while(!isStop) {
			//轮询selector,查看是否有server的消息
			selector.select();
			selectionKeys = selector.selectedKeys();
			iterator = selectionKeys.iterator();
			while(iterator.hasNext()) {
				selectionKey = iterator.next();
				if (selectionKey.isConnectable()) {
					System.out.println("[Client] Client request connection");
					client = (SocketChannel) selectionKey.channel();
					if (client.isConnectionPending()) {
						client.finishConnect();
						System.out.println("[Client] Connection finished");
						sendbuffer.clear();
						sendText = "< Hello Server >";
						sendbuffer.put(sendText.getBytes());
						sendbuffer.flip();
						client.write(sendbuffer);
						System.out.println("[Client] Client send first message to server" + sendText);
					}
					client.register(selector, SelectionKey.OP_READ);
				}
				if (selectionKey.isReadable()) {
					client = (SocketChannel) selectionKey.channel();
					receiveBuffer.clear();
					count = client.read(receiveBuffer);
					if (count > 0) {
						receiveText = new String(receiveBuffer.array(), 0, count);
						System.out.println("[Client] Client receive message from server" + receiveText);
						client.register(selector, SelectionKey.OP_WRITE);
					}
				}
				if (selectionKey.isWritable()) {
					sendbuffer.clear();
					client = (SocketChannel) selectionKey.channel();
					sendText = "< Client msg >";
					sendbuffer.put(sendText.getBytes());
					sendbuffer.flip();
					client.write(sendbuffer);
					System.out.println("[Client] Client send message to server" + sendText);
					client.register(selector, selectionKey.OP_READ);
					
					System.out.println("[Client] Close");
					isStop = true;
					break;
				}
			}
			selectionKeys.clear();
		}
	}
}
