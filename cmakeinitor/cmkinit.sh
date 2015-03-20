#!/bin/sh
# @Author: fxl
# @Date:   2015-03-20 01:13:11
# @Last Modified by:   fxl
# @Last Modified time: 2015-03-20 01:43:32


if [[ "$(ls)" != "" ]]; then
	echo "the directory is not empty"
	exit 1
fi

read -p "Enter The Project Name:"
if [[ "$REPLY" == "" ]]; then
	echo "the project name can't be empty!"
	exit 1
fi
echo "create source folder ............. src"
echo "create build folder .............. build"
echo "create README file ............... README.md"
echo "create LICENSE file .............. LICENSE"
echo "create CMakeLists file ........... CMakeLists.txt"
mkdir src
mkdir build
touch README.md
touch LICENSE
touch CMakeLists.txt

PROJECT_NAME=$REPLY

cat > README.md << _EOF_ 
Project ${PROJECT_NAME}\'s README File 
_EOF_

cat > LICENSE << _EOF_

====

Copyright fanxl, Inc. and other Node contributors. All rights reserved.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

====
_EOF_
echo "Create main.c file ........... src/main.c"
touch src/main.c

cat > src/main.c << _EOF_
#include <stdio.h>
int main(int argc,char *argvs[]){
	printf("%s\n","hello world!");
}
_EOF_

cat > CMakeLists.txt << _EOF_
PROJECT (${PROJECT_NAME})
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
SET(SRC_LIST src/main.c)
ADD_EXECUTABLE(${PROJECT_NAME} \${SRC_LIST})
_EOF_

