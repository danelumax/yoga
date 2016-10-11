/*
 * ExportOperate.cpp
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#include "ExportOperate.h"

ExportOperate::ExportOperate()
{
}

ExportOperate::~ExportOperate()
{
}

void ExportOperate::Export(std::string data)
{
	ExportFileApi* api = factoryMethod();
	api->Export(data);
}
