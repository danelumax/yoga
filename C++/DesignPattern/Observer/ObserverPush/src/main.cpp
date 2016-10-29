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
	Newspaper *subject = new Newspaper();

	Reader *reader1 = new Reader();
	reader1->setName("John");
	Reader *reader2 = new Reader();
	reader2->setName("Jack");
	Reader *reader3 = new Reader();
	reader3->setName("Peter");

	subject->attach(reader1);
	subject->attach(reader2);
	subject->attach(reader3);

	/*1. Activate subject status changing */
	subject->setContent("\"The Current Content is Observer Pattern\"");
	return 0;
}
