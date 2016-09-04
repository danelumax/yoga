/*
 * ContextAction.cpp
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#include "ContextAction.h"
#include "MessageHandler.h"

ContextAction::ContextAction()
{
}

ContextAction::~ContextAction()
{
}

void ContextAction::handleAction(DiaSessionContext* context)
{
	if (NULL != _msgHandler)
	{
		_msgHandler->execute(context);
	}
}

/* DER */
ContextActionDER::ContextActionDER()
{
	_msgHandler = new DERMessageHandler();
}

ContextActionDER* ContextActionDER::_instance = NULL;
ContextActionDER* ContextActionDER::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextActionDER();
	}

	return _instance;
}

void ContextActionDER::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

/* MAA */
ContextActionMAA::ContextActionMAA()
{
	_msgHandler = new SWxMAAMessageHandler();
}

ContextActionMAA* ContextActionMAA::_instance = NULL;
ContextActionMAA* ContextActionMAA::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextActionMAA();
	}

	return _instance;
}

void ContextActionMAA::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

/* SAA Get Profile */
ContextActionSAAGetProfile::ContextActionSAAGetProfile()
{
	_msgHandler = new SWxSAAMessageHandler();
}

ContextActionSAAGetProfile* ContextActionSAAGetProfile::_instance = NULL;
ContextActionSAAGetProfile* ContextActionSAAGetProfile::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextActionSAAGetProfile();
	}

	return _instance;
}

void ContextActionSAAGetProfile::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

/* SAA Register */
ContextActionSAARegister::ContextActionSAARegister()
{
	_msgHandler = new SWxSAAMessageHandler();
}

ContextActionSAARegister* ContextActionSAARegister::_instance = NULL;
ContextActionSAARegister* ContextActionSAARegister::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextActionSAARegister();
	}

	return _instance;
}

void ContextActionSAARegister::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

/* S6b SAA Update Pdn Info */
ContextActionS6bSAAUpdatePdnInfo* ContextActionS6bSAAUpdatePdnInfo::_instance = NULL;
ContextActionS6bSAAUpdatePdnInfo::ContextActionS6bSAAUpdatePdnInfo()
{
	_msgHandler = new SWxSAAMessageHandler();
}

ContextActionS6bSAAUpdatePdnInfo* ContextActionS6bSAAUpdatePdnInfo::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextActionS6bSAAUpdatePdnInfo();
	}

	return _instance;
}

void ContextActionS6bSAAUpdatePdnInfo::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

/* AAR */
ContextActionS6bAAR* ContextActionS6bAAR::_instance = NULL;
ContextActionS6bAAR::ContextActionS6bAAR()
{
	_msgHandler = new S6bAARMessageHandler();
}

ContextActionS6bAAR* ContextActionS6bAAR::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextActionS6bAAR();
	}

	return _instance;
}

void ContextActionS6bAAR::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}



