//============================================================================
// Name        : sharedPtr.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include "boost/shared_ptr.hpp"

class TestSharedPtr
{
public:
	TestSharedPtr(std::string str);
	~TestSharedPtr();
	void show();
private:
	std::string _str;
};

TestSharedPtr::TestSharedPtr(std::string str)
{
	std::cout << "\nInitializing object ..." << std::endl;
	_str = str;
}

TestSharedPtr::~TestSharedPtr()
{
	std::cout << "\nShared_prt is destorying object ..." << std::endl;
}

void TestSharedPtr::show()
{
	std::cout << _str << std::endl;
}

int main(void)
{
	std::cout << "\nbreakpoint 1" << std::endl;

	TestSharedPtr *obj = new TestSharedPtr("test string");

	std::cout << "\nbreakpoint 2" << std::endl;

	boost::shared_ptr<TestSharedPtr> sharedPrtObj(obj);

	std::cout << "\nbreakpoint 3" << std::endl;

	sharedPrtObj.get()->show();

	std::cout << "\nbreakpoint 4" << std::endl;

	return 0;
}
