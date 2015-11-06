#functions interacting with client filesystem

def pdfPickle(output_file_name_base, binary_obj):
    import pickle
    pickleFileName = "./SL-Quote-ID"+str(output_file_name_base)+".pdf"
    pickleFile = open(pickleFileName, 'wb')
    pickle.dump(binary_obj, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()
    return pickleFileName

def jsonGateway(action, file_name, data_object=None):
    import json
    if action=='save':
        with open(file_name, 'w') as fp:
            json.dump(data_object, fp)
    if action=='load':
        with open(file_name, 'r') as fp:
            return json.load(fp)

def enumFilesInDir(dataDir,fileExtention):
    import os
    fileList = []
    for dataFile in os.listdir(dataDir):
        if dataFile.endswith(fileExtention):
            fileList.append(dataFile)
    return fileList

def byteify(input):
#http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
