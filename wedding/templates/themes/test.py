import os

for i in range(1, 31) :
    os.chdir('/home/sunnyarora07/wedding/wedding/templates/themes')
    os.popen('cp -r default theme%s' % i)


for i in range(1, 31) :
    os.chdir('/home/sunnyarora07/wedding/wedding/templates/themes/theme%s' % i)
    os.popen("grep -nr 'themes/default' . | cut -d':' -f1 | while read line; do sed -i 's#themes/default#themes/theme%s#g' $line; done" % i)
    os.popen("grep -nr 'theme0' . | cut -d':' -f1 | while read line; do sed -i 's#theme0#theme%s#g' $line; done" % i)
