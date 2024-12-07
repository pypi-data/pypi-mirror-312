import threading
import time
from typing import Optional
import logging
from rx.subject import BehaviorSubject
import requests
from requests.exceptions import RequestException
import os
import keyring
from typing import Union



# Constants
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
AUTH_KEYRING_SERVICE = 'firebase-auth'
ID_TOKEN_KEY = 'id_token'
REFRESH_TOKEN_KEY = 'refresh_token'
TOKEN_EXPIRY_KEY = 'token_expiry'
TOKEN_EXPIRY_BUFFER = 300  # 5 minutes in seconds
TOKEN_REFRESH_INTERVAL = 60  # 1 minute in seconds

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JitAuth:
    def __init__(self):
        self.token_refresh_thread: Optional[threading.Thread] = None
        self.stop_refresh = threading.Event()
        self._current_auth_state = self._is_logged_in()
        self.user_subject = BehaviorSubject(self._current_auth_state)


    def _is_logged_in(self) -> bool:
        """Check if the user is currently logged in."""
        if keyring.get_password(AUTH_KEYRING_SERVICE, ID_TOKEN_KEY):
            print(keyring.get_password(AUTH_KEYRING_SERVICE, ID_TOKEN_KEY))
            self.start_token_refresh_thread()
            return True
        else:
            return False


    def _update_auth_state(self, new_state: bool) -> None:
        """
        Update the authentication state and notify observers if it has changed.

        Args:
            new_state (bool): The new authentication state
        """
        if new_state != self._current_auth_state:
            self._current_auth_state = new_state
            self.user_subject.on_next(new_state)

    def sign_in(self, email: str, password: str):
        """
        Sign in the user with email and password.

        Args:
            email (str): User's email
            password (str): User's password

        Returns:
            bool: True if sign-in was successful, False otherwise
        """
        url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}'
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            print(data['idToken'])
            expiry_time = time.time() + int(data['expiresIn']) - TOKEN_EXPIRY_BUFFER
            self._save_tokens(data['idToken'], data['refreshToken'], expiry_time)
            self._update_auth_state(True)
            self.start_token_refresh_thread()
        except RequestException as e:
            logger.error(f"Failed to sign in: {str(e)}")
            raise



    def _save_tokens(self, id_token: str, refresh_token: str, expiry_time: float) -> None:
        """
        Securely save authentication tokens and expiry time.

        Args:
            id_token (str): ID token
            refresh_token (str): Refresh token
            expiry_time (float): Token expiry time
        """
        keyring.set_password(AUTH_KEYRING_SERVICE, ID_TOKEN_KEY, id_token)
        keyring.set_password(AUTH_KEYRING_SERVICE, REFRESH_TOKEN_KEY, refresh_token)
        keyring.set_password(AUTH_KEYRING_SERVICE, TOKEN_EXPIRY_KEY, str(expiry_time))

    def refresh_id_token(self) -> None:
        """Refresh the ID token using the stored refresh token."""
        url = f'https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}'
        refresh_token = keyring.get_password(AUTH_KEYRING_SERVICE, REFRESH_TOKEN_KEY)
        if not refresh_token:
            logger.error("No refresh token found. User may need to re-authenticate.")
            self.logout()
            return

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            expiry_time = time.time() + int(data['expires_in']) - TOKEN_EXPIRY_BUFFER
            self._save_tokens(data['id_token'], data['refresh_token'], expiry_time)
            print(data['id_token'])
            self._update_auth_state(True)
        except RequestException as e:
            self._handle_refresh_error(e)
        except Exception as e:
            self._handle_refresh_error(f"{str(e)}")

    def _handle_refresh_error(self, error: Union[str, Exception]) -> None:
        """
        Handle token refresh errors.

        Args:
            error (Union[str, Exception]): Error message or exception from the refresh attempt
        """
        error_message = str(error)
        
        # Define critical errors that require immediate logout
        critical_errors = ['TOKEN_EXPIRED', 'INVALID_REFRESH_TOKEN', 'USER_DISABLED', 'USER_NOT_FOUND']
        
        # Define retryable errors
        retryable_errors = ['NETWORK_ERROR', 'SERVER_ERROR', 'TIMEOUT']
        
        if any(msg in error_message for msg in critical_errors):
            self.logout()
            logger.error(f"Critical error refreshing token: {error_message}. Logged out.")
            self.user_subject.on_error(Exception(f"Authentication failed: {error_message}"))
        elif any(msg in error_message for msg in retryable_errors):
            retry_count = getattr(self, '_retry_count', 0) + 1
            self._retry_count = retry_count
            
            if retry_count <= 3:  # Maximum 3 retry attempts
                wait_time = 2 ** retry_count  # Exponential backoff: 2, 4, 8 seconds
                logger.warning(f"Retryable error refreshing token: {error_message}. "
                            f"Retrying in {wait_time} seconds (attempt {retry_count}/3).")
                time.sleep(wait_time)
                self.refresh_id_token()  # Retry the refresh
            else:
                logger.error(f"Failed to refresh token after 3 attempts. Last error: {error_message}")
                self.logout()
                self.user_subject.on_error(Exception("Failed to refresh authentication after multiple attempts"))
        else:
            logger.error(f"Unexpected error refreshing token: {error_message}.")
            self.user_subject.on_error(Exception(f"Unexpected authentication error: {error_message}"))

        # Reset retry count if we're not in a retry scenario
        if not any(msg in error_message for msg in retryable_errors):
            self._retry_count = 0

    def start_token_refresh_thread(self) -> None:
        """Start a background thread to automatically refresh the token."""
        self.stop_refresh.clear()
        if self.token_refresh_thread is None or not self.token_refresh_thread.is_alive():
            self.token_refresh_thread = threading.Thread(target=self.auto_refresh_token)
            self.token_refresh_thread.daemon = True
            self.token_refresh_thread.start()

    def auto_refresh_token(self) -> None:
        """Automatically refresh the token before it expires."""
        count = 60
        while not self.stop_refresh.is_set():
            if count ==TOKEN_REFRESH_INTERVAL:
                count=0
                expiry_str = keyring.get_password(AUTH_KEYRING_SERVICE, TOKEN_EXPIRY_KEY)
                if expiry_str:
                    expiry_time = float(expiry_str)
                    time_until_expiry = expiry_time - time.time()
                    if time_until_expiry < TOKEN_EXPIRY_BUFFER:
                        self.refresh_id_token()
            else:
                count+=1
            time.sleep(1)

    def logout(self) -> None:
        """Handle logout operations."""
        if keyring.get_password(AUTH_KEYRING_SERVICE, ID_TOKEN_KEY) is None:
            return
        self.dispose()
        keyring.delete_password(AUTH_KEYRING_SERVICE, ID_TOKEN_KEY)
        keyring.delete_password(AUTH_KEYRING_SERVICE, REFRESH_TOKEN_KEY)
        keyring.delete_password(AUTH_KEYRING_SERVICE, TOKEN_EXPIRY_KEY)
        self._update_auth_state(False)


    def dispose(self) -> None:
        """Dispose of resources, stopping all threads and clearing stored data."""
        self.stop_refresh.set()
        
        if self.token_refresh_thread and self.token_refresh_thread.is_alive():
            try:
                self.token_refresh_thread.join(timeout=5.0)  # Wait up to 5 seconds for the thread to finish
                if self.token_refresh_thread.is_alive():
                    logger.warning("Refresh thread did not terminate within the timeout period.")
            except Exception as e:
                logger.error(f"Error while joining refresh thread: {str(e)}")


