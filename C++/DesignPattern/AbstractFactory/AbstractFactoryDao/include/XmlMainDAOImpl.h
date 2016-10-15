/*
 * XmlMainDAOImpl.h
 *
 *  Created on: Oct 15, 2016
 *      Author: eliwech
 */

#ifndef XMLMAINDAOIMPL_H_
#define XMLMAINDAOIMPL_H_

#include "OrderMainDAO.h"

class XmlMainDAOImpl : public OrderMainDAO
{
public:
	XmlMainDAOImpl();
	virtual ~XmlMainDAOImpl();
	virtual void saveOrderMain();
};

#endif /* XMLMAINDAOIMPL_H_ */
