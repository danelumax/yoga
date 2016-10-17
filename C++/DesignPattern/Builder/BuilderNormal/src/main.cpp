//============================================================================
// Name        : BuilderNormal.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include "Director.h"
#include "TxtBuilder.h"
#include "XmlBuilder.h"

int main()
{
	ExportHeaderModel* ehm = new ExportHeaderModel();
	ehm->setDepId("One Penny Company");
	ehm->setExportDate("2016-10-17");

	std::map< std::string, std::vector<ExportDataModel*> > mapData;
	std::vector<ExportDataModel*> col;

	ExportDataModel* edm1 = new ExportDataModel();
	edm1->setProductId("Product 001");
	edm1->setPrice(100);
	edm1->setAmount(80);

	ExportDataModel* edm2 = new ExportDataModel();
	edm2->setProductId("Product 002");
	edm2->setPrice(99);
	edm2->setAmount(55);

	col.push_back(edm1);
	col.push_back(edm2);
	mapData["Marketing Record Table"] = col;

	ExportFooterModel* efm = new ExportFooterModel();
	efm->setExportUser("John");

	TxtBuilder* txtBuilder = new TxtBuilder();
	Director* director = new Director(txtBuilder);
	director->construct(ehm, mapData, efm);

	std::cout << "\nOutput to Txt File:\n" << txtBuilder->getResult() << std::endl;

	XmlBuilder* xmlBuilder = new XmlBuilder();
	director = new Director(xmlBuilder);
	director->construct(ehm, mapData, efm);

	std::cout << "\nOutput to Xml File:\n" << xmlBuilder->getResult() << std::endl;

	delete xmlBuilder;
	delete director;
	delete txtBuilder;
	delete efm;
	delete edm2;
	delete edm1;
	delete ehm;

	return 0;
}
