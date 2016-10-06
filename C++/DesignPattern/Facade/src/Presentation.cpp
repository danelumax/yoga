/*
 * Presentation.cpp
 *
 *  Created on: Oct 6, 2016
 *      Author: eliwech
 */

#include "Presentation.h"
#include "ConfigModel.h"
#include "ConfigManager.h"

Presentation::Presentation()
{
}

Presentation::~Presentation()
{
}

void Presentation::generate()
{
	ConfigModel* cm = ConfigManager::getInstance()->getConfigData();
	if (cm->isNeedGenPresentation())
	{
		std::cout << "Generating Presentation Code file ..." << std::endl;
	}
}
