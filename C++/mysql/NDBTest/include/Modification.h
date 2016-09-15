/*
 * Modification.h
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#ifndef MODIFICATION_H_
#define MODIFICATION_H_

#include <map>
#include <string>

class Modification
{
public:
	Modification(std::string table);
	virtual ~Modification();
	void addValue(std::string key, int value);
	std::map<std::string, int> getValues();
	std::string getTable();
private:
	std::string _table;
	std::map<std::string, int> _values;
};

#endif /* MODIFICATION_H_ */
