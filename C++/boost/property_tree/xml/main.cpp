//============================================================================
// Name        : xml.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <string>
#include <vector>
#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/optional/optional.hpp>
#include <boost/assign.hpp>

/* using aaa/diameter/server/diameter_swi/UnitAttributes.xml */
const std::string xmlFile = "UnitAttributes.xml";

std::vector<std::string> attrVec = boost::assign::list_of
		("type")
		("name")
		("id");


void recursionLoad(std::string ptreeName,boost::property_tree::ptree pt)
{
	bool flag = false;
	std::vector<std::string>::iterator it = attrVec.begin();
	for(; it!=attrVec.end(); it++)
	{
		std::string xmlattr = "<xmlattr>." + *it;
		/* check if xmlattr node exist */
		boost::optional< boost::property_tree::ptree& > child = pt.get_child_optional(xmlattr);
		if( child )
		{
			flag = true;
			std::cout << "\n" << ptreeName << " " <<*it << ": "<<pt.get<std::string>(xmlattr) << std::endl;
			break;
		}
	}

	/* skip empty data, skip target with <xmlattr>, skip target with children */
	if(!pt.data().empty() && flag == false && pt.empty())
	{
	    std::cout << ptreeName << " " << "value: " <<pt.data() << std::endl;
	}

	/* if target have children */
	if (!pt.empty())
	{
		boost::property_tree::ptree::iterator iter = pt.begin();
		for(; iter!=pt.end(); iter++)
		{
			/* skip <xmlattr> target */
			if(iter->first == "<xmlattr>")
			{
				continue;
			}
			/* recursion */
			recursionLoad(iter->first, iter->second);
		}
	}
	else
	{
		return;
	}
}

void simpleLoad(boost::property_tree::ptree pt)
{
	/* get CdfUnit attribute "type" */
	std::vector<std::string>::iterator it = attrVec.begin();
	for(; it!=attrVec.end(); it++)
	{
		std::string xmlattr = "<xmlattr>." + *it;
		boost::optional< boost::property_tree::ptree& > child = pt.get_child_optional(xmlattr);
		if( child )
		{
			std::cout << *it << ": "<<pt.get<std::string>(xmlattr) << std::endl;
		}
	}

	if (!pt.empty())
	{
		boost::property_tree::ptree::iterator iter = pt.begin();
		/* traverse all target under CdfUnit, and each iter is a target, such as Identity,Description */
		for(; iter!=pt.end(); iter++)
		{
			if(iter->first == "<xmlattr>")
			{
				continue;
			}
			/* each iter is a pair, first=target name(string), second=target ptree */
			if (iter->first == "Identity")
			{
				boost::property_tree::ptree Identity, identity, name, version;
				std::string identityStr, nameStr, versionStr;
				/* get Identity prtree */
				Identity = iter->second;

				/* get "identity" child ptree */
				identity = Identity.get_child("identity");
				if(!identity.data().empty())
				{
				    std::cout << "Node have value" << std::endl;
				}
				/* get data "SWI/DIAMETER"*/
				identityStr = identity.data();
				std::cout << identityStr << std::endl;

				name = Identity.get_child("name");
				nameStr = name.data();
				std::cout << nameStr << std::endl;

				version = Identity.get_child("version");
				versionStr = version.data();
				std::cout << versionStr << std::endl;

			}
		}
	}
}

int main()
{
	boost::property_tree::ptree pt, CdfUnit;
	/* load xml */
	read_xml(xmlFile, pt);
	/* using string "CdfUnit" to get CdfUnit target */
	CdfUnit = pt.get_child("CdfUnit");

	recursionLoad("CdfUnit", CdfUnit);

	simpleLoad(CdfUnit);
	return 0;
}
