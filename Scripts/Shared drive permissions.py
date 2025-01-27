from googleapiclient.discovery import build
from google.oauth2 import service_account

# Specify the path to your JSON service account key
SERVICE_ACCOUNT_FILE = 'D:\\Scripts\\gw-admin.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly']

# Autorization
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If delegation is used, specify the user's email
delegated_credentials = credentials.with_subject('admin@yourdomain.com')

# Initialization of API client
service = build('drive', 'v3', credentials=delegated_credentials)

# Get all Shared Drives
def list_shared_drives():
    shared_drives = []
    request = service.drives().list(pageSize=100)
    while request is not None:
        response = request.execute()
        shared_drives.extend(response.get('drives', []))
        request = service.drives().list_next(request, response)
    return shared_drives

# Get permissions for every Shared Drive
def list_permissions(drive_id):
    permissions = []
    request = service.permissions().list(fileId=drive_id, supportsAllDrives=True, fields='permissions')
    while request is not None:
        response = request.execute()
        permissions.extend(response.get('permissions', []))
        request = service.permissions().list_next(request, response)
    return permissions

# Print results
shared_drives = list_shared_drives()
for drive in shared_drives:
    print(f"Shared Drive: {drive['name']} (ID: {drive['id']})")
    permissions = list_permissions(drive['id'])
    for permission in permissions:
        print(f" - User: {permission.get('emailAddress', 'N/A')}, Role: {permission['role']}")
