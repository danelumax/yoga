/*
 * DAO.cpp
 *
 *  Created on: Oct 6, 2016
 *      Author: eliwech
 */

#include "DAO.h"
#include "ConfigModel.h"
#include "ConfigManager.h"

DAO::DAO()
{
}

DAO::~DAO()
{
}

void DAO::generate()
{
	ConfigModel* cm = ConfigManager::getInstance()->getConfigData();
	if (cm->isNeed_needGenDAO())
	{
		std::cout << "Generating Data Code file ..." << std::endl;
	}
}
