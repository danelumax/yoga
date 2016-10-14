/*
 * HyMemory.h
 *
 *  Created on: Oct 14, 2016
 *      Author: eliwech
 */

#ifndef HYMEMORY_H_
#define HYMEMORY_H_

#include "MemoryApi.h"

class HyMemory : public MemoryApi
{
public:
	HyMemory();
	virtual ~HyMemory();
	virtual void cacheData();
};

#endif /* HYMEMORY_H_ */
