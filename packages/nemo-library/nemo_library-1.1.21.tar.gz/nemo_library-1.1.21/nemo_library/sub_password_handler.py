import sys
import keyring


class PasswordManager:
    def __init__(self, service_name, username):
        self.service_name = service_name
        self.username = username

    def set_password(self, password):
        """
        Stores the password in the Credential Manager (Windows) or Keychain (macOS).

        Args:
            password (str): The password to be stored.
        """
        keyring.set_password(self.service_name, self.username, password)

    def get_password(self):
        """
        Retrieves the password from the Credential Manager (Windows) or Keychain (macOS).

        Returns:
            str: The stored password or None if no password is found.
        """
        return keyring.get_password(self.service_name, self.username)


if __name__ == "__main__":
    # Example usage:
    service_name = "nemo_library"
    username = "my_username"
    password = "my_password"

    pm = PasswordManager(service_name, username)

    # Set password
    pm.set_password(password)
    print(
        f"Password for user '{username}' in service '{service_name}' has been stored."
    )

    # Retrieve password
    retrieved_password = pm.get_password()
    if retrieved_password:
        print(f"The stored password for user '{username}' is: {retrieved_password}")
    else:
        print(f"No password found for user '{username}' in service '{service_name}'.")
