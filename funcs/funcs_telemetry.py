#module to perform error reporting
import requests, json
#/repos/:owner/:repo/issues
#https://developer.github.com/v3/issues/#create-an-issue

github_url = ""
data = json.dumps({'name':'test', 'description':'some test repo'})
r = requests.post(github_url)#, data, auth=())

print data
print r.json
