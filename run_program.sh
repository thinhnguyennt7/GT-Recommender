#Execute the main code

	UNIQUE_NAME="GT-Recommender"

echo "Compile and execute the program"

echo "Checking if the folder already exist"
if  [ "$(ls -A GT-Recommender)" ]
then
	echo "File exists"

	# Go to folder
	echo "Go to folder ${UNIQUE_NAME}"
	cd $UNIQUE_NAME
	if [ $? -ne 0 ]
	then
		echo "Error: unable to cd to directory $TEMP_DIR"
		exit 25
	fi
fi

echo "Run python3 recommender.py"
python3 recommender.py
if [ $? -ne 0 ]
then
	echo "Error: Can not execute the python file"
	exit 30
fi