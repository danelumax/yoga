/*
 * Builder.h
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#ifndef BUILDER_H_
#define BUILDER_H_

#include <map>
#include <vector>
#include "ExportHeaderModel.h"
#include "ExportDataModel.h"
#include "ExportFooterModel.h"

class Builder
{
public:
	virtual void buildHeader(ExportHeaderModel* ehm) = 0;
	virtual void buildBody(std::map< std::string, std::vector<ExportDataModel*> > mapData) = 0;
	virtual void buildFooter(ExportFooterModel* efm) = 0;
};

#endif /* BUILDER_H_ */
