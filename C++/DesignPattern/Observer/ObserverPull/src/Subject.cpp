/*
 * Subject.cpp
 *
 *  Created on: Aug 12, 2016
 *      Author: eliwech
 */

#include "Subject.h"

Subject::Subject()
{
}

Subject::~Subject()
{
}

void Subject::attach(Observer *reader)
{
	_readers.push_back(reader);
}

void Subject::detach(Observer *reader)
{
	std::vector<Observer*>::iterator iter = _readers.begin();
	for(; iter!=_readers.end(); ++iter)
	{
		if (*iter == reader)
		{
			_readers.erase(iter);
		}
	}
}

/*4. traverse all reader to notify */
void Subject::notifyObservers()
{
	std::vector<Observer*>::iterator iter = _readers.begin();
	for(; iter!=_readers.end(); ++iter)
	{
		/*5. call reader to get Subject obj */
		(*iter)->update(this);
	}
}
