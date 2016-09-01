//============================================================================
// Name        : ContextFSM.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <ContextPolicy.h>
#include <ContextPolicyFactory.h>
#include <DiaSessionContextFsm.h>
#include <DiaCommonCode.h>

int main()
{
	DiaSessionContextFsm* _fsm = new DiaSessionContextFsm();
	ContextPolicy* ctxPolicy = ContextPolicyFactory::getInstance()->getContextPolicy(DIA_APP_ID_SWM, DIA_CMD_CODE_DE);
	ctxPolicy->initContextFsm(_fsm);
	return 0;
}
