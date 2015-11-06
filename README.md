###What?

A Python command line / menu driven quote creation experience for IBM SoftLayer. (SL)

An alternative to the quote generation process available variously at:
https://store.softlayer.com/configure
https://control.softlayer.com/

Functionality:
* Explore SL server 'packages' available to your SL account
* Explore SL server package mandatory & optional components
* Build a quote container, composed of one or more package containers
* Validate quote containers (can they generate quotes that SL will accept)
* Register quotes on the SL portal, for later approval / purchasing / deletion
* Download Pdf verion of existing quotes from SL portal

###Why?

Discussions suggest some users experience challenges or frustrations
to fit the publicly available solution into their work flow. This is an
experiment to investigate possible solutions.

###Prerequisites:

#####Python 2.x; version 2.7.x or later:
  * Most testing to date happened with 2.7.5
  * There are known issues with 2.6.6, possibly all 2.6.x and earlier

######For Windows:
https://www.python.org/downloads/windows/

######For Linux:
Since most distros ship with *a* version of Python, we assume you have
a supported version, or know how to get one.

#####Python pip: (or some other way to install the following Python packages)

######For CentOS 7.x you will need:
```
yum install epel-release
yum install python-pip
```
Other rpm based distros will need something similar.

######Debian based distros could be as simple as:
```
apt-get install python-pip
```

######For Windows:

    Included in the installer version 2.7.9+

    https://docs.python.org/2/whatsnew/2.7.html#pep-477-backport-ensurepip-pep-453-to-python-2-7
    http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows

#####Python importlib:

```
pip install importlib
```
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

#####SoftLayer API key:

  http://knowledgelayer.softlayer.com/procedure/retrieve-your-api-key

###Installation:

```
cd <some-dir>
git clone <this-repo>
cd <this-repo>
```
###Use:
```
export export SL_API_KEY=<YOUR-API-KEY>
export SL_USERNAME=<YOUR-SL-API-USERNAME>
python slquotecli.py
```
