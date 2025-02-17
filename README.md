This is a placeholder at the moment, I will update README instructions when full code has been compiled.
I just went in below and added some stuff about how to make it works, feel free to change it however you want.

Requirements
============
-Python 3
-Pygame
-Psycopg2
-PostgreSQL

How to Install Dependencies
===========================
On the Debian Virtual Machine that already has PostgreSQL open the terminal.
In the terminal type 'sudo apt-get install python3' to install python.
You can then verify the installation by entering 'python3 --version' and then 'pip3 --version'.
Pygame should install with python3, if not enter 'pip3 install pygame'. This will also server as a check for if it is installed.
Psycopg2 will not come with python3, enter 'pip3 install psycopg2' to install it.

How to Run
==========
Download main.py, database.py, udp_server.py, and logo.jpg.
In a terminal go to the directory you installed the downloaded the files to.
Start the server by entering 'python3 udp_server.py'. This defaults to 0.0.0.0 to listen on all interfaces on port 7501.
To start the server on a specific IP and Port enter 'python3 udp_server.py 127.0.0.1 5000'. The IP address still hass to be assigned to your machine.
On a separate terminal go to the same directory.
Start the application by entering 'python3 main.py'.

Testing
=======
udp_client is optional and can be used to test the UDP server separately.
