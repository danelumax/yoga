//============================================================================
// Name        : MultiKeyMap.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <map>
#include <string>
#include <iostream>

struct TestPairCmp
{
	bool operator()(const std::pair<std::string, std::string> p1, const std::pair<std::string, std::string> p2) const
	{
		std::cout << "Trigger multi Map compare." << std::endl;
		/* return (p1.first < p2.first) is ok as well */
		return (p1.first < p2.first) || ((p1.first == p2.first) && (p1.second < p2.second));
	}
};
typedef std::map<std::pair<std::string, std::string>, std::string, TestPairCmp> TestMapType;

int main()
{
	TestMapType testMap;
	std::string key1 = "key1";
	std::string key2 = "key2";
	std::string key3 = "key3";
	std::string key4 = "key4";
	std::string value1 = "value1";
	std::string value2 = "value2";

	std::cout << "\nInsert value into map:" << std::endl;
	testMap[std::make_pair(key1, key2)] = value1;
	testMap[std::make_pair(key3, key4)] = value2;

	std::cout << "\nGet value using iteration:" << std::endl;
	TestMapType::iterator iter = testMap.begin();
	for(; iter!=testMap.end(); iter++)
	{
		std::cout << iter->second << std::endl;
	}

	std::cout << "\nGet value using find:" << std::endl;
	iter = testMap.find(std::make_pair(key1, key2));
	std::cout << iter->second << std::endl;
	iter = testMap.find(std::make_pair(key3, key4));
	std::cout << iter->second << std::endl;



	return 0;
}
