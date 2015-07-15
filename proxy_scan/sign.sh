#!/bin/sh
# @Author: xinlei.fan
# @Date:   2015-05-28 17:07:03
# @Last Modified by:   xinlei.fan
# @Last Modified time: 2015-06-03 12:01:52
USER_AGENT="User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN"
ORIGIN="Origin:http://wefire.qq.com"
COOKIE="Cookie:access_token=OezXcEiiBSKSxW0eoylIeF2YIPexlSaSH6asSwuByHLJN3HPV4q1vlA2uUiTQNi8zQ9mcpKoFYcskTWXbzBt51rDKZjuoX9MJLcVrKZhNHLppLSjB8CX40wkMKFLvUkiMoGPDO_jKQTRT_AwgAkHQw; acctype=wx; appid=wx21d9c743f261c238; openid=o4v4Cj88xnCHg8iS2jJBqNNCyaD4; pgv_info=pgvReferrer=&ssid=s4957331744; pgv_pvid=8570326706"
data=$(curl -H "${USER_AGENT}" -H $ORIGIN  -H "${COOKIE}" -X POST -d "appid=wx21d9c743f261c238&gameId=&sArea=1&iSex=&sRoleId=&iGender=&sPlatId=0&sPartition=2006&sServiceType=wefire&isSignToday=1&continuousSignDays=1&objCustomMsg=&areaname=&roleid=&rolelevel=&rolename=&areaid=&iActivityId=18859&iFlowId=137471&g_tk=1842395457&sServiceDepartment=lzm3" "http://apps.game.qq.com/ams/ame/ame.php?ameVersion=0.3&sServiceType=wefire&iActivityId=18859&sServiceDepartment=newterminals&set_info=newterminals&_=1432805423501" &2>/dev/null)

errorcode=$(python -c "import json;re=json.loads('$data');print re['ret']")

[[ "$errorcode" == "600" ]] && echo "已经签到" && exit
[[ "$errorcode" == "100" ]] && echo "签到成功" && exit
[[ "$errorcode" == "101" ]] && echo "设备未登录" && exit
echo "其它错误 代码$errorcode"




