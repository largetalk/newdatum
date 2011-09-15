#!/bin/bash
CHECK_FILE=~/bin/updating.lock UPDATED_LOG=~/bin/updated.log UPDATED_RESULT=~/bin/updated.result
if [ -f $CHECK_FILE ]; then
	rm $CHECK_FILE
    export LC_CTYPE=en_US.UTF-8  
    echo `date` >> $UPDATED_LOG 
    echo `date` > $UPDATED_RESULT 
	cd /home/saybot/workspace/vworld_client/branches/2.0-dev/source/main/resources/
	svn cleanup >>$UPDATED_LOG 2>>$UPDATED_LOG
	svn up 
	rsync -av --delete --exclude "*.fla" --exclude ".svn" --exclude "* *" --exclude "*'*" --exclude "Thumbs.db"  /home/saybot/workspace/vworld_resources/swf/default /home/saybot/workspace/vworld_client/branches/2.0-dev/source/main/resources/swf/
	rsync -av --delete --exclude "*.fla" --exclude ".svn" --exclude "* *" --exclude "*'*" --exclude "Thumbs.db"  /home/saybot/workspace/vworld_resources/sub_app/newsTv /home/saybot/workspace/vworld_client/branches/2.0-dev/source/main/resources/sub_app/
    cat /var/log/samba/audit.log.tmp | sort | uniq > ~/bin/audit.log.tmp && > /var/log/samba/audit.log.tmp
	cd /home/saybot/workspace/vworld_client/branches/2.0-dev/source/main/resources/swf/default
	svn status | grep ? | awk {'print $2'} | xargs svn add 
	svn status | grep ! | awk {'print $2'} | xargs svn rm 
	svn commit -F ~/bin/audit.log.tmp --username leon.li --password 771024  1>>$UPDATED_LOG 1>>$UPDATED_RESULT 2>>$UPDATED_LOG
    ~/bin/email_update ~/bin/audit.log.tmp 2>>$UPDATED_LOG

	cd /home/saybot/workspace/vworld_client/branches/2.0-dev/source/main/resources/sub_app/newsTv
	svn status buttons/ | grep ? | awk {'print $2'} | xargs svn add 
	svn status buttons/ | grep ! | awk {'print $2'} | xargs svn rm 
	svn status newsResource/ | grep ? | awk {'print $2'} | xargs svn add 
	svn status newsResource/ | grep ! | awk {'print $2'} | xargs svn rm 
	svn status npcMovie/ | grep ? | awk {'print $2'} | xargs svn add 
	svn status npcMovie/ | grep ! | awk {'print $2'} | xargs svn rm 
	svn commit buttons/  newsResource/  news_config.cfg  npcMovie/ -F ~/bin/audit.log.tmp --username leon.li --password 771024  1>>$UPDATED_LOG 1>>$UPDATED_RESULT 2>>$UPDATED_LOG
    ~/bin/email_update ~/bin/audit.log.tmp 2>>$UPDATED_LOG

	svn commit /home/saybot/workspace/vworld_client/branches/2.0-dev/source/main/resources/operation_control.txt -F ~/bin/audit.log.tmp --username leon.li --password 771024  1>>$UPDATED_LOG 1>>$UPDATED_RESULT 2>>$UPDATED_LOG
    ~/bin/email_update ~/bin/audit.log.tmp 2>>$UPDATED_LOG

    touch $CHECK_FILE
fi

#!/bin/bash
netstat -anp | grep ":3000.*LISTEN" | awk '{print $7}' | sed -e "s/\/.*//" | xargs kill -9
source /usr/local/rvm/scripts/rvm
rvm use 1.9.2-p180
bundle install
nohup script/rails server -e production &



