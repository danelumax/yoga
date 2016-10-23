//============================================================================
// Name        : MediatorDep.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Dep.h"
#include "User.h"
#include "DepUserMediatorImpl.h"

int main(void)
{
	DepUserMediatorImpl* mediator = DepUserMediatorImpl::getInstance();
	Dep* dep = new Dep();
	dep->setDepId("d1");
	Dep* dep2 = new Dep();
	dep2->setDepId("d2");

	User* user = new User();
	user->setUserId("u1");

	std::cout << "\nBefore Repeal Department ----------" << std::endl;
	mediator->showUserDeps(user);

	std::cout << "\nAfter Repealing Department:" << dep->getDepId() << " ----------" << std::endl;
	dep->deleteDep();
	mediator->showUserDeps(user);

	std::cout << "\nBefore user dimission ----------" << std::endl;
	mediator->showDepUsers(dep2);

	std::cout << "\nAfter user dimission:" << user->getUserId()<< " ----------" << std::endl;
	user->dimission();
	mediator->showDepUsers(dep2);


	return 0;
}
