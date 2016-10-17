/*
 * Director.cpp
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#include "Director.h"

Director::Director(Builder* builder)
	: _builder(builder)
{
}

Director::~Director()
{
}

void Director::construct(ExportHeaderModel* ehm,
						 std::map< std::string, std::vector<ExportDataModel*> > mapData,
						 ExportFooterModel* efm)
{
	_builder->buildHeader(ehm);
	_builder->buildBody(mapData);
	_builder->buildFooter(efm);
}
