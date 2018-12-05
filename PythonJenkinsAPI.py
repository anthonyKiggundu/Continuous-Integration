#!/usr/bin/python2.7
# @author: 

from jenkinsapi.jenkins import Jenkins
import urllib
import urllib2
import sys
import json
import urllib3
import socket
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Let us disable some un-necessary warning output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class jenkins_job:
    def __init__(self):
        self.jenkins_server = None  
        self.build_status = None      
        self.job_name = None
        self.job_desc = None
        self.jenkins_user = "jenkins_user"      
        self.token = "users_jenkins_token"
        
    def get_server(self,jenkins_server_ip): 
        
        self.jenkins_server = "http://"+jenkins_server_ip
        
        try:
            response = Jenkins(self.jenkins_server, username=self.jenkins_user, password=self.jenkins_pass,ssl_verify=False, timeout=90) # password=self.token, ssl_verify=False, timeout=90)#, ssl_verify=False, timeout=30)
            
        except urllib3.exceptions.SSLError as e:
            print ("SSL Error:", e)
            return -1
        
        return response
         
    """Get job details of each job that is running!! """
    def get_job_details(self,response, jenkins_server_ip):
        
     
        failed_builds = []
#        aborted_builds = []
        bool_build = False 
        success_builds = []
        self.jenkins_server = "http://"+jenkins_server_ip+"/job/"       
        
        for job_name, job_instance in response.get_jobs():
            self.job_name = job_instance.name 
            if "puppet" in self.job_name:
                self.build_status = job_instance.is_running()                                 
                if self.build_status:
                    status = 0
                    perfdata = "This job -->", self.job_name," is still RUNNING"
                    print status, "Jenkins_Status" , " - ", perfdata
                    sys.exit(3)
                else:
                    try:
                        jenkinsStream   = urllib2.urlopen( self.jenkins_server + self.job_name + "/lastBuild/api/json" )
                    except urllib2.HTTPError, e:                    
                        continue
                              
                    try:
                        buildStatusJson = json.load( jenkinsStream )
                    except:
                        print "Failed to parse json"
                        sys.exit(3)
                
                    if buildStatusJson["result"] != "SUCCESS" and buildStatusJson["result"] != "ABORTED" :               
                        bool_build = True
                        failed_builds.append(self.job_name)
                    else:
                        success_builds.append(self.job_name)
                        
      # Arrays contain duplicates that need to be gotten rid of,,                 
        success_builds = list(set(success_builds))       
        failed_builds = list(set(failed_builds))
        self.report_build_results(bool_build, failed_builds,success_builds )
         
            
    def report_build_results(self, bool_build, failed_builds,success_builds):
        
        if bool_build and len(failed_builds)>0:
            status = 2
            perfdata = "The following jobs FAILED --> ", failed_builds
            print status, "Jenkins_Status" , " - ", perfdata
            
        else:
            status = 0
            perfdata = "No jobs were found to have failed. These jobs --> ",success_builds, " completed SUCCESSFULLY"
            print status, "Jenkins_Status" , " - ", perfdata
            
                 
def main():
# We are interested in the host's IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    s.connect(('8.8.8.8', 1))
    local_ip_address = s.getsockname()[0] 
          
    job = jenkins_job()
    response = job.get_server(local_ip_address)
    
    if response:
        job.get_job_details(response, local_ip_address)    
        
if __name__ == "__main__":
    main()
  
