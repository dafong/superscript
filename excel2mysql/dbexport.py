# coding=utf-8
# rszip.py
# @author yin.li
# @date 2013-05-14
# @update henry.sha 2013-05-14


# -*- coding:utf-8 -*-
t={}
t[u'武将表']='tbl_general'
t[u'兵种表']='tbl_general_type'
t[u'兵种进阶表']='tbl_general_type_rebirth'
t[u'法术表']='tbl_magic'
t[u'法术类型表']='tbl_magic_type'
t[u'武将法术表']='tbl_general_magic'
t[u'装备类型表']='tbl_equip_type'
t[u'装备表']='tbl_equip'
t[u'装备效果表']='tbl_equip_effect'
t[u'装备效果类型表']='tbl_equip_effect_type'
t[u'技能表']='tbl_skill'

t[u'道具表']='tbl_props'
t[u'道具类型表']='tbl_props_type'
t[u'AI类型表']='tbl_ai_type'
t[u'战役表']='tbl_mission_war'
t[u'战斗表']='tbl_battle'
t[u'战斗剧情表']='tbl_battle_plot'
t[u'战斗敌人表']='tbl_battle_enemy'
t[u'战斗友军表']='tbl_battle_allian'
t[u'战斗玩家阵容表']='tbl_battle_player'
t[u'战斗胜败条件表']='tbl_battle_condition'
t[u'战斗胜败条件类型表']='tbl_battle_condition_type'
t[u'战斗奖励表']='tbl_battle_bonus'
t[u'战斗副本敌人表']='tbl_battle_fuben_enemy'
t[u'天气类型表']='tbl_weather'

from optparse import OptionParser

import os, json, zipfile, datetime, shutil, hashlib, ConfigParser,codecs,xlrd,sys,re,xlwt,zlib

__help = '''usage %prog [options]'''
__parser = OptionParser(__help)
__parser.add_option('-e', '--engine', dest = 'engine', help = 'engine', action = 'store', default = 'sqlite3')
__parser.add_option('-i','--input',dest='input',help='input config file',action='store',default='config.xlsx')
__parser.add_option('-m','--map',dest='map',help='input map file',action='store',default='map.xlsx')
__parser.add_option('-o','--output',dest='output',help='output resource directoty',action='store',default='data')
     
if __name__ == '__main__':
    options, args = __parser.parse_args()
    basedir = os.path.split(os.path.realpath(__file__))[0]
    config = t
    
    wb = xlrd.open_workbook(os.path.join(basedir,options.input))
    print("check the config.xlsx and db_import_config:")
    sheets = wb.sheets()
    for i in range(1,len(sheets)):
        sh = sheets[i]
        print(sh.name + "=>" + (config.get(sh.name) if config.get(sh.name) else "None"))
        if config.get(sh.name)==None: 
            print("check Fail:" + sh.name + "is None config")
            exit()
            
    temp = {}                
    for i in range(1,len(sheets)):
        sh = sheets[i]        
            
        trow = sh.row(0)
        table_name = config.get(sh.name)
       
        temp[table_name]={}
        temp[table_name]['rows']=['id']
        temp[table_name]['col_index']=[]
        temp[table_name]['datas']=[]
        temp[table_name]['name2id']={}
        temp[table_name]['fk']={}
        columnstr=""
        nameindex=-1
        index=0
        for j in range(0,len(trow)):
            regex=re.compile('.+\((.+?)(\|(.+))?\)')
            mr = regex.match(trow[j].value)
            if mr:
                column_name = mr.group(1,3)[0]
                foreign_table=mr.group(1,3)[1]
                if column_name=="name":
                    nameindex=j
                    
                
                if column_name==None:
                    continue 
                if foreign_table==None:
                    index=index+1
                    columnstr=columnstr+column_name+' | '
                    temp[table_name]['rows'].append(column_name)
                    temp[table_name]['col_index'].append(j)
                    
                else:
                    index=index+1
                    columnstr=columnstr+column_name+"=>"+foreign_table+' | '
                    temp[table_name]['col_index'].append(j)
                    temp[table_name]['rows'].append(column_name)
                    temp[table_name]['fk'][index]=foreign_table
                    
        #print('\n'+table_name+'('+str(len(temp[table_name]['rows']))+' colums):')                        
       # print("| id | "+columnstr)
       # print( temp[table_name]['fk'])
        ##print(nameindex) 
        for j in range(1,sh.nrows):
            row = sh.row(j)
            datarow=[j]
 
            for k in temp[table_name]['col_index']:
                cell = row[k]
                
                datarow.append(cell.value)
                if nameindex!=-1 and nameindex==k:
                   temp[table_name]['name2id'][cell.value]=j 
 
            temp[table_name]['datas'].append(datarow)   
        ##print(temp[table_name]['datas'])
        ##print(temp[table_name]['name2id'])
        
    ##solve the foreign key data,if some data can't find the parent ,raise error and exit
    print("\ncheck and update foreign key data...")
    for tname in temp:
        print("check and update table " + tname) 
        for rowdata in temp[tname]['datas']:
            for colindex in range(0,len(rowdata)):   
                ftable = temp[tname]['fk'].get(colindex)
                if ftable!=None:            
                    if rowdata[colindex] != "":
                        if temp[ftable]['name2id'].get(rowdata[colindex]) == None:
                            
                            print('warning: Foreign Key : data:'+rowdata[colindex]+" can't find in table: "+ftable)
                            rowdata[colindex]=-1
                            #exit()
                        else:    
                            rowdata[colindex]=temp[ftable]['name2id'].get(rowdata[colindex])
                    else:
                       rowdata[colindex]=-1 
            
                    
    #for tname in temp:
     #   print(tname) 
     #   print(temp[tname]['datas']) 
    print(str(len(temp))+" tables \nready to generate export.xls...")
    ewb=xlwt.Workbook(encoding="utf-8")               
    for tname in temp:
        ws=ewb.add_sheet(tname,cell_overwrite_ok=True)
        for col in range(0,len(temp[tname]['rows'])):
            ws.write(0,col,temp[tname]['rows'][col])
        index = 0    
        for drow in temp[tname]['datas']:
            index=index+1
            for col in range(0,len(temp[tname]['rows'])):
                ws.write(index,col,drow[col])
                
    ewb.save(os.path.join(basedir,options.output) + "/export.xls")             
    print("generate export.xls success!") 
    
    print("ready to generate sql:") 
    f = codecs.open(os.path.join(basedir,options.output)+'/data.sql', 'w', 'utf-8')
    if options.engine=='mysql':       
       print("set autocommit=0;")
       f.write("set autocommit=0;\n")
    elif options.engine=='sqlite3':
        print("begin;")
        f.write("begin;\n")
    for tname in temp:
        print("\ndelete from `"+tname+"`;")
        f.write("\ndelete from `"+tname+"`;\n")
        for r in temp[tname]["datas"]:
            sql="insert into `"+tname+"` ("
            for i in range(len(temp[tname]['rows'])):
                sql=sql+"`"+temp[tname]['rows'][i]+"`,"
            sql = sql[:-1]
            sql = sql + ") values ("
           
            for c in r:
                if type(c) is str or type(c) is unicode:
                    if not c:
                        sql=sql+"null,"
                    else:  
                        sql = sql + "'" +(re.sub(r'\'','\\\'',c))+"',"
                else:
                    if not c:
                        sql = sql + "'0',"
                    else:
                        sql = sql + "'" + str(int(c))+"',"
    
            sql = sql[:-1]
            sql = sql + ");"
            print(sql)    
            f.write(sql+"\n")
    print("generate config sql complete!")     
    f.write("commit;")
 
 
    print("\ncheck the map.xlsx")
    f = codecs.open(os.path.join(basedir,options.output)+'/map.sql', 'w', 'utf-8')    
    f.write("begin;\n")
    wb = xlrd.open_workbook(os.path.join(basedir,options.map))
    f.write("\ndelete from `tbl_battle_map`;\n")
    print("\ndelete from `tbl_battle_map`;\n")
    sheets = wb.sheets()
    configsheet = sheets[0]
    maps = {}
    for i in range(1,configsheet.nrows):
        row   = configsheet.row(i)        
        name  = row[0].value
        width = int(row[1].value)
        height= int(row[2].value)
        maps[name]={'width':width,'height':height}    
    
    for i in range(1,len(sheets)):
        sh   = sheets[i]
        name = sh.name
        sql="insert into `tbl_battle_map` (battle_id,width,height,data) values("
        if maps.get(name)!=None:
            array=[]
            h=maps.get(name)['height']
            w=maps.get(name)['width']
            for r in range(0,h):
                colarray=[]
                row = sh.row(r)
                for c in range(0,w):
                    colarray.append(int(row[c].value))  
                array.append(colarray)
            
            idv=temp['tbl_battle']['name2id'].get(name)
            if idv!=None:
                sql = sql + "'"+str(idv)+"',"+"'"+str(w)+"',"+"'"+str(h)+"',"+"'"+json.dumps(array)+"');\n"
            else:
                print("error can't find battle name in tbl_battle")
                continue
        f.write(sql)        
        print(sql)
    f.write("commit;")                
    print("generate map sql complete!")

        
   
                    
            
                    
                    
                              
            
                
            
        
        

    
    
    
    
    
    
    
    
    
    
    
    
        
    