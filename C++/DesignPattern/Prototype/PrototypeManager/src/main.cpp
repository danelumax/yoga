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
	Prototype* p1 = new ConcretePrototype1();
	PrototypeManager* manager = PrototypeManager::getInstance();
	manager->setPrototype("Prototype1", p1);
	Prototype* p3 = manager->getPrototype("Prototype1")->clone();
	if (p3 != NULL)
	{
		p3->setName("John");
		p3->toString();
	}

	Prototype* p2 = new ConcretePrototype2();
	manager->setPrototype("Prototype1", p2);

	Prototype* p4 = manager->getPrototype("Prototype1")->clone();
	if (p4 != NULL)
	{
		p4->setName("Peter");
		p4->toString();
	}

	manager->removePrototype("Prototype1");

	Prototype* p5 = manager->getPrototype("Prototype1")->clone();
	if (p5 != NULL)
	{
		p5->setName("Tom");
		p5->toString();
	}

	return 0;
}
