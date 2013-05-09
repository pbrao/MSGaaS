import json
import os
import requests


def main():
	"""docstring for main"""
	accessKey = os.environ['ACCESS_KEY']
	secretKey = os.environ['SECRET_KEY']
	tenantID = os.environ['TENANT_ID']
	token = getToken(accessKey, secretKey, tenantID)
	
	numMessages = 3
	queueName = "newqueuei4"
	
	if not queueExists(queueName, tenantID, token):
		print "Create queue"
		createQueue(queueName, tenantID, token)
	
	print " "
	print "***** Sending Messages to the Queue *****"
	for counter in range(1,numMessages):
		sendMessage(queueName, tenantID, token, counter)
	print " "
	print "***** Fetching Messages from the Queue *****"
	for counter in range(1,numMessages):
		getMessage(queueName, tenantID, token)
	

def sendMessage(queueName, tenantID, token, counter):
	endpoint = "https://region-a.geo-1.messaging.hpcloudsvc.com/v1.1/%s/queues/%s/messages" %(tenantID, queueName)
	
	headers = {"content-type": "application/json", "x-auth-token": token}
	
	body = '{"body": "From Python Script %s"}' %counter
	
	req = requests.post(endpoint, data=body, verify=False, headers=headers)

	print "#%s Message sent to queue" %counter

def getMessage(queueName, tenantID, token):
	endpoint = "https://region-a.geo-1.messaging.hpcloudsvc.com/v1.1/%s/queues/%s/messages" %(tenantID, queueName)
	
	headers = {"content-type": "application/json", "x-auth-token": token}
	
	req = requests.get(endpoint, verify=False, headers=headers)
	
	print req.text


def getToken(accessKey, secretKey, tenantID):
	endpoint = "https://region-a.geo-1.identity.hpcloudsvc.com:35357/v2.0/tokens"
	
	headers = {"content-type": "application/json"}
	
	body = '{"auth":{"apiAccessKeyCredentials":{"accessKey":"%s", "secretKey":"%s" }, "tenantId":"%s"}}' %(accessKey, secretKey, tenantID)
	req = requests.post(endpoint, data=body, verify=False, headers=headers)
	
	resp = json.loads(req.text)
	#print json.dumps(resp)
	token = resp["access"]["token"]["id"]
	#print token
	return token

def queueExists(queueName, tenantID, token):
	print "In queueExists"
	endpoint = "https://region-a.geo-1.messaging.hpcloudsvc.com/v1.1/%s/queues" %tenantID
	headers = {"content-type": "application/json", "x-auth-token": token}
	req = requests.get(endpoint, verify=False, headers=headers)
	resp = json.loads(req.text)
	queues = resp["queues"]
	for queue in queues:
		print queue["name"]
		if queueName == queue["name"]:
			return True
	return False
	
def createQueue(queueName, tenantID, token):
	endpoint = "https://region-a.geo-1.messaging.hpcloudsvc.com/v1.1/%s/queues/%s" %(tenantID, queueName)
	headers = {"content-type": "application/json", "x-auth-token": token}
	req = requests.put(endpoint, verify=False, headers=headers)
	print req.status_code
	print req.text
	print req.headers
	
	
if __name__ == '__main__':
	main()	