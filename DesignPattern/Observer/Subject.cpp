/*
 * Subject.cpp
 *
 *  Created on: Aug 12, 2016
 *      Author: eliwech
 */

#include "Subject.h"

std::string Subject::getContent()
{
	return _content;
}

void Subject::setContent(std::string content)
{
	/*2. change status */
	_content = content;
	/*3. notify */
	notifyObservers();
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
	std::cout << _subjectName << " comes hot news!" << std::endl;
	std::vector<Observer*>::iterator iter = _readers.begin();
	for(; iter!=_readers.end(); ++iter)
	{
		/*5. call reader to get Subject obj */
		(*iter)->update(this);
	}
}
