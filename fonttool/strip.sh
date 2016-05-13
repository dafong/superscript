#!/bin/sh

base=$(pwd)
[[ $# < 2 ]] && cat << _EOF_ && exit 0
    usage:
        sh strip.sh characters_txt input_font_ttf
_EOF_
charfile=$1
input_font=$2
[[ ! -f $charfile ]] && echo "characters_txt not exist" && exit 0
[[ ! -f $input_font ]] && echo "input_font_ttf not exist " && exit 0
output_font_name=$(basename -s .ttf $input_font)
output_font_name="${output_font_name}_striped.ttf"
characters=$(cat $charfile)
charcount=$(wc -m $charfile | awk '{ print $1 }')
cat << _EOF_
# ---------------------------TTF Glyphs Strip Script-------------------------
#  charfile   $charfile
#  charcount  $charcount
#  inputfont  $input_font
#  outputfont $output_font_name
# ---------------------------------------------------------------------------
_EOF_
read -p "Press any key to continue..."
java -jar sfnttool.jar -s "$characters" $input_font output/$output_font_name
