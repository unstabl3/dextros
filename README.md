# dextros
# Version 1.0(beta)
A command line password cracking utility which works on a cluster(HPC).

# Why this tool?
This is our project which was presented during our final's.

Dextros is password cracking tool which works on cluster environment with currently supported upto 10 nodes(1 master + 9 slaves).
**will be adding support for more nodes in future**.

To know more about how to setup a cluster read this,

[https://medium.com/@the_unstable/build-your-own-cluster-with-rocks-os-f198dd994129](url)

# Still have a problem?

Connect with me here
[https://twitter.com/chaskar_shubham](url)


Now I would recommend to update your cluster and install python3 if it is not installed.

# Screenshot

![dpc](https://user-images.githubusercontent.com/48474764/68997824-c20be280-08d0-11ea-8815-49001ba57936.png)

# Tested only on rocks os.

# Installation

`git clone https://github.com/unstabl3/dextros.git`

 `cd dextros`
 
 `chmod +x dextros.py`
 
 `pip3 install -r requirements.txt`

# How to use

`python3 dextros.py`

# What you need?

1) A hash to crack
2) A good dictionary in the case of dictionary attack.

# Note

Make sure in your cluster all your nodes are up and working.

that is from compute-0-0 to compute-0-9 should be up and running if fails program will not work.

# ToDo
1) multithreading support
2) more support for cluster nodes.(i.e,from compute-1-0 and so on).
3) More reliability( If one node fails other should take his workload).

# Contributers
@rohithbieber

# Credits
1) **Manu zacharia** for giving us this project and suggesting a way to do so.
2) **vaibhav yadav** for suggesting the name.

# Want to contribute
Do a pull request.
any suggestion/feedback is appreciable! :3 :)

# License

dextros is licensed under the GNU Affero General Public License v3.0

# Disclaimer
Author is not responsible for how you use this tool.
