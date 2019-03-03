#!/bin/sh


# Default value
	PYTHON_VERSION=3.7.0
	GIT_URL="https://github.com/thinhnguyennt7/GT-Recommender.git"
	UNIQUE_NAME="GT-Recommender"
	CODE_DIR="$DOWNLOAD_DIR/$$"
	BRANCH="master"
	TEMP_DIR=""


# Install python if need
echo "Check if python exist or not, otherwise install"
if command -v python3 &>/dev/null; then
    echo "**Python 3 has installed**"
else
	# Install GCC
    yum install gcc openssl-devel bzip2-devel

    # Download Python
	wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz

	# Extract download archive using tar command
	tar xzf Python-3.7.0.tgz

	# Open the folder
	cd Python-3.7.0

	# Install Python 27 to linux system
	./configure --enable-optimizations
	make altinstall

	# Remove the zip file
	rm Python-3.7.0.tgz

	# Check verions
	python --version
fi


# Install pip3 if need
echo "Check if pip3 exist or not, otherwise install pip3"
if command -v pip3; then
	echo "pip3 has installed"
else
	apt install python3-pip
	pip3 --version
fi


# Check if the folder has not exist in the directory
echo "Checking if the folder already exist"
if  [ "$(ls -A GT-Recommender)" ]
then
	echo "File exists"

	# Go to folder
	echo "Go to folder ${TEMP_DIR}"
	cd $UNIQUE_NAME
	if [ $? -ne 0 ]
	then
		echo "Error: unable to cd to directory $TEMP_DIR"
		exit 25
	fi

	# Pull the lastest version from master branch
	echo "Pull the lastest update"
	git pull origin master
	if [ $? -ne 0 ]
	then
		echo "Error: Can not pull the lastest from github"
		exit 50
	fi
else
	# Download the lastest code
	echo "Downloading latest code $UNIQUE_NAME"
	git clone $GIT_URL
	if [ $? -ne 0 ]
	then
	   echo "Error: unable to download code for branch $BRANCH to current directory"
	   exit 22
	fi

	#Run pip to install package if needed"
	echo "Install package in requirements.txt if need"
	pip install requirements.txt
	if [ $? -ne 0 ]
	then
		echo "Package already installed"
		exit 29
	fi
fi


#Execute the main code
echo "Run python3 recommender.py"
python3 recommender.py
if [ $? -ne 0 ]
then
	echo "Error: Can not execute the python file"
	exit 30
fi
