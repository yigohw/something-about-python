import shutil
home = input("文件位置：")
id = input("av号：")
n = int(input("集数："))
for i in range(n):
    i = str(i+1)
    sub = home + '\\' + i
    name = id + '_' + i + '_0.mp4'
    shutil.move(sub+'\\'+name, home)
