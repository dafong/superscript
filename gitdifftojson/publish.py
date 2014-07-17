# publish.py
# -*- coding:utf-8 -*-
# @autor fxl

from optparse import OptionParser

import os, json, zipfile, datetime, shutil, hashlib, ConfigParser,codecs,sys,re,zlib,commands
from jinja2 import  Environment, PackageLoader, Template



def getDiffFilesFromRivision(base_version,git_path):
    files = []
    cmd   = 'git diff %s master  --name-status -- %s' % (base_version,git_path)
    (status,output) = commands.getstatusoutput(cmd)
    if status == 0:
        for line in output.split('\n'):
            (type,filepath) = line.split('\t')
            if type == "A" or type == "M" or type == "D":
                files.append({ "type" : type , "path":filepath})
            else:
                print "unknow type of git diff: %s" % type
                sys.exit()
            
            for file in files:
                if file["type"] == "A" or file["type"]  == "M":
                    path         = os.path.join(basedir,file["path"])
                    file["size"] = os.path.getsize(path)
                else:
                    file["size"] = 0
    return files

__help = '''usage %prog [options]'''
__parser = OptionParser(__help)
__parser.add_option('-p','--template',dest='template',help=u'template file 模板文件',             action='store',default='iphone_test.tpl')
__parser.add_option('-d','--path',    dest='path',    help=u'git diff path 执行git diff的路径',   action='store',default='.')
__parser.add_option('-b','--base',    dest='base',    help=u'the base version(tag or commit) 基于git的哪个Tag或Commit进行比较',action='store',default='test')
__parser.add_option('-o','--output',  dest='output',  help=u'output directoty 输出目录',          action='store',default='data')
__parser.add_option('-s','--srcver',  dest='srcver',  help=u'src version 源版本号',               action='store',default='1.0.0')
__parser.add_option('-t','--target',  dest='tarver',  help=u'tar version 目标版本号',              action='store',default='1.0.1')

if __name__ == '__main__':
    options, args = __parser.parse_args()
    basedir       = os.path.split(os.path.realpath(__file__))[0]
    base_version  = options.base
    git_path      = options.path
    template      = options.template
    out_path      = os.path.join(basedir,options.output,template)
    src_ver       = options.srcver
    tar_ver       = options.tarver
    
    env = Environment(loader=PackageLoader('publish', 'template'))
    print'''
    *********************************************************************
    *
    *                     版本Json生成工具
    * ==请注意所使用的 模板路径 及基于的版本Tag 以及原版本号和目标版本号==
    *     
    *        template     = %s
    *        git_path     = %s
    *        base_version = %s
    *        src_ver      = %s
    *        tar_ver      = %s
    *        out_path     = %s
    *
    *
    *********************************************************************
    ''' % (template,git_path,base_version,src_ver,tar_ver,out_path)
    raw_input("press any key to continue....")
    
    
    files = getDiffFilesFromRivision( base_version , git_path)
    print'''
    *********************************************************************
                            文件变化列表
                      Git: from (%s) to (%s)
                      Ver: from (%s) to (%s)
    *********************************************************************
    ''' % (base_version,"master",src_ver,tar_ver)
    totalsize = 0
    for file in files:
        print "%s   %12s byte  %4.1sKB  %s" % (file["type"] , file["size"] ,file["size"]/1024, file["path"])
        totalsize = totalsize + file["size"]
    print "TotalSize: %sKB" % (totalsize/1024)
    raw_input("\npress any key to continue....\n")
    
    
    template    = env.get_template(template)
    output_json = template.render(files=files, is_show=3, src_ver=src_ver , dst_ver=tar_ver , total_size=totalsize)
    decodejson  = json.loads(output_json)
    print u'''
    *********************************************************************
                            输出Json预览
    *********************************************************************
    '''
    print(output_json)
    #json.dumps(decodejson,indent=2)
    raw_input("press any key to continue....")
    
    
    #path example ./{out_path}/{template}/version_{src_ver}_to_{tar_ver}.json
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    fn = os.path.join(out_path,("version_%s_to_%s.json" % (src_ver,tar_ver)))
    vf = open(fn,'w')
    #vf.write(json.dumps(decodejson,indent=2))
    vf.write(output_json)
    vf.close()
    print "Json file generate successfull to %s" % fn
    