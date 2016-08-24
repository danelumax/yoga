/*
 * OperatorReload.h
 *
 *  Created on: Aug 24, 2016
 *      Author: eliwech
 */

#ifndef OPERATORRELOAD_H_
#define OPERATORRELOAD_H_

#include <string>
#include <iostream>

class OperatorReload {
public:
	OperatorReload(std::string valueA, std::string valueB, std::string valueC);
	virtual ~OperatorReload();
	OperatorReload& operator=(const OperatorReload &other);
	OperatorReload& operator+(const OperatorReload &other);
	void showAllValue();
private:
	std::string _valueA;
	std::string _valueB;
	std::string _valueC;

};

#endif /* OPERATORRELOAD_H_ */
