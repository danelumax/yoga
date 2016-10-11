/*
 * ExportOperate.h
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#ifndef EXPORTOPERATE_H_
#define EXPORTOPERATE_H_

#include "ExportFileApi.h"

class ExportOperate
{
public:
	ExportOperate();
	virtual ~ExportOperate();
	void Export(std::string data);
	virtual ExportFileApi* factoryMethod() = 0;
};

#endif /* EXPORTOPERATE_H_ */
