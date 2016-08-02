#include "StringUtil.h"

std::string StringUtil::toLowerCase(std::string s)
{
    size_t i = 0;
    size_t len = s.size();

    while(i < len)
    {
        char c = s[i];

        if((c >= 'A') && (c <= 'Z'))
        {
            c += 32;
            s[i] = c;
        }

        i++;
    }

    return s;
}

std::string StringUtil::toUpperCase(std::string s)
{
    size_t i = 0;
    size_t len = s.size();

    while(i < len)
    {
        char c = s[i];

	if((c >= 'a') && (c <= 'z'))
	{
	    c -= 32;
	    s[i] = c;
	}

	i++;
    }

    return s;
}
