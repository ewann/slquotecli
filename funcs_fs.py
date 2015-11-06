#functions interacting with client filesystem

def pdfPickle(output_file_name_base, binary_obj):
    import pickle
    pickleFileName = "./SL-Quote-ID"+str(output_file_name_base)+".pdf"
    pickleFile = open(pickleFileName, 'wb')
    pickle.dump(binary_obj, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()
    return pickleFileName

def jsonGateway(action, file_name, data_object):
    data = None
    if action='save':
        with open(file_name, 'w') as fp:
            json.dump(data, fp)
    if action='load':
        with open(file_name, 'r') as fp:
            data = json.load(fp)
