/*
 * ExportDBOperate.h
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#ifndef EXPORTDBOPERATE_H_
#define EXPORTDBOPERATE_H_

#include "ExportOperate.h"

class ExportDBOperate : public ExportOperate
{
public:
	ExportDBOperate();
	virtual ~ExportDBOperate();
	virtual ExportFileApi* factoryMethod();
};

#endif /* EXPORTDBOPERATE_H_ */
