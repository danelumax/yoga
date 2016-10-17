/*
 * TxtBuilder.h
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#ifndef TXTBUILDER_H_
#define TXTBUILDER_H_

#include "Builder.h"

class TxtBuilder : public Builder
{
public:
	TxtBuilder();
	virtual ~TxtBuilder();
	virtual void buildHeader(ExportHeaderModel* ehm);
	virtual void buildBody(std::map< std::string, std::vector<ExportDataModel*> > mapData);
	virtual void buildFooter(ExportFooterModel* efm);
	std::string getResult();
private:
	std::string _buffer;
};

#endif /* TXTBUILDER_H_ */
