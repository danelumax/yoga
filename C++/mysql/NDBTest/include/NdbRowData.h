/*
 * NdbRowData.h
 *
 *  Created on: Sep 21, 2016
 *      Author: eliwech
 */

#ifndef NDBROWDATA_H_
#define NDBROWDATA_H_

#include <map>
#include <string>

class NdbRowData
{
public:
	NdbRowData();
	virtual ~NdbRowData();
	void addValue(std::string colName, std::string value);
	int getValue(std::string colName, std::string& value);
	std::map<std::string, std::string> getValues();
private:
	std::map<std::string, std::string> _values;
};

#endif /* NDBROWDATA_H_ */
