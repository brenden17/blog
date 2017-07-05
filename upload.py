import httplib2
import urllib2
import os
from datetime import date
import calendar
import time
import tempfile
import sys
reload(sys)  
sys.setdefaultencoding('utf-8')

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.file' #create or upload file
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
#    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join('credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service

def get_list():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    service = get_service()
    
    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def download_sbs_radio_file():
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]
    dest_url = 'https://media.sbs.com.au/ondemand/audio/%s_ONDemand_SBS_RADIO1_21_00.mp3' % day#    r = requests.get(dest_url)
    filename = time.strftime("%d%m") + ".mp3"
    attempts = 0

    while attempts < 3:
        try:
            response = urllib2.urlopen(dest_url, timeout=65)
            content = response.read()
            f = open(filename, 'w')
            f.write(content)
            f.close()
            break
        except urllib2.URLError as e:
            attempts += 1
            print(e)

def upload_sbs_radio_file():
    service = get_service()
    filename = time.strftime("%d%m") + ".mp3"
    file_metadata = {
      'name' : filename,
      'mimeType' : 'audio/mpeg'
    }
    media = MediaFileUpload(filename,
                            mimetype='audio/mpeg',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    # remove file
    os.remove(filename)
    print ('Uploaded %s' % filename)

def main():
    download_sbs_radio_file()
    upload_sbs_radio_file()
#    print ('Uploaded')

if __name__ == '__main__':
    main()
