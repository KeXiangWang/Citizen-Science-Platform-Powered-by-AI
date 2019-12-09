if false; then
for f in `ls event`
do
    mv event/$f event/$f.bak
    cp loading.png event/$f
done
fi


if true; then
for f in `ls cause`
do
    mv cause/$f cause/$f.bak
    cp loading.png cause/$f
done
fi


