/*
 * ExportDB.h
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#ifndef EXPORTDB_H_
#define EXPORTDB_H_

#include "ExportFileApi.h"

class ExportDB : public ExportFileApi
{
public:
	ExportDB();
	virtual ~ExportDB();
	virtual void Export(std::string data);
};

#endif /* EXPORTDB_H_ */
