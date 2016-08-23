//============================================================================
// Name        : xml.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <string>
#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>

/* using aaa/diameter/server/diameter_swi/UnitAttributes.xml */
const std::string xmlFile = "UnitAttributes.xml";

int main()
{
	boost::property_tree::ptree pt, CdfUnit;
	read_xml(xmlFile, pt);
	/* using string "CdfUnit" to get CdfUnit target */
	CdfUnit = pt.get_child("CdfUnit");
	/* get CdfUnit attribute "type" */
	std::string CdfUnitStr = CdfUnit.get<std::string>("<xmlattr>.type");
	std::cout << CdfUnitStr << std::endl;

	boost::property_tree::ptree::iterator iter = CdfUnit.begin();
	/* traverse all target under CdfUnit, and each iter is a target, such as Identity,Description */
	for(; iter!=CdfUnit.end(); iter++)
	{
		/* each iter is a pair, first=target name(string), second=target ptree */
		if (iter->first == "Identity")
		{
			boost::property_tree::ptree Identity, identity, name, version;
			std::string identityStr, nameStr, versionStr;
			/* get Identity prtree */
			Identity = iter->second;

			/* get "identity" child ptree */
			identity = Identity.get_child("identity");
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
	return 0;
}
