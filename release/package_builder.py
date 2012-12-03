#!/usr/bin/env python
import glob
import sys
import os
from subprocess import call
#sys.path.append('../../../stage/lib')
#print os.listdir('./')
#print os.getcwd()

#from distutils.core import setup
#from ganga.distutils.config import setup

"""
Default distutils 'setup' method overwritten.
"""


#for root, dirs, files in os.walk('./'):
#  if '.svn' in dirs:
#      dirs.remove('.svn')
#  for filename in files:
#      data_files.append((root, [os.path.join(root,filename)]))

this_version = glob.glob('ThisTagVersion-*')[0].lstrip('ThisTagVersion-')
print "Building RPMs for Ganga version: " + this_version

os.chdir('../python')
packageDirs = glob.glob('Ganga[A-Z]*')
for p in packageDirs:
    if p.endswith('egg-info'):
        packageDirs.remove(p)    
#packageDirs = ['Ganga', 'GangaAtlas', 'GangaLHCb']


rpm_require_map = {
'Ganga' : "python >= 2.4.3",
'GangaAtlas' : "Ganga = "+this_version,
'GangaCamtology' : "Ganga = "+this_version,
'GangaCMS' : "Ganga = "+this_version,
'GangaGaudi' : "Ganga = "+this_version,
'GangaLHCb' : "Ganga = "+this_version,
'GangaPanda' : "Ganga = "+this_version,
'GangaPlotter' : "Ganga = "+this_version,
'GangaRobot' : "Ganga = "+this_version,
'GangaSAGA' : "Ganga = "+this_version,
'GangaService' : "Ganga = "+this_version,
'GangaSuperB' : "Ganga = "+this_version,
'GangaTest' : "Ganga = "+this_version,
'GangaTutorial' : "Ganga = "+this_version
}

egg_require_map = {
'Ganga' : ["python>=2.4.3"],
'GangaAtlas' : ["Ganga=="+this_version],
'GangaCamtology' : ["Ganga=="+this_version],
'GangaCMS' : ["Ganga=="+this_version],
'GangaGaudi' : ["Ganga=="+this_version],
'GangaLHCb' : ["Ganga=="+this_version],
'GangaPanda' : ["Ganga=="+this_version],
'GangaPlotter' : ["Ganga=="+this_version],
'GangaRobot' : ["Ganga=="+this_version],
'GangaSAGA' : ["Ganga=="+this_version],
'GangaService' : ["Ganga=="+this_version],
'GangaSuperB' : ["Ganga=="+this_version],
'GangaTest' : ["Ganga=="+this_version],
'GangaTutorial' : ["Ganga=="+this_version]
}





description_map = {
'Ganga' : 'The Core Ganga package', 
'GangaAtlas' : 'The Ganga ATLAS package',
'GangaCamtology' : 'The Ganga Camtology package',
'GangaCMS' : 'The Ganga CMS package',
'GangaGaudi' : 'The Ganga Gaudi package',
'GangaLHCb' : 'The Ganga LHCb package',
'GangaPanda' : 'The Ganga Panda package',
'GangaPlotter' : 'The Ganga Plotter package',
'GangaRobot' : 'The Ganga Robot package',
'GangaSAGA' : 'The Ganga SAGA package',
'GangaService' : 'The Ganga Service package',
'GangaSuperB' : 'The Ganga SuperB package',
'GangaTest' : 'The Ganga Testing package',
'GangaTutorial' : 'The Ganga Tutorial package'
}

long_desc_map = {}

for package in packageDirs:

    config_script = '''[global]
verbose         = 1
force-manifest  = 1

[sdist]
dist-dir        = /home/mkenyon/dist/src

[bdist]
dist-dir        = /home/mkenyon/dist/bin
plat-name       = noarch

[bdist_rpm]
dist-dir = /home/mkenyon/dist
vendor = "Ganga <project-ganga-developers@cern.ch>"
###REQUIREMENTS###

[install]
prefix = /opt/ganga/install/python
#install_data    = /opt/ganga/Ganga
install_lib     = /opt/ganga/install/python
compile         = 0
'''

    config_script = config_script.replace('###REQUIREMENTS###', 'requires = ' + rpm_require_map[package])
    conf_file = open('setup.cfg','w')
    print "Writing " + conf_file.name
    conf_file.write(config_script)
    conf_file.close()

    setup_script = '''#!/usr/bin/env python
import glob
import sys
import os
from setuptools import setup, find_packages

setup(
        #find all of the pythonic files
        ###PACKAGES###
        #and also things other than *.py, e.g. *.gpi, *.gpim etc
        include_package_data = True,

        #installation requirements relating to the egg distribution
        ###REQUIREMENTS###

        ###PACKAGENAME###

        ###THISVERSION###

        ###DESCRIPTION###
        description = 'Description goes here',

        ###LONG_DESCRIPTION###
        long_description = "Long description goes here",

        url = "http://ganga.web.cern.ch/ganga/",
        author = "The Ganga Project",
        author_email = "project-ganga-developers@cern.ch"
    )
'''

    filenames = []
    
    setup_script = setup_script.replace('###PACKAGES###', 'packages = ' + str([package])+',')
    #install_requires is a string or list of strings
    setup_script = setup_script.replace('###REQUIREMENTS###', 'install_requires = ' + str(egg_require_map[package])+',')
    setup_script = setup_script.replace('###PACKAGENAME###', 'name = \"' + package + '\",')
    setup_script = setup_script.replace('###THISVERSION###', 'version = \"' + this_version + '\",')

    setup_file = open('setup.py','w')
    print "Writing " + setup_file.name
    setup_file.write(setup_script)
    setup_file.close()


    call(["python setup.py bdist_rpm --post-uninstall ../release/postun-packages.sh"], shell=True)
