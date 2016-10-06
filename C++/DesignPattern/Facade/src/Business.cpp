/*
 * Business.cpp
 *
 *  Created on: Oct 6, 2016
 *      Author: eliwech
 */

#include "Business.h"
#include "ConfigModel.h"
#include "ConfigManager.h"

Business::Business()
{
}

Business::~Business()
{
}

void Business::generate()
{
	ConfigModel* cm = ConfigManager::getInstance()->getConfigData();
	if (cm->isNeedGenBusiness())
	{
		std::cout << "Generating Business Code file ..." << std::endl;
	}
}
