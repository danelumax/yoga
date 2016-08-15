/*
 * WorkEngineManager.h
 *
 *  Created on: 2016年2月13日
 *      Author: root
 */

#ifndef VERNAL_SERVER_WORKENGINEMANAGER_H_
#define VERNAL_SERVER_WORKENGINEMANAGER_H_

#include <iostream>
#include <list>
#include <WorkEngine.h>

class WorkEngineManager {
public:
	virtual ~WorkEngineManager();
	static WorkEngineManager* getInstance();
	int registerWorkEngine(int type, WorkEngine* engine);
	int startAllWorkEngines();
	void clearWorkEngines();
protected:
	WorkEngineManager();
private:
	static WorkEngineManager* _instance;
	std::list<WorkEngine*> _engineList;
};

#endif /* VERNAL_SERVER_WORKENGINEMANAGER_H_ */
