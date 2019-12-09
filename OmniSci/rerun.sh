while true

do

ps -ef | grep "python manage.py" | grep "80" | grep -v "grep"

if [ "$?" -eq 1 ]

then

python manage.py runserver 0.0.0.0:80 --insecure

echo "process has been restarted!"

else

echo "process already started!"

fi

sleep 20

done
