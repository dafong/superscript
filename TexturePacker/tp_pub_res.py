# rszip.py
# @author fxl
# @date 2013-05-14
# @update henry.sha 2013-05-14


# -*- coding:utf-8 -*-
from optparse import OptionParser

import os, json, zipfile, datetime, shutil, hashlib, ConfigParser

__help = '''usage %prog [options]'''
__parser = OptionParser(__help)
__parser.add_option('-o', '--output', dest = 'output', help = 'output directory', action = 'store', default = 'output/')
__parser.add_option('-i','--input',dest='input',help='input resource directoty',action='store',default='resources/')
__parser.add_option('-f','--force',dest='force',help='force publish resources',action='store',default='false')
__parser.add_option('-p','--publish',dest='publish',help='publish directory',action='store',default='./')
__parser.add_option('-s','--scale',dest='scale',help='scale factor',action='store',default='1') 
     
if __name__ == '__main__':
    options, args = __parser.parse_args()
    basedir = os.path.split(os.path.realpath(__file__))[0]
    
    output=os.path.join(basedir,options.output)
    input =os.path.join(basedir,options.input)
    temppath = os.path.join(basedir,'temp')
    pubpath = os.path.join(basedir,options.publish)
    config={}
    autosdpath = 'resources-ipadhd/'
    if options.scale == str(0.5) :
        autosdpath = 'resources-iphonehd/'
    if options.scale == str(0.25):
        autosdpath = 'resources-iphone/'        
    
    dfg = ConfigParser.ConfigParser()
    dfg.readfp(open(basedir+'/cfg.properties'))
    config['data-format'] = dfg.get('output','data-format')
    config['texture-format'] = dfg.get('output','texture-format')  
    config['paths']={}
    for k in dfg.items('paths'): 
        config['paths'][k[0]] = k[1]
        
    print "Base Dir:     " + (basedir)
    print "Input:        " + input     
    print "Output:       " + output
    print "Publish       " + pubpath 
    print "Configure:    cfg.properties"
    for k in config:
        if k!="paths":
            print(k+' = '+config[k])
    if not os.path.exists(output):
        os.makedirs(output)
    
    if not os.path.exists(temppath):
        os.makedirs(temppath)
    
    for d in os.listdir(input):
        filepath = os.path.join(input,d)
        if os.path.isdir(filepath):
            for cd in os.listdir(filepath):
                childpath = os.path.join(filepath,cd)
                if os.path.isdir(childpath):                
                    pathinconfig = d+'_'+cd
                    filetime = os.stat(childpath).st_mtime
                    #detect modified!!
                    tempdest = os.path.join(temppath,pathinconfig)
                    tempdest = os.path.join(tempdest,d)
                    if not os.path.exists(tempdest):
                        os.makedirs(tempdest)
                    tempresin = os.path.join(temppath,pathinconfig)    
                    if config['paths'].get(pathinconfig)!=str(filetime):
                        shutil.rmtree(os.path.join(tempdest,cd),True)
                        shutil.copytree(childpath,os.path.join(tempdest,cd))
                        dfg.set('paths',pathinconfig,filetime)
                    cmd='/usr/local/bin/TexturePacker --trim-mode None --scale '+options.scale+' --texture-format '+config['texture-format']+' --data "'+output+autosdpath+pathinconfig+'.plist" --main-extension "'+output+autosdpath+'"  --sheet "'+output+autosdpath+pathinconfig+'.png" "'+tempresin+'"'
                    os.system(cmd)  
                    
                    if options.force == 'true':
                        cmd='/usr/local/bin/TexturePacker --trim-mode None --scale '+options.scale+'  --texture-format '+config['texture-format']+' --data "'+pubpath+autosdpath+pathinconfig+'.plist" --main-extension "'+pubpath+autosdpath +'" --sheet "'+pubpath+autosdpath+pathinconfig+'.png" "'+tempresin+'"'
                        os.system(cmd) 
                     
    with open(basedir+'/cfg.properties','wb') as configfile:
        dfg.write(configfile)
    
    
    
    
        
    