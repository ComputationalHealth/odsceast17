# ODSC East 2017 - Creating Data Science Workflows (A Healthcare Use Case)

## Environment preparation
1. VirtualBox
	* Add Sandbox entry to your local machine's hosts file:
		* 127.0.0.1	sandbox.hortonworks.com
2. Hortonworks Sandbox (HDP 2.6)
	* After import of image, add port 6667 and 22 to the NAT port forwarding
	* From the command line (or by SSH after enabling port 22 forwarding; user: root; pass: hadoop), run: 
		```shell
		curl -o start_sandbox.sh https://raw.githubusercontent.com/ComputationalHealth/odsceast17/master/0-prereqs/start_sandbox.sh
		./start_sandbox.sh
		chmod 755 start_sandbox.sh
		```
	* SSH to the new docker container via web (http://127.0.0.1:4200) or SSH (127.0.0.1:2222), user: root; pass: hadoop
		```shell
		yum install python-pip (may need to run twice to get past repo outdates)
		pip install kafka hdfs
		curl -o .hdfscli.cfg https://raw.githubusercontent.com/ComputationalHealth/odsceast17/master/0-prereqs/.hdfscli.cfg
		```
	* Install NiFi in Sandbox via Ambari
	* Make sure Kafka broker is started (or go to Service Actions -> Start if in Stopped status)

## Host Configuration
* If you want to run the IPython Notebooks to generate the normally distributed data, you will need a Python environment with matplotlib, pandas, and the kafka library. To create a conda environment with these dependencies:
	```shell
	conda create --n odscHealth python=3
	activate odscHealth
	conda install notebook ipykernel matplotlib pandas
	pip install kafka
	jupyter notebook --notebook-dir=/path/to/git/repo
	```