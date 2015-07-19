#!/bin/sh
# @Author: fxl
# @Date:   2015-07-19 09:13:53
# @Last Modified by:   fxl
# @Last Modified time: 2015-07-19 20:15:30
[[ ! -f http_proxy.txt ]]  && touch http_proxy.txt
[[ ! -f socks_proxy.txt ]] && touch socks_proxy.txt
curl http://free-proxy-list.net | grep "<tr><td>" | sed "s/<[^>]*>/ /g"| awk '{ print "http "$1":"$2}' >> http_proxy.txt
curl http://www.socks-proxy.net | grep "<tr><td>" | sed "s/<[^>]*>/ /g"| awk '{ print "sock5 "$1":"$2}' >> socks_proxy.txt
for page in $(seq 1 5);do
	curl www.getproxy.jp/en/default/$page | grep text-align:left | sed -E 's/<[^>]+>/ /g' | sed 's/[[:space:]]//g' | awk '{ print "http "$1}' >> http_proxy.txt
done


