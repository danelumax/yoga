//============================================================================
// Name        : FactoryMethod.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "ExportTxtFileOperate.h"
#include "ExportDBOperate.h"

int main()
{
	ExportOperate* operate = new ExportTxtFileOperate();
	operate->Export("test data");

	operate = new ExportDBOperate();
	operate->Export("test data");
	return 0;
}
