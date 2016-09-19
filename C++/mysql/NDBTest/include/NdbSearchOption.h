/*
 * NdbSearchOption.h
 *
 *  Created on: Sep 18, 2016
 *      Author: eliwech
 */

#ifndef NDBSEARCHOPTION_H_
#define NDBSEARCHOPTION_H_

#include "SearchOption.h"

class NdbSearchOption : public SearchOption
{
public:
	/* search type */
	enum Type
	{
		T_SINGLE_PK = 0,
		T_UNKNOWN
	};
	NdbSearchOption();
	virtual ~NdbSearchOption();
	void setTable(std::string table);
	void setType(NdbSearchOption::Type type);
	NdbSearchOption::Type getType();
private:
	NdbSearchOption::Type _type;
};

#endif /* NDBSEARCHOPTION_H_ */
