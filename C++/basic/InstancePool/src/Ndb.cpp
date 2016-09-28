/*
 * Ndb.cpp
 *
 *  Created on: Sep 28, 2016
 *      Author: eliwech
 */

#include "Ndb.h"

Ndb::Ndb(int id)
	: _id(id)
{
}

Ndb::~Ndb()
{
}

int Ndb::getId()
{
	return _id;
}
