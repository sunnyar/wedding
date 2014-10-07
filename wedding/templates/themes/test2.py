import os

for i in range(0, 33) :
    os.chdir('/home/sunnyarora07/wedding/wedding/templates/themes')
    os.popen('cp -r default premium_theme%s' % i)


for i in range(0, 33) :
    os.chdir('/home/sunnyarora07/wedding/wedding/templates/themes/premium_theme%s' % i)
    os.popen("grep -nr 'themes/default' . | cut -d':' -f1 | while read line; do sed -i 's#themes/default#themes/premium_theme%s#g' $line; done" % i)
    os.popen("grep -nr 'themes/theme0' . | cut -d':' -f1 | while read line; do sed -i 's#themes/theme0#premium_themes/premium_theme%s#g' $line; done" % i)
