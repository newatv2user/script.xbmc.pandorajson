'''
Created on Jun 1, 2012

@author: newatv2user
'''
import urllib2

HTTP_TIMEOUT = 30

def JsonGetURL(Url, postData=None, Opener=None):
    #print 'JsonGetURL:'
    #print 'Url: ' + Url
    #print 'postData: ' + postData
    req = urllib2.Request(Url, postData, {'Content-Type': 'application/json'})
    if Opener:
        u = Opener.open(req, timeout=HTTP_TIMEOUT)
    else:
        u = urllib2.urlopen(req)
    resp = u.read()
    u.close()
    return resp
    
