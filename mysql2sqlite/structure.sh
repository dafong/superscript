#!/usr/bin/env bash
# 
# 
shellpath=`dirname $0`
mysql test<$shellpath/structure.sql
mysqldump --compatible=ansi --skip-extended-insert --compact test>$shellpath/structure/mysql_structure.sql
sh $shellpath/mysql2sqlite.sh $shellpath/structure/mysql/mysql_structure.sql>$shellpath/structure/sqlite3_structure.sql