#SLquoteCli

##What?

A command line / menu driven quote creation utility for IBM SoftLayer. (SL)

An alternative to the financial quote process available via:

https://control.softlayer.com/

https://store.softlayer.com/configure

#####Functionality:
* Explore SL server 'packages' available to your SL account
* Explore SL server package mandatory & optional components
* Build a quote container, composed of one or more package containers
* Validate quote containers (can they generate quotes that SL will accept)
* Locally save quote containers, and reload them later
* Register quotes on the SL portal, for later approval / purchasing / deletion
* Download Pdf version of existing quotes from SL portal

***
##Why?

Some users find it difficult to fit the publicly available
solution into their work flow. In one case an organization has built
an intranet replacement, but this doesn't interface directly with
the SL api. As a consequence, selected indicative quotes
must be re-keyed into the SL ordering solution.

This repo hosts an *experiment* to investigate other possible solutions.

#####Requirements cited as missing from the SL solution & provided here:
* Ability to save quote components for later *editing* & rapid resubmission
* Ability to generate / iterate / finalize quotes quickly

***
##Prerequisites:

#####Python 2.x; version 2.7.x or later:
  * Most testing to date happened with 2.7.5
  * The first version of the walk through slides used 2.7.10
  * There are known issues with 2.6.6, possibly all 2.6.x and earlier

######For Windows:
https://www.python.org/downloads/windows/

######For Linux:
Since most distros ship with *a* version of Python, we assume you have
a supported version, or know how to get one.

***
#####Python pip: (or some other way to install the following Python packages)

######CentOS 7.x:
```
yum install epel-release
yum install python-pip
```
Other rpm based distros will need something similar.
Check the documentation for your distro.

######Debian:
```
apt-get install python-pip
```
Or check the documentation for your distro.

######Windows:

Included in the installer, version 2.7.9+

https://docs.python.org/2/whatsnew/2.7.html#pep-477-backport-ensurepip-pep-453-to-python-2-7

http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows

***
#####Python importlib:

```
pip install importlib
```

***
#####Python SoftLayer:

```
pip install SoftLayer
```

or:

```
git clone https://github.com/softlayer/softlayer-python.git
cd softlayer-python
python setup.py install
```
***
#####Git:
######CentOS 7.x:
```
yum install git
```
Other rpm based distros will need something similar.
Check the documentation for your distro.

######Debian:
```
apt-get install git
```
Or check the documentation for your distro.

######Windows:

https://git-scm.com/download/win
***
#####SoftLayer API key:

http://knowledgelayer.softlayer.com/procedure/retrieve-your-api-key

***
##Install:

```
cd <some-dir>
git clone https://github.com/ewann/slquotecli.git
cd slquotecli
```

***
###Use:
####Linux:
```
export SL_API_KEY=<YOUR-API-KEY>
export SL_USERNAME=<YOUR-SL-API-USERNAME>
echo $SL_USERNAME
python slquotecli.py
```
####Windows:
```
set SL_API_KEY=<YOUR-API-KEY>
set SL_USERNAME=<YOUR-SL-API-USERNAME>
echo %SL_USERNAME%
python slquotecli.py
```

***
##Walkthrough:

* Quickstart walkthrough - https://github.com/ewann/slquotecli/blob/master/walkthrough-quick.pdf

* Full Walkthrough - https://github.com/ewann/slquotecli/blob/master/walkthrough-full.pdf

***
######Markdown aided by: https://github.com/joeyespo/grip
