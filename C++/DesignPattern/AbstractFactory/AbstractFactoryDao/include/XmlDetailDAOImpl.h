/*
 * XmlDetailDAOImpl.h
 *
 *  Created on: Oct 15, 2016
 *      Author: eliwech
 */

#ifndef XMLDETAILDAOIMPL_H_
#define XMLDETAILDAOIMPL_H_

#include "OrderDetailDAO.h"

class XmlDetailDAOImpl : public OrderDetailDAO
{
public:
	XmlDetailDAOImpl();
	virtual ~XmlDetailDAOImpl();
	virtual void saveOrderDetail();
};

#endif /* XMLDETAILDAOIMPL_H_ */
