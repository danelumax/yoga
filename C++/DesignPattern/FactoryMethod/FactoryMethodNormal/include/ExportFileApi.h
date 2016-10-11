/*
 * ExportFileApi.h
 *
 *  Created on: Oct 11, 2016
 *      Author: eliwech
 */

#ifndef EXPORTFILEAPI_H_
#define EXPORTFILEAPI_H_

#include <string>
#include <iostream>

class ExportFileApi
{
public:
	virtual void Export(std::string data) = 0;
};

#endif /* EXPORTFILEAPI_H_ */
