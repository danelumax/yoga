//============================================================================
// Name        : Adapter.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Adaptee.h"
#include "Target.h"

int main(void)
{
	Adaptee *adaptee = new Adaptee();

	Target *target = new Adapter(adaptee);
	target->request();
	return 0;
}
