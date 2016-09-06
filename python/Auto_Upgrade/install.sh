#!/bin/bash

echo "IPWorks Auto-Upgrade Tool Installation information:"
packet_name="IPW_AutoUpgrade"

packet_path=`pwd`
#packet_path="${packet_path}/${packet_name}.tgz"
packet_path="${packet_path}/${packet_name}"
echo "    Install packet: ${packet_path}"

install_path=`echo ~`
target_path="${install_path}/${packet_name}"
#echo -e "\033[34;1m    Install target: ${target_path}\033[0m"

if [ -d ${target_path} ]; then
    echo "      Already exist: ${target_path}"
    date_time=`date "+%F_%T"`
    echo "      Move it to ${target_path}.${date_time}"
    mv ${target_path} "${target_path}.${date_time}"
fi

cd ${install_path}
#tar -zxf ${packet_path}
cp -r ${packet_path} .
chmod -R +w ${target_path}
mkdir -p ${target_path}/log

echo -e "\033[34;1m    Install target: ${target_path}\033[0m"
echo "Install completed !"
