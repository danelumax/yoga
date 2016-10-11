/*
 * ExportTxtFileOperate.cpp
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#include "ExportTxtFileOperate.h"
#include "ExportTxtFile.h"

ExportTxtFileOperate::ExportTxtFileOperate()
{
}

ExportTxtFileOperate::~ExportTxtFileOperate()
{
}

ExportFileApi* ExportTxtFileOperate::factoryMethod()
{
	return new ExportTxtFile();
}
