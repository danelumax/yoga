/*
 * EPCAction.cpp
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#include <iostream>
#include "EPCAction.h"

EPCAction::EPCAction()
{
}

EPCAction::~EPCAction()
{
}

void EPCActionRequestAuthVector::doAction(DiaSessionContext* context)
{
	std::cout << "Action: do Request Auth Vector" << std::endl;
}

void EPCActionRequestProfile::doAction(DiaSessionContext* context)
{
	std::cout << "Action: do Request Profile" << std::endl;
}

void EPCActionSendChallenge::doAction(DiaSessionContext* context)
{
	std::cout << "Action: do Send Challenge" << std::endl;
}

void EPCActionSendSuccess::doAction(DiaSessionContext* context)
{
	std::cout << "Action: do Send Success" << std::endl;
}

void EPCActionSendReauthentication::doAction(DiaSessionContext* context)
{
	std::cout << "Action: do Send Re-Authentication" << std::endl;
}
