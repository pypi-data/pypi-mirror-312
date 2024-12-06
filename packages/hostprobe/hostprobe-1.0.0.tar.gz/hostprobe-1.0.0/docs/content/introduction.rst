:orphan:

Introduction
============================

*The sole maintainer/writer of this project is malachi196*

About
----------------------------

Hostprobe strives to be a minimal cross-platform toolkit for networking. It uses the
built-in python socket module to extract info from a network, such as if a 
device is online, or all the online devices on your network. Hostprobe should
have the capabilities of nmap, while being completely cross system, and in python.

.. code-block::

    >>> from hostprobe import netprobe  
    >>> onlinehosts = netprobe("192.168.0.1") #returns a list  
    >>> print(f"some online hosts: {onlinehosts}")  
    ["192.168.0.1", "192.168.0.7"]

Network mapping in python
----------------------------------------------------

Hostprobe enables anyone to easily check a variety of network stats, from which devices are online
on their network, to individual device statistics. Alternatively,
hostprobe can be used to output to the terminal, similar to shell commands (such as nmap), except in python.
Hostprobe aims to provide an easy interface, with the most control possible over how
you hope to probe your network.


Cross system
----------------------------------------------------
Another good aspect of hostprobe is the fact that it is as cross-system as possible. This insures
that your network needs will be fulfilled, whether using Windows, MacOs,
Raspberrypi OS on an ARM64 device, and more!

.. note::

    This project is meant to be a cross-system network
    probing toolkit, although **confirmed operating systems** are:

    * Windows
    * MacOS
    * Linux (debian distros)
    * Unix-based

    ARM64 machines (with a similar distro) are also supported
