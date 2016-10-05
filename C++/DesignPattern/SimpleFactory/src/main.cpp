//============================================================================
// Name        : SimpleFactory.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Api.h"
#include "Factory.h"

int main()
{
	Api* api = Factory::createApi(1);
	api->test1("HaHa, don't worry, just a test!");

	api = Factory::createApi(2);
	api->test1("HaHa, don't worry, just a test!");
	return 0;
}
