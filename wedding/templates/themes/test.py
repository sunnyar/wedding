import os

for i in range(1, 31) :
    #os.chdir('/home/sunnyarora07/wedding/wedding/templates/themes')
    os.chdir('/home/sunnyarora07/wedding/wedding/templates/themes/theme%s' % i)
    #os.popen('cp -r default theme%s' % i)
    os.popen("grep -nr 'Select Themes' . | cut -d':' -f1 | while read line; do sed -i 's#Select Themes#Themes#g' $line; done")


