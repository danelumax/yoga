/*
 * TxtBuilder.cpp
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#include "TxtBuilder.h"
#include <sstream>

TxtBuilder::TxtBuilder()
	: _buffer("")
{
}

TxtBuilder::~TxtBuilder()
{
}

void TxtBuilder::buildHeader(ExportHeaderModel* ehm)
{
	_buffer.append(ehm->getDepId() + ", " + ehm->getExportDate() + "\n");
}

void TxtBuilder::buildBody(std::map< std::string, std::vector<ExportDataModel*> > mapData)
{
	std::map< std::string, std::vector<ExportDataModel*> >::iterator iterMap = mapData.begin();
	for(; iterMap!=mapData.end(); ++iterMap)
	{
		std::vector<ExportDataModel*> modelVec = iterMap->second;
		std::vector<ExportDataModel*>::iterator it = modelVec.begin();
		for(; it!=modelVec.end(); ++it)
		{
			std::ostringstream oss;
			oss << (*it)->getProductId() << ", " << (*it)->getPrice() << ", " << (*it)->getAmount() << "\n";
			_buffer.append(oss.str());
		}


	}
}

void TxtBuilder::buildFooter(ExportFooterModel* efm)
{
	_buffer.append(efm->getExportUser());
}

std::string TxtBuilder::getResult()
{
	return _buffer;
}
