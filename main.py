from google.oauth2 import service_account
import googleapiclient.discovery

credentials = service_account.Credentials.from_service_account_file(
    'service-account.json',
    scopes=['https://www.googleapis.com/auth/business.manage']
)

client = googleapiclient.discovery.build(serviceName='mybusiness', version='v4', credentials=credentials)
# print(client)