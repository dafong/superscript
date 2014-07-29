#!/bin/bash
cat <<- _EOF_
#----------------------------------------------------------------------------
#                          三国传奇二进制包打包及分发工具
#feature:
#       1. build app
#       2. package ipa
#       3. upload to the server of ethernet
#
#---------------------------------------------------------------------------
_EOF_

project_path=$(pwd)
build_path=${project_path}/build

function doexit {
	echo "Script exited！T_T"
}


function isneedclean {
	cat <<- _EOF_
是否需要Clean?
0. YES
1. NO	
2. Return Parent
_EOF_
    read -p "Enter selection [0-2] >"
    if [[ $REPLY =~ ^[0-2]$ ]]; then
		if [[ $REPLY == 0 ]]; then
			xcodebuild clean || doexit
		fi
		if [[ $REPLY == 1 ]]; then
			echo ""
		fi
		if [[ $REPLY == 2 ]]; then
			main
		fi
	else
		echo "ohhhhhh~ there is no option you input!!"
		isneedclean
	fi
    return
}
#待加configuration 检测 因为要根据configuration 去找build出来的app的目录
function getConfiguration {
	read -p "which Configuration you want to use:>"
	if [[ "$REPLY" == "" ]]; then
		getConfiguration
	else
		build_config=$REPLY
	fi
	return	
}
#待加target 检测 列出来 让我选
function getTarget {
	 xcodebuild -list
	 read -p "whitch Target you want to use:>"
	 if [[ "$REPLY" == "" ]]; then
		 getTarget
	 else
		 build_target=$REPLY
	 fi	 
	 return 
}

function buildProject {
    getTarget && getConfiguration
	
	build_cmd='xcodebuild -configuration '${build_config}' -target '${build_target}
	
	cat <<- _EOF_
############################################################
#
#    Ready to Build
#    target: ${build_target}
#    config: ${build_config}
#    
#    ${build_cmd}
#
#############################################################
_EOF_
	sleep 2
	$build_cmd 
	if [[ $? == 0 ]]; then
		echo "=================>Build Successful!"
	else
		echo "=================>Build failed!"
		doexit
	fi
}


function package {
 	isneedclean
	
	buildProject
	
	appdirname=${build_config}'-iphoneos'
	app_name=$(basename ${build_path}/${appdirname}/*.app)
	app_infoplist_path=${build_path}/${appdirname}/${app_name}/Info.plist
	#echo $app_infoplist_path
	app_version=$(/usr/libexec/PlistBuddy -c "print CFBundleShortVersionString" ${app_infoplist_path})
	#echo $app_version
	app_build_version=$(/usr/libexec/PlistBuddy -c "print CFBundleVersion" ${app_infoplist_path})
	#echo $app_build_version
	ipa_name="${build_target}_${app_version}_${build_config}${app_build_version}_$(date +"%Y%m%d")"
	#echo $ipa_name
	pkg_cmd="xcrun -sdk iphoneos PackageApplication -v $build_path/${appdirname}/*.app -o ${build_path}/ipa/${ipa_name}.ipa "
cat <<- _EOF_
############################################################
#
#    准备打包
#    target        : ${build_target}
#    config        : ${build_config}
#    version       : ${app_version}
#    build-version : ${app_build_version}
#    ipad-name     : ${ipa_name}
# 
#    ${pkg_cmd}
#
#############################################################
_EOF_
	sleep 2
	$pkg_cmd 
	if [[ $? == 0 ]]; then
		echo "=================>ipa  package Successful!"
		main
	else
		echo "=================>ipa  package failed!"
		doexit
	fi	
}

function sendPackage2Server {
	#list the ipa file names
	cd "${build_path}/ipa"
	#input the ipa name
	ls -lhAt | grep *.ipa | less
	read -p "Please ipa name you want to upload:>"
	if [[ -f "$REPLY" ]]; then
		scp $REPLY root@server:/var/www/sites/demo.mojolegend.com/packages
		if [[ $? == 0 ]]; then
			echo "=================>ipa upload Successful!"
			cd ..
			main
		else
			echo "=================>ipa upload failed!"	
			doexit
		fi	
	else
		echo "In valide file"
		sendPackage2Server
	fi
	return
}


function main {

    cat <<- _EOF_
Hi guys, what do you want

0. I want to package an ipa file
1. I want send the ipa to the vcs server
2. exit script
_EOF_

    read -p "Enter selection [0-2] >" 
    
    if [[ $REPLY =~ ^[0-2]$ ]]; then
        if [[ $REPLY == 0 ]]; then
            package
			return
        fi
        if [[ $REPLY == 1 ]]; then
            sendPackage2Server
			return
        fi
		if [[ $REPLY == 2 ]]; then
			doexit
			return
		fi
    else
        echo "ohhhhhh~ there is no option you input!!"
		main
    fi
	return
}

main