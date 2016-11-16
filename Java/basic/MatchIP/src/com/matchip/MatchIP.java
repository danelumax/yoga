package com.matchip;

import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MatchIP {
	
	public String matchIP(String ip, String regex) {
        Pattern p=Pattern.compile(regex);
        Matcher m=p.matcher(ip);
        if(m.find()) {
        	return (String)m.group();
        } else {
        	return null;
        }
	}
	
	public static void main(String[] args) 
		throws IOException {
		
		MatchIP mip = new MatchIP();
		String result = mip.matchIP("169.254.100.2", "\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}");

		if (result != null) {
        	System.out.println("Output: "+ result);
        }
    }
}
