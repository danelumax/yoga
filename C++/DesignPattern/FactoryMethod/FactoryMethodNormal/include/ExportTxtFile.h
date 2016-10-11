/*
 * ExportTxtFile.h
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#ifndef EXPORTTXTFILE_H_
#define EXPORTTXTFILE_H_

#include "ExportFileApi.h"

class ExportTxtFile : public ExportFileApi
{
public:
	ExportTxtFile();
	virtual ~ExportTxtFile();
	virtual void Export(std::string data);
};

#endif /* EXPORTTXTFILE_H_ */
