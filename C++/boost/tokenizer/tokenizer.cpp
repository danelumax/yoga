//============================================================================
// Name        : tokenizer.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================
#include <string>
#include <iostream>

#include <boost/format.hpp>
#include <boost/tokenizer.hpp>
#include <boost/algorithm/string.hpp>

typedef boost::tokenizer<boost::char_separator<char> > CustomTokenizer;

int main()
{
	//blank space
	std::string strTag("I come from China");
	boost::char_separator<char> sep(" , ");
	CustomTokenizer tok(strTag, sep);

	std::vector<std::string> vecSegTag;
	CustomTokenizer::iterator iter = tok.begin();
	for(; iter!=tok.end(); ++iter)
	{
		vecSegTag.push_back(*iter);
	}

	for(unsigned int i=0; i<vecSegTag.size(); i++)
	{
		std::cout << vecSegTag[i] << std::endl;
	}
	vecSegTag.clear();


    //","
	std::string strTag1("hello,world");
	CustomTokenizer tok1(strTag1, sep);

	iter = tok1.begin();
	for(; iter!=tok1.end(); ++iter)
	{
		vecSegTag.push_back(*iter);
	}

	for(unsigned int i=0; i<vecSegTag.size(); i++)
	{
		std::cout << vecSegTag[i] << std::endl;
	}
	return 0;
}

