import sys
from os import mkdir, remove
from os.path import dirname, join

from appdirs import AppDirs
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from comparetransactionsets import __APP_NAME__, OK, RESET, WARNING

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def exec():
    dirs = AppDirs(appname=__APP_NAME__, appauthor=__APP_NAME__)
    credentials_file_path = join(dirs.user_config_dir, "client_id.json")
    token_file_path = join(dirs.user_cache_dir, "token.json")
    creds = None
    try:
        creds = Credentials.from_authorized_user_file(token_file_path)
        print(f"{OK}Reusing credentials file from previous run.{RESET}")
    except FileNotFoundError:
        pass

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(f"{WARNING}Refreshing credentials.{RESET}")
            try:
                creds.refresh(Request())
            except RefreshError as e:
                remove(token_file_path)
                print(
                    (
                        f"We encountered an error refreshing the credentials: {e}"
                        f"\n\n{WARNING}We've deleted the old credentials."
                        f" Please run the command again to reauthorize.{RESET}"
                    )
                )
                sys.exit(1)
        else:
            print(f"{WARNING}Obtaining credentials.{RESET}")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file_path,
                scopes=SCOPES,
            )
            creds = flow.run_local_server(port=0)
        try:
            mkdir(dirname(token_file_path))
        except FileExistsError:
            pass
        with open(token_file_path, "w") as token:
            token.write(creds.to_json())
    return creds
