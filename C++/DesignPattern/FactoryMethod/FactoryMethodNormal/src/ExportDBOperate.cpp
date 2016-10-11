/*
 * ExportDBOperate.cpp
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#include "ExportDBOperate.h"
#include "ExportDB.h"

ExportDBOperate::ExportDBOperate()
{
}

ExportDBOperate::~ExportDBOperate()
{
}

ExportFileApi* ExportDBOperate::factoryMethod()
{
	return new ExportDB();
}
