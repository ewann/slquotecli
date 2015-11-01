#functions interacting with client filesystem

def pdfPickle(output_file_name_base, binary_obj):
    import pickle
    pickleFileName = "./SL-Quote-ID"+str(output_file_name_base)+".pdf"
    pickleFile = open(pickleFileName, 'wb')
    pickle.dump(binary_obj, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()
