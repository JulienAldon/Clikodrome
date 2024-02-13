# Installation
Install python dependencies
```
pipenv install
```

You need to setup every environment variables present in configuration.py
- frontend_uri : Uri of this app front end
- public_uri : Uri of the backend
- jwt_origin : Microsoft app origin
- jwt_issuer : Microsoft app JWT issuer
- client_id : Azure Client ID
- client_secret : Azure Client Secret
- intranet_secret : Autologin
- db_host : Clikodrome Database Host
- db_user : Clikodrome Database User
- db_password : Clikodrome Database password
- database : Clikodrome Database name
- event_activity : Intranet Activity url to retreive sign sessions
- all_edusign_credentials : List of credential (if there is mutltiple account in charge of differents promotions)

# Deploy
- Backend : FastAPI using uvicorn and pipenv or hatch if you prefer
- FrontEnd : React classic build folder with nginx
- create_sessions : A systemd service
# Manual Usage
First create clikodrome sessions
```
[pipenv run python] create_sessions.py [-h] [--date DATE] hour
```
Then sign clikodrome sessions with the following command
```
[pipenv run python] sign_sessions.py [-h] [--date DATE] hour
```
**Date** format must be (*YYYY-MM-DD*) and **hour** format must be (*00:00:00.000*)

> In both cases if date is not specified it'll take today's date.

For now only two hours are recognized from edusign : 
- 07:30:30.000
- 15:30:00.000
They have been variabilized in case of later changes.

# Fully deployed usage
> If the tool is fully deployed what should I do ?

Every day Clikodrome sessions will be created automatically by the `create_sessions` script at a given hour. 

The pedago in charge of signing will connect using his microsoft account (he must be staff) to the deployed frontend and validate the session student list.

Once validated the `sign_sessions` script will be allowed to trigger. In fact the script will trigger every day at the same hour, the pedago must validate on the interface before the hour of signature.

Theses hours can be tweaked during the deployment process. We recommand to send the mail at the end of the school session (13h and 17h30).

# Actions of the tool
- Login To get SchoolID (request edusign)
- Get All sessions for a given date (edusign) (request )edusign
- Get All students for a given session (edusign) (request )edusign
- Get Presence List from intranet (json of intranet logins) (request intranet )
  - Filter out the "absent" students (logic)
- Append the remote students (csv of intranet logins) (request sharepoint)
- Create logins (intranet) and IDs (edusign) object {'login': 'test@epitech.eu', 'edusign_id': 'xzaazep13afr'} (logic)
- Send signature for session (request edusign)
- Send MassSendSignEmail (for each students in session object) (request edusign)

# Test

## Create test environment
```sh
docker-compose -f devops/docker-compose-test.yml up --build --renew-anon-volumes
```

## Execute backend integration tests
```sh
docker-compose -f devops/docker-compose-test.yml exec back_test python -m pytest
```