#!/usr/bin/python2.7
# For deployment option, please see last line in this file
import requests
from optparse import OptionParser
import sys
import logging
import os

class file_downloader:
    def __init__(self):
        self.url = None
        self.file_source = None
    
    def get_and_write(self, options):    
        self.file_source = os.getcwd()            
        
        try:            
            with open(self.file_source+"/"+options.source) as f:
                for line in f:
                    self.url = line.rstrip("\n")          
                    response = requests.get(self.url,timeout=10)                             
                    if response:             
                        dest_filename =  self.url.rsplit('/', 1)[1]
                        open(self.file_source+"/"+dest_filename, 'wb').write(response.content)
                    else:
                        print("An error occurred while reading from source --> ",response.status_code)            
        except Exception as e:
            print( e)

def main():

    parser = OptionParser()
    parser.add_option("-s", "--source", dest="source", metavar="SOURCE FILE",
                      help="supply a file name to read from (REQUIRED)")
    
    (options,args) = parser.parse_args()

    if not options.source:
        parser.print_help()
        logging.debug('Invalid configuration options')
        sys.exit(1)
        
    f_d = file_downloader()
    f_d.get_and_write(options)

if __name__ == "__main__":
    main()


# For deployment on debian machines, i would set up a cronjob with this Entry
# This can be rolled out using any configuration management tool like puppet
# For the puppet setup you'd need a to either create a profile file(then include this class in an already defined profile class),
# for the script, or easier add the script config to an existing profile.
# Say added to an existing profile, these few lines can be added to the profile
## ------------------------------------------------ 
#   file { '/usr/local/bin/picker.py':
#       mode   => '0755',
#       source => "puppet:///modules/$module_name/folder/picker.py",
#    }
# ------------------------------------------------
# Assumption is that this puppet server has been setup with all necessary resources and python libraries or required dependencies.
# ----- Crontab config in an existing profile class  -------
#   cron::crond { 'file_downloader':
#     command   => '/usr/local/bin/picker.py',
#     ensure    => present,
#     minute    => '5',
#     hour      => "",
#     weekday   => "",
#  }

# --------------------------------------- crontab entry when deployed on nodes  -----
# */5 * * * * /path/to/this/script.py
