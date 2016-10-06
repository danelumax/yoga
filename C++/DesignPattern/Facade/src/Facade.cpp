/*
 * Facade.cpp
 *
 *  Created on: Oct 6, 2016
 *      Author: eliwech
 */

#include "Facade.h"
#include "DAO.h"
#include "Business.h"
#include "Presentation.h"
#include "ConfigManager.h"

Facade::Facade()
{
}

Facade::~Facade()
{
	ConfigManager::destory();
}

void Facade::generate()
{
	Presentation* pre = new Presentation();
	pre->generate();

	Business * bus = new Business();
	bus->generate();

	DAO* dao = new DAO();
	dao->generate();
}
