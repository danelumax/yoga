/*
 * Director.h
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#ifndef DIRECTOR_H_
#define DIRECTOR_H_

#include "Builder.h"

class Director
{
public:
	Director(Builder* builder);
	virtual ~Director();
	void construct(ExportHeaderModel* ehm,
				   std::map< std::string, std::vector<ExportDataModel*> > mapData,
				   ExportFooterModel* efm);
private:
	Builder* _builder;
};

#endif /* DIRECTOR_H_ */
