import requests

# Constants for the API
BASE_URL = "http://localhost:8000"
USER_DETAILS = {
    "username": "testuser183",
    "email": "testuser183@example.com",
    "password": "strongpassword123"
}
JOB_DETAILS = {
    "description": "Process data",
    "priority": "1"  # Ensure this is a string to match server expectations
}
LOGIN_FORM = {
    "username": "testuser183",
    "password": "strongpassword123"
}

def register_user():
    response = requests.post(f"{BASE_URL}/register/", json=USER_DETAILS)
    print("Registration Response:", response.json())
    return response

def login():
    response = requests.post(f"{BASE_URL}/token", data=LOGIN_FORM)
    print("Login Response:", response.json())
    return response

def create_job(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(f"{BASE_URL}/jobs/", json=JOB_DETAILS, headers=headers)
    print("Job Creation Response:", response.json())
    return response


def main():
    # Register user
    reg_response = register_user()
    if reg_response.ok:
        # Login user
        login_response = login()
        if login_response.ok:
            access_token = login_response.json().get("access_token")
            # Create job
            if access_token:
                create_job(access_token)

if __name__ == "__main__":
    main()
