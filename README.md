# Download many files at once in google drive
Download folders in google drive with 10000+ files

When there are lots of files inside a single directory in google drive, it is annoying to download it directly by default zipping process.It is also difficult to just find a few files and download them.

This code can be used to download speicific files inside the directory using google drive API.

Steps to be followed:
1. Go to Google Cloud Console
2. Go to Google Drive APIs and Services
3. Register an app using Oauth Consent Screen
4. Get Credentials in the form of .json file (credentials.json). Add this file in the same folder where your code is located.
5. You might have to add yourself as a test user inside 'Audience' of OAuth Consent Screen.
6. Run this code after installing necessary dependencies.


*Create a new python 3.11 environment and install the following:
   
!pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
