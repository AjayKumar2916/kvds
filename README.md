# Key-Value Data Store
A file-based key-value data store that supports the basic CRD (create, read and delete) operations.
## Usage

    import KVDS

    # Initializing the class with filename and filepath,
    # if filepath is not specified the json file will save
    # into current working directory
    kvds = KVDS(filename=FILE_NAME, filepath=FILE_PATH)

    #To creating new key-value
    kvds.create(KEY, VAULE)

    #To creating new key-value with ttl(ttl in seconds)
    kvds.create(KEY, VAULE, 300)

    #To read a value
    kvds.read(KEY)

    #To delete a key-value
    kvds.delete(KEY)
