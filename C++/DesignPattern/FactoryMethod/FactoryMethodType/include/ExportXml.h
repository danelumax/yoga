/*
 * ExportXml.h
 *
 *  Created on: Oct 12, 2016
 *      Author: eliwech
 */

#ifndef EXPORTXML_H_
#define EXPORTXML_H_

#include "ExportFileApi.h"

class ExportXml : public ExportFileApi
{
public:
	ExportXml();
	virtual ~ExportXml();
	void Export(std::string data);
};

#endif /* EXPORTXML_H_ */
