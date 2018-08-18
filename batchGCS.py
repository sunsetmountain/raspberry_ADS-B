import os
import time
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials

dataDir = "/home/pi/rawData"
bucket_name = "bucketnamegoeshere"
keyfile = "/home/pi/enterYourKeyfileName.json" #change to your keyfile name

def upload_blob(fileList):

	credentialsJson = keyfile
	scopesList = ["https://www.googleapis.com/auth/storage"]
	credentialsObj = ServiceAccountCredentials.from_json_keyfile_name(
		credentialsJson,
		scopes = scopesList
	)

"""Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    for fileName in fileList:
      destination_blob_name = fileName
      source_file_name = dataDir + "/" + fileName
      
      blob = bucket.blob(destination_blob_name)
      blob.upload_from_filename(source_file_name)

      print('File {} uploaded to {}.'.format(
          source_file_name,
          destination_blob_name))
          
  return

def publishBatch(msgList):

	credentialsJson = "/home/pi/[keyfile].json"
	scopesList = ["https://www.googleapis.com/auth/pubsub"]
	credentialsObj = ServiceAccountCredentials.from_json_keyfile_name(
		credentialsJson,
		scopes = scopesList
	)

	pubsubClient = pubsub.Client(
		project="[projectName]"
	)

	topicName = "raw-adsb-data"
	topicObj = pubsubClient.topic(topicName)
        with topicObj.batch() as batchObj:
                for eachItem in msgList:
                        eachItem = eachItem.encode("utf-8")
                        batchObj.publish(eachItem)

	return


def loadList(fileList):
        msgList = []
        for fileName in fileList:
                filePath = dataDir + "/" + fileName
		with open(filePath) as fileObj:
                        fileContents = fileObj.read()
                        msgList.append(fileContents)

        return msgList


def main():
        while True:
          fileList = os.listdir(dataDir)
        	#msgList = loadList(fileList)
        	#print len(msgList)

                try:
                        if len(fileList) > 0:
                                uploadBlob(fileList)
                                for fileName in fileList:
                                        filePath = dataDir + "/" + fileName
                                        os.remove(filePath)
                        #if len(msgList) > 0:
                        #        publishBatch(msgList)
                        #        for fileName in fileList:
                        #                filePath = dataDir + "/" + fileName
                        #                os.remove(filePath)
                        else:
                                print "No messages to send..."
                        time.sleep(10)

                except KeyboardInterrupt:
                        quit()
                
                except Exception,e:
                        print "Encountered error..."
                        print e
                        continue


if __name__ == "__main__":
	main()
