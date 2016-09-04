/*
 * ContextAction.h
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#ifndef CONTEXTACTION_H_
#define CONTEXTACTION_H_

#include <iostream>
#include <MessageHandler.h>
#include <DiaSessionContext.h>

class ContextAction
{
public:
	ContextAction();
	virtual ~ContextAction();
	void handleAction(DiaSessionContext* context);
protected:
	MessageHandler* _msgHandler;
};

/* DER */
class ContextActionDER : public ContextAction
{
public:
	virtual ~ContextActionDER(){};
	static ContextActionDER* getInstance();
	static void destory();
private:
	ContextActionDER();
	static ContextActionDER* _instance;
};

/* MAA */
class ContextActionMAA : public ContextAction
{
public:
	virtual ~ContextActionMAA(){};
	static ContextActionMAA* getInstance();
	static void destory();
private:
	ContextActionMAA();
	static ContextActionMAA* _instance;
};

/* SAA Get Profile */
class ContextActionSAAGetProfile : public ContextAction
{
public:
	virtual ~ContextActionSAAGetProfile(){};
	static ContextActionSAAGetProfile* getInstance();
	static void destory();
private:
	ContextActionSAAGetProfile();
	static ContextActionSAAGetProfile* _instance;
};

/* SAA Register */
class ContextActionSAARegister : public ContextAction
{
public:
	virtual ~ContextActionSAARegister(){};
	static ContextActionSAARegister* getInstance();
	static void destory();
private:
	ContextActionSAARegister();
	static ContextActionSAARegister* _instance;
};

/* S6b SAA Update Pdn Info */
class ContextActionS6bSAAUpdatePdnInfo : public ContextAction
{
public:
	virtual ~ContextActionS6bSAAUpdatePdnInfo(){};
	static ContextActionS6bSAAUpdatePdnInfo* getInstance();
	static void destory();
private:
	ContextActionS6bSAAUpdatePdnInfo();
	static ContextActionS6bSAAUpdatePdnInfo* _instance;
};

/* AAR */
class ContextActionS6bAAR : public ContextAction
{
public:
	virtual ~ContextActionS6bAAR(){};
	static ContextActionS6bAAR* getInstance();
	static void destory();
private:
	ContextActionS6bAAR();
	static ContextActionS6bAAR* _instance;
};



#endif /* CONTEXTACTION_H_ */
