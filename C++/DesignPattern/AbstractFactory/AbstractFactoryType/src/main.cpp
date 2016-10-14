/*
 * main.cpp
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#include "Schema1.h"
#include "Schema2.h"
#include "Schema3.h"
#include "ComputeEngineer.h"
#include "AbstractFactory.h"

int main()
{
	ComputeEngineer* engineer = new ComputeEngineer();

	std::cout << "\nTest Schema1 ..." << std::endl;
	AbstractFactory* schema = new Schema1();
	engineer->makeComputer(schema);

	std::cout << "\nTest Schema2 ..." << std::endl;
	schema = new Schema2();
	engineer->makeComputer(schema);

	std::cout << "\nTest Schema3 ..." << std::endl;
	schema = new Schema3();
	engineer->makeComputer(schema);

	delete schema;
	delete engineer;

	return 0;
}

