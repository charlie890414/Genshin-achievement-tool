import httplib2
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = './credential/client_id.json'
APPLICATION_NAME = 'Python OCR'


def get_credentials():
    credential_path = os.path.join(
        "./credential", 'google-ocr-credential.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run(flow, store)
        print('save credential in' + credential_path)
    return credentials


def recognize(imgfile, txtfile):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    mime = 'application/vnd.google-apps.document'
    res = service.files().create(
        body={
            'name': imgfile,
            'mimeType': mime
        },
        media_body=MediaFileUpload(imgfile, mimetype=mime, resumable=True)
    ).execute()

    downloader = MediaIoBaseDownload(
        io.FileIO(txtfile, 'wb'),
        service.files().export_media(fileId=res['id'], mimeType="text/plain")
    )
    done = False
    while done is False:
        _, done = downloader.next_chunk()

    service.files().delete(fileId=res['id']).execute()


if __name__ == '__main__':
    recognize('./debug/sample.png', './debug/output.txt')
