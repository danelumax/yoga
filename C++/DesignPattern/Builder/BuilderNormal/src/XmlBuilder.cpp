/*
 * XmlBuilder.cpp
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#include "XmlBuilder.h"
#include <sstream>

XmlBuilder::XmlBuilder()
{
}

XmlBuilder::~XmlBuilder()
{
}

void XmlBuilder::buildHeader(ExportHeaderModel* ehm)
{
	_buffer.append("<?xml version='1.0' encoding='gb2312'?>\n");
	_buffer.append("<Header>\n");
	_buffer.append("\t" + ehm->getDepId() + "\n\t" + ehm->getExportDate() + "\n");
	_buffer.append("</Header>\n");
}

void XmlBuilder::buildBody(std::map< std::string, std::vector<ExportDataModel*> > mapData)
{
	_buffer.append("<Body>\n");
	std::map< std::string, std::vector<ExportDataModel*> >::iterator iterMap = mapData.begin();
	for(; iterMap!=mapData.end(); ++iterMap)
	{
		std::vector<ExportDataModel*> modelVec = iterMap->second;
		std::vector<ExportDataModel*>::iterator it = modelVec.begin();
		for(; it!=modelVec.end(); ++it)
		{
			_buffer.append("\t<Data>\n");
			std::ostringstream oss;
			oss << "\t\t" <<(*it)->getProductId() << "\n\t\t" << (*it)->getPrice() << "\n\t\t" << (*it)->getAmount() << "\n";
			_buffer.append(oss.str());
			_buffer.append("\t</Data>\n");
		}
	}
	_buffer.append("</Body>\n");
}

void XmlBuilder::buildFooter(ExportFooterModel* efm)
{
	_buffer.append("<Footer>\n");
	_buffer.append("\t" + efm->getExportUser() + "\n");
	_buffer.append("</Footer>\n");
}

std::string XmlBuilder::getResult()
{
	return _buffer;
}
