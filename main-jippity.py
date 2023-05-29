import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from textblob import TextBlob

# Authenticate and obtain an API client
creds = None
if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
else:
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=["https://www.googleapis.com/auth/business.manage"])
    creds = flow.run_local_server(port=0)

api_client = build("mybusinessbusinessinformation", "v1", credentials=creds, static_discovery=False)

# Replace with your Google My Business account and location IDs
account_id = "your-account-id"
location_id = "your-location-id"

# Fetch the reviews
reviews = api_client.accounts().locations().reviews().list(parent=f"accounts/{account_id}/locations/{location_id}").execute()

# Analyze sentiment and respond to reviews
for review in reviews["reviews"]:
    user_name = review["reviewer"]["displayName"]
    num_of_stars_user_gave = review["starRating"]
    review_text = review["comment"]
    
    # Analyze sentiment using TextBlob
    sentiment = TextBlob(review_text).sentiment.polarity
    response = ""

    if sentiment > 0 and num_of_stars_user_gave >= 4:
        response = f"Thanks for the {num_of_stars_user_gave} stars, {user_name}! We hope you'll be back soon."
    else:
        missing_stars = 5 - num_of_stars_user_gave
        response = f"Sorry {user_name}, we couldn't give you a 5-star experience. What can we do to make up for the {missing_stars} stars?"

    # Reply to the review
    reply_body = {
        "comment": response
    }
    api_client.accounts().locations().reviews().reply(parent=f"accounts/{account_id}/locations/{location_id}/reviews/{review['reviewId']}", body=reply_body).execute()

