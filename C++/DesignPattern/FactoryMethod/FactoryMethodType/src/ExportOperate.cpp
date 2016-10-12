/*
 * ExportOperate.cpp
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#include "ExportOperate.h"
#include "ExportDB.h"
#include "ExportXml.h"
#include "ExportTxtFile.h"

ExportOperate::ExportOperate()
{
}

ExportOperate::~ExportOperate()
{
}

void ExportOperate::Export(int type, std::string data)
{
	ExportFileApi* api = factoryMethod(type);
	if (api != NULL)
	{
		api->Export(data);
	}
	else
	{
		std::cout << "Wrong Export Type !" << std::endl;
	}
}

ExportFileApi* ExportOperate::factoryMethod(int type)
{
	/* delay to product */
	ExportFileApi* api = NULL;
	if (1 == type)
	{
		api = new ExportTxtFile();
	}
	else if (2 == type)
	{
		api = new ExportDB();
	}
	else if (3 == type)
	{
		api = new ExportXml();
	}

	return api;
}
