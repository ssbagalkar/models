from apiclient import discovery
from httplib2 import Http
import oauth2client
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload
from pathlib import Path


PATH_TO_TRAIN_VIDEOS = './object_detection/test_video/walmart/input/'
def authorize():
    obj = lambda: None
    lmao = {"auth_host_name":'localhost', 'noauth_local_webserver':'store_true', 'auth_host_port':[8080, 8090], 'logging_level':'ERROR'}
    for k, v in lmao.items():
        setattr(obj, k, v)

    # authorization boilerplate code
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    # The following will give you a link if token.json does not exist, the link allows the user to give this app permission
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('./object_detection/utils/client_id.json', SCOPES)
        creds = tools.run_flow(flow, store, obj)
    return creds

def download(creds):
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    # if you get the shareable link, the link contains this id, replace the file_id below
    file_id = input("Enter the id in the shareable link here:\n")
    request = DRIVE.files().get_media(fileId=file_id)
    # replace the filename and extension in the first field below
    filename_in_drive = input("Enter the file name with extension here:\n")
    # check if filename already exists
    file_to_download = Path(PATH_TO_TRAIN_VIDEOS+filename_in_drive)
    if not file_to_download.is_file(): 
        fh = io.FileIO(filename_in_drive, mode='w')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
    else:
        print("File with same name already exists. File will not be downloaded.")
        

def download_from_gdrive():
    creds = authorize()
    download(creds)


download_from_gdrive()