# -*- coding: utf-8 -*-

from os import getenv

import google.auth.exceptions
import google.oauth2.credentials
import google_auth_oauthlib.flow
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from flask_cors import CORS
from googleapiclient.discovery import build

load_dotenv()

CLIENT_SECRETS_FILE = getenv('CLIENT_SECRETS_FILE')
SCOPES = [
    'https://www.googleapis.com/auth/contacts.readonly',
    'https://www.googleapis.com/auth/userinfo.profile'
]
API_SERVICE_NAME = 'people'
API_VERSION = 'v1'
SCHEME_URL = 'https' if getenv('FLASK_ENV') == 'production' else 'http'

app = Flask(
    __name__,
    template_folder='./dist/',
    static_folder='./dist/static/')


app.secret_key = getenv('SECRET_KEY')
cors = CORS(app, resources={
            r'/api/*': {'origins': getenv('CORS_ORIGIN_LIST', '*')}})


@app.route('/api/emails')
def emails():
    if 'credentials' not in session:
        return {'code': 'FORBIDDEN'}, 403

    # Load credentials from the session.
    cred = google.oauth2.credentials.Credentials(
        **session['credentials']
    )

    all_emails = list()

    try:
        with build(API_SERVICE_NAME, API_VERSION, credentials=cred) as service:
            connections = list()
            nextPageToken = None
            stop = False

            while not stop:
                results = service.people().connections().list(
                    resourceName='people/me',
                    pageToken=nextPageToken,
                    pageSize=1000,
                    personFields='emailAddresses'
                ).execute()

                connections.extend(results.get('connections', []))
                nextPageToken = results.get('nextPageToken', None)
                stop |= nextPageToken is None

            def contain_email(person):
                return person.get('emailAddresses', [])

            for person in filter(contain_email, connections):
                emails = person.get('emailAddresses', [])
                if emails:
                    all_emails.extend(
                        map(lambda email: email.get('value'), emails)
                    )

            session['credentials'] = credentials_to_dict(cred)
    except google.auth.exceptions.RefreshError:
        del session['credentials']
        return {'code': 'FORBIDDEN'}, 403

    return {'emails': all_emails}


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'credentials' not in session:
            return {'code': 'FORBIDDEN'}, 403

        cred = google.oauth2.credentials.Credentials(
            **session['credentials']
        )

        try:
            with build(API_SERVICE_NAME, API_VERSION, credentials=cred) as service:
                profile = service.people().get(resourceName='people/me',
                                               personFields='names,photos'
                                               ).execute()
                display_name = profile.get('names')[0].get(
                    'displayName')
                photo = profile.get('photos')[0].get('url')

                session['credentials'] = credentials_to_dict(cred)
        except google.auth.exceptions.RefreshError:
            del session['credentials']
            return {'code': 'FORBIDDEN'}, 403

        return {
            'displayName': display_name,
            'photo': photo
        }
    else:
        if request.args.get('next'):
            session['next'] = request.args.get('next')

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES)

        flow.redirect_uri = url_for(
            'login_callback', _external=True)

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        # Store the state so the callback can verify the auth server response.
        session['state'] = state

        return redirect(authorization_url)


@app.route('/api/login/callback')
def login_callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for(
        'login_callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    if session.get('next'):
        return redirect(session.pop('next'))

    return redirect(url_for('index'))


@app.route('/api/logout')
def logout():
    if 'credentials' in session:
        del session['credentials']
    return '', 204


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


if __name__ == '__main__':
    app.run()
