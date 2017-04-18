cd ~/Agnes_AutoSpiders/AUTO_EVENT_SPIDERS/
for dir in `ls .`
 do
   if [ -d $dir ]
   then
     echo $dir
     cd $dir
     python main.py
     cd ..
   fi
done