//============================================================================
// Name        : ObjectPool.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include <map>
#include <boost/pool/object_pool.hpp>

class TestModel
{
public:
	TestModel(int value):_value(value){}
	~TestModel()
	{
		std::cout << "destory ~ " << std::endl;
	}
	int getValue()
	{
		return _value;
	}
private:
	int _value;
};

int main()
{
	boost::object_pool<TestModel> pl;
	std::map<int, TestModel*> TestMap;
	std::map<int, TestModel*>::iterator iter;

	/* insert obj into map */
	for(int i=0; i<10; i++)
	{
		TestModel *poolElement = pl.construct(i);
		iter = TestMap.find(i);
		if (iter == TestMap.end())
		{
			TestMap[i] = poolElement;
		}
	}

	/* show all map value */
	std::cout << "Show all map values ..." << std::endl;
	iter = TestMap.begin();
	for(; iter!=TestMap.end(); iter++)
	{
		std::cout << iter->second->getValue() << std::endl;
	}

	/* wait pool recover source */
	std::cout << "Object pool will destory obj pointers from pool, you don't need delete them ..." << std::endl;

	return 0;
}
