//============================================================================
// Name        : Facade.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Facade.h"

int main()
{
	Facade* facade = new Facade();
	facade->generate();

	delete facade;

	return 0;
}
