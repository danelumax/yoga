/*
 * ConfigModel.cpp
 *
 *  Created on: Oct 6, 2016
 *      Author: eliwech
 */

#include "ConfigModel.h"

ConfigModel::ConfigModel()
	: _needGenPresentation(true),
	  _needGenBusiness(true),
	  _needGenDAO(true)
{
}

ConfigModel::~ConfigModel()
{
}

bool ConfigModel::isNeedGenPresentation()
{
	return _needGenPresentation;
}

bool ConfigModel::isNeedGenBusiness()
{
	return _needGenBusiness;
}

bool ConfigModel::isNeed_needGenDAO()
{
	return _needGenDAO;
}


