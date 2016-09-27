//============================================================================
// Name        : FindSubStr.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include <boost/algorithm/string.hpp>

int main()
{
	std::string strBase = "abcde";
	std::string testStr1 = "abc";
	std::string testStr2 = "homo";
	boost::iterator_range<std::string::iterator> r = boost::algorithm::find_first(strBase, testStr1);
	std::cout << "match: " << r << std::endl;
	r = boost ::algorithm::find_first(strBase, testStr2);
	if (r.empty())
	{
		std::cout << "no match" << std::endl;
	}
	else
	{
		std::cout << r << std::endl;
	}
	return 0;
}
