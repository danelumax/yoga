/*
 * OperatorReload.cpp
 *
 *  Created on: Aug 24, 2016
 *      Author: eliwech
 */

#include "OperatorReload.h"

OperatorReload::OperatorReload(std::string valueA, std::string valueB, std::string valueC)
	:_valueA(valueA), _valueB(valueB), _valueC(valueC)
{
}

OperatorReload::~OperatorReload()
{
}

OperatorReload& OperatorReload::operator=(const OperatorReload &other)
{
	std::cout << "operator reload happen" << std::endl;
	_valueA = other._valueA;
	_valueB = other._valueB;

	return *this;
}

OperatorReload& OperatorReload::operator+(const OperatorReload &other)
{
	std::cout << "operator reload happen" << std::endl;
	_valueA += other._valueC;

	return *this;
}

void OperatorReload::showAllValue()
{
	std::cout << _valueA << std::endl;
	std::cout << _valueB << std::endl;
	std::cout << _valueC << std::endl;
}
