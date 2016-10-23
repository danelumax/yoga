/*
 * Dep.h
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#ifndef DEP_H_
#define DEP_H_

#include <string>

class Dep
{
public:
	Dep();
	virtual ~Dep();
    std::string getDepId() const;
    std::string getDepName() const;
    void setDepId(std::string depId);
    void setDepName(std::string depName);
    void deleteDep();
private:
	std::string _depId;
	std::string _depName;
};

#endif /* DEP_H_ */
