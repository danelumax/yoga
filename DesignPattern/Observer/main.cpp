//============================================================================
// Name        : Observer.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Reader.h"
#include "Newspaper.h"

int main(void)
{
	Newspaper *subject = new Newspaper("Liwei Paper");

	Reader *reader1 = new Reader("Tom");
	Reader *reader2 = new Reader("Jack");
	Reader *reader3 = new Reader("Peter");

	subject->attach(reader1);
	subject->attach(reader2);
	subject->attach(reader3);

	/*1. Activate subject status changing */
	subject->setContent("International News");
	return 0;
}
