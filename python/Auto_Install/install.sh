#!/bin/bash
version=''
echo "IPWorks Auto-Install Tool Installation information:"
packet_name="IPW_AutoInstall"

packet_path=`pwd`
#packet_path="${packet_path}/${packet_name}.tgz"
packet_path="${packet_path}/${packet_name}"
echo "    Install packet: ${packet_path}"

install_path=`echo ~`
target_path="${install_path}/${packet_name}"
#echo -e "\033[34;1m    Install target: ${target_path}\033[0m"

if [ -d ${target_path} ]; then
    echo "      Already exist: ${target_path}"
    rm -rf ${target_path} 
fi

cd ${install_path}
#tar -zxf ${packet_path}
cp -r ${packet_path} .
chmod -R +w ${target_path}
mkdir -p ${target_path}/log

echo -e "\033[34;1m    Install target: ${target_path}\033[0m"
cat /mnt/x86-linux/utils/version.txt | grep "REVISION"  > /version.txt
while read line
do
      str1=${line#*=}
      str2=${str1%;*}
      version+=$str2
      version+="."
done < /version.txt
version=${version%.*}
rm -rf /version.txt
sed -i "s/###/$version/g" ${target_path}/healthcheck.json
echo "Install compeleted !"
