//============================================================================
// Name        : EapFSM.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include <EAPHandler.h>
int main()
{
	DiaSessionContext *context = new DiaSessionContext();
	context->setState(STATE_IDLE);

	EAPHandler *handler = new EAPHandler(context);
	handler->Authentication();
	handler->Authorization();
}
