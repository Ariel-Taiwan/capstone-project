#my_string = "{"_id":{"$oid":"62ce60ab1efb8a3612e22d99"},"urls":"https://www.ptt.cc/bbs/hotboards.html","indomain":1,"layer":"1","category":"8"}
#"

#for i in my_string:
 #   if my_string.find('"8"}'):
  #      index= my_string.find('"8"}')
   #     index += 5
    #    final_string = my_string[:index] + ',' + my_string[index:]
     #   print(final_string)

fo = open("cat8_insert.csv", "r")
print("文件名为: ", fo.name)

#寫入cat8.csv
path = 'cat8.csv'
f = open(path, 'w')
#f.write('Hello World')

for line in fo.readlines():                          #依次读取每行  
    line = line.strip()  #去掉每行头尾空白
    index= line.find('"8"}')
    index += 5
    final_string = line[:index] + ',' + line[index:]
    f.write(line[:index] + ',\n' )
    #print(final_string)
 
# 关闭文件
fo.close()
f.close()

