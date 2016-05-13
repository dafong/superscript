require 'rubygems'
require 'roo'
require 'roo-xls'

needscan = {
    "物品总表" => ["G","I"],
    "技能信息" => ["D","G"],
    "任务城市" => ["B"]
}
s = Roo::Excelx.new("test.xlsx")
content=""
s.sheets.each do |sh|
    s.default_sheet=sh
    if needscan[sh]!=nil then
        needscan[sh].each do |c|
            7.upto(s.last_row) do |line|
                str=s.cell(line,c)
                if str!= nil then
                    content+=str
                end
            end
        end
    end
end
puts content

file=File::open("excel.txt","w")
file.write(content)
file.close
