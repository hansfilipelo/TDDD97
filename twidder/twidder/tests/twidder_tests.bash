#!//bin/bash

db_file="database.sdb"

# Setup environment
rm -f ../$db_file
sqlite3 $db_file < ../database.sql # Due to bug in sqlite3 I can't put file directly under twidder
mv $db_file ../ # Move to correct location

# cd to server dir and run server
cd ../..
./runserver.py &
pid=$!

# cd back to test dir and run tests
cd twidder/tests
python ./twidder_tests.py

kill $pid
