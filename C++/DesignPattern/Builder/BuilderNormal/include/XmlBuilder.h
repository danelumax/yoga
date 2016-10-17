/*
 * XmlBuilder.h
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#ifndef XMLBUILDER_H_
#define XMLBUILDER_H_

#include "Builder.h"

class XmlBuilder : public Builder
{
public:
	XmlBuilder();
	virtual ~XmlBuilder();
	virtual void buildHeader(ExportHeaderModel* ehm);
	virtual void buildBody(std::map< std::string, std::vector<ExportDataModel*> > mapData);
	virtual void buildFooter(ExportFooterModel* efm);
	std::string getResult();
private:
	std::string _buffer;
};

#endif /* XMLBUILDER_H_ */
