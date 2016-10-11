/*
 * ExportTxtFileOperate.h
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#ifndef EXPORTTXTFILEOPERATE_H_
#define EXPORTTXTFILEOPERATE_H_

#include "ExportOperate.h"

class ExportTxtFileOperate : public ExportOperate
{
public:
	ExportTxtFileOperate();
	virtual ~ExportTxtFileOperate();
	virtual ExportFileApi* factoryMethod();
};

#endif /* EXPORTTXTFILEOPERATE_H_ */
