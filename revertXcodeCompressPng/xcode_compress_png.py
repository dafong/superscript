# coding=utf-8
# revert_xcode_compress_png.py
# @athor fxl
# @date 2014-03-20

from optparse import OptionParser

import os,shutil

__help = '''usage %prog [options]'''
__parser = OptionParser(__help)
__parser.add_option('-i','--input',dest = 'input',action='store',default='input')
__parser.add_option('-o','--output',dest ='output',action='store',default='output')
__parser.add_option('-r','--revert',dest ='revert',action='store',default='true')


def dealImgInDir(dir,outputdir,isRevert):

    if not os.path.exists(outputdir):
        print("out is " + outputdir)
        os.makedirs(outputdir)
    if os.path.exists(dir):
        for d in os.listdir(dir):
            childpath = os.path.join(dir,d)
            out = os.path.join(outputdir,d)
            if os.path.isdir(d):
                dealImgInDir(childpath,out,isRevert)
            else:
                if os.path.splitext(childpath)[1]==".png":
                    revertopt = ' -revert-iphone-optimizations' if isRevert else ''
                    cmd       = "xcrun -sdk iphoneos pngcrush"+revertopt+" -q "+childpath+" " +os.path.join(outputdir,d)
                    os.system(cmd)
            
if __name__=='__main__':
    options,args = __parser.parse_args()
    basedir = os.path.split(os.path.realpath(__file__))[0]
    dealImgInDir(os.path.join(basedir,options.input),os.path.join(basedir,options.output),options.revert=="true")