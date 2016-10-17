/*
 * ExportDataModel.h
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#ifndef EXPORTDATAMODEL_H_
#define EXPORTDATAMODEL_H_

#include <string>

class ExportDataModel
{
public:
	ExportDataModel()
		: _productId(""), _price(0), _amount(0)
	{
	}

    double getAmount() const
    {
        return _amount;
    }

    double getPrice() const
    {
        return _price;
    }

    std::string getProductId() const
    {
        return _productId;
    }

    void setAmount(double amount)
    {
        _amount = amount;
    }

    void setPrice(double price)
    {
        _price = price;
    }

    void setProductId(std::string productId)
    {
        _productId = productId;
    }

private:
	std::string _productId;
	double _price;
	double _amount;
};

#endif /* EXPORTDATAMODEL_H_ */
