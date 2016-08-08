//============================================================================
// Name        : AssignInitial.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <string>
#include <vector>
#include <map>
#include "boost/assign.hpp"

std::vector<std::string> vectorTest = boost::assign::list_of
	("one")
	("two")
	("three");

std::map<std::string, std::string> mapTest = boost::assign::map_list_of
	("key1", "value1")
	("key2", "value2")
	("key3", "value3");


int main()
{
	std::cout << "Traverse vector:" << std::endl;
	std::vector<std::string>::iterator iter = vectorTest.begin();
	for(; iter!=vectorTest.end(); ++iter)
	{
		std::cout << *iter << std::endl;
	}
	std::cout << "Use index to get the second element:" << std::endl;
	std::cout << vectorTest[1] << std::endl;

	std::cout << "\nTraverse map:" << std::endl;
	std::map<std::string, std::string>::iterator it = mapTest.begin();
	for (; it!=mapTest.end(); ++it)
	{
		std::cout << it->second << std::endl;
	}
	std::cout << "Use find \"key2\" to get the second value:" << std::endl;
	it = mapTest.find("key2");
	std::cout << it->second << std::endl;
	return 0;
}
