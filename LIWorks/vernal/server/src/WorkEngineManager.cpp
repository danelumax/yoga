/*
 * WorkEngineManager.cpp
 *
 *  Created on: 2016年2月13日
 *      Author: root
 */

#include "WorkEngineManager.h"

WorkEngineManager* WorkEngineManager::_instance = NULL;

WorkEngineManager::WorkEngineManager()
{
	// TODO Auto-generated constructor stub

}

WorkEngineManager::~WorkEngineManager() {
	// TODO Auto-generated destructor stub
}

WorkEngineManager* WorkEngineManager::getInstance()
{
	if(_instance == NULL)
	{
		_instance = new WorkEngineManager();
	}

	return _instance;
}

int WorkEngineManager::registerWorkEngine(int type, WorkEngine* engine)
{
	if(NULL == engine)
	{
		return -1;
	}
	std::list<WorkEngine*>::iterator it = _engineList.begin();
    while(it != _engineList.end())
	{
        if((*it)  == engine)
        {
            return 0;
        }
        it++;
	}
	_engineList.push_back(engine);

	return 0;
}

int WorkEngineManager::startAllWorkEngines()
{
    std::list<WorkEngine*>::iterator it = _engineList.begin();
    while(it != _engineList.end())
    {
	    WorkEngine* engine = *it;
	    engine->start();
	    it++;
    }
    return 0;
}

void WorkEngineManager::clearWorkEngines()
{
    std::list<WorkEngine*>::iterator it = _engineList.begin();
    while(it != _engineList.end())
    {
    	(*it)->destroy();
    	delete (*it);
    	it++;
    }
    _engineList.clear();
}
