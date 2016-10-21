//============================================================================
// Name        : PrototypeManager.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "PrototypeManager.h"
#include "ConcretePrototype1.h"
#include "ConcretePrototype2.h"

int main()
{
	/* Initial Prototype Manager */
	Prototype* prototype = NULL;
	Prototype* p1 = new ConcretePrototype1();
	PrototypeManager* manager = PrototypeManager::getInstance();
	manager->setPrototype("Prototype1", p1);

	/* Fetch the prototype */
	prototype = manager->getPrototype("Prototype1");
	if (prototype != NULL)
	{
		Prototype* p3 = prototype->clone();
		p3->setName("John");
		p3->toString();
	}

	/* Change the prototype */
	Prototype* p2 = new ConcretePrototype2();
	manager->setPrototype("Prototype1", p2);

	/* Fetch the prototype */
	prototype = manager->getPrototype("Prototype1");
	if (prototype != NULL)
	{
		Prototype* p4 = prototype->clone();
		p4->setName("Peter");
		p4->toString();
	}

	/* Delete the prototype */
	manager->removePrototype("Prototype1");

	/* Fetch the prototype again*/
	prototype = manager->getPrototype("Prototype1");
	if (prototype != NULL)
	{
		Prototype* p5 = prototype->clone();
		p5->setName("Tom");
		p5->toString();
	}

	PrototypeManager::destory();
	delete p1;
	delete p2;
	delete prototype;

	return 0;
}
