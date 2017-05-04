# ODSC East 2017 - Creating Data Science Workflows (A Healthcare Use Case)

## Environment preparation
1. VirtualBox
	* Add Sandbox entry to your local machine's hosts file:
		* 127.0.0.1	sandbox.hortonworks.com
2. Hortonworks Sandbox (HDP 2.6)
	* After import of image, add port 6667 and 22 to the NAT port forwarding
	* From the command line (or by SSH after enabling port 22 forwarding; user: root; pass: hadoop), run: 
		```shell
		wget https://raw.githubusercontent.com/ComputationalHealth/odsceast17/master/0-prereqs/start_sandbox.sh
		./start_sandbox.sh
		```
	* SSH to the new docker container via web (http://127.0.0.1:4200) or SSH (127.0.0.1:2222), user: root; pass: hadoop
		```shell
		yum install python-pip (may need to run twice to get past repo outdates)
		pip install kafka hdfs
		wget https://raw.githubusercontent.com/ComputationalHealth/odsceast17/master/0-prereqs/.hdfscli.cfg
		```
	* Install NiFi in Sandbox via Ambari