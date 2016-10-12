//============================================================================
// Name        : FactoryMethod.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "ExportOperate.h"

int main()
{
	ExportOperate* operate = new ExportOperate();
	operate->Export(1, "test data");
	operate->Export(2, "test data");
	operate->Export(3, "test data");
	operate->Export(4, "test data");

	return 0;
}
