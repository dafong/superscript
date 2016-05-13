#!/bin/sh
# @Author: xinlei.fan
# @Date:   2015-07-16 10:51:12
# @Last Modified by:   xinlei.fan
# @Last Modified time: 2015-07-16 10:57:51

curl  http://proxy.com.ru/ | iconv -f gb2312 -t utf-8 | grep "<tr><b><td>" | sed 's/<\/td><td>/ /g'| awk '{print $2" "$3}'