#env-checks.py module
import sys
    #needed for is_python_supported
import os
    #needed for is_api_key_in_env()

def args_check_suceed():
    if not (is_python_supported()):
        show_python_version_error_msg()
        return False
    if not (is_importlib_installed()):
        show_importlib_error_msg()
    if not (is_SoftLayer_installed()):
        #check if the SL python module is present
        show_SoftLayer_error_msg()
        if not (is_pip_installed()):
            show_pip_error_msg()
        return False
    if not (is_api_key_in_env()):
        show_api_env_warn_msg()

def show_python_version_error_msg():
    print
    print "Python version must be 2.6 or greater"
    print
    print "http://sldn.softlayer.com/article/python"
    print
    print "You will need to make a newer version available."

def show_importlib_error_msg():
    print
    print "Fatal issue importing importlib module."
    print
    print "You need to execute:"
    print
    print "pip install importlib"
    print
    print "or your platform's equivalent"
    print


def show_SoftLayer_error_msg():
    print
    print "Fatal issue importing SoftLayer module."
    print
    print "You need to execute:"
    print
    print "pip install SoftLayer"
    print
    print "or your platform's equivalent"
    print

def show_pip_error_msg():
    print "pip isn't currently installed."
    print "you will need to:"
    print
    print "yum install epel-release'"
    print "yum install python-pip"
    print
    print "or your platform's equivalent"
    print

def show_api_env_warn_msg():
    print
    print "SL_API_KEY and / or SL_USERNAME"
    print
    print "were not found in the environment"
    print

def is_python_supported():
    if sys.version_info < (2, 6, 0):
        return False
    else:
        return True

def is_importlib_installed():
    try:
        import importlib
        return True
    except:
        return False

def is_SoftLayer_installed():
    try:
        import SoftLayer
        return True
    except:
        return False

def is_pip_installed():
    try:
        import pip
        return True
    except:
        return False

def is_api_key_in_env():
    SL_API_KEY = str(os.environ['SL_API_KEY'])
    SL_USERNAME = str(os.environ['SL_USERNAME'])
    if SL_USERNAME == '' or SL_API_KEY == '':
        return False
    else:
        return True
