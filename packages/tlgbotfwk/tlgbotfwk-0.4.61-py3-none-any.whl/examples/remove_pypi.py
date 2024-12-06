import requests

# Set your package name and PyPI API token
package_name = "tlgbotfwk"
api_token = "pypi-AgEIcHlwaS5vcmcCJDA4MDViMWVhLTY1MzYtNDMyZC1iYWQ4LTc3ZTgxNDFmNDJjZQACKlszLCI0YWNiOTg2OC01MzA4LTQwNTktYjcyZS0wNDM4NDE5ZDIyYjMiXQAABiD8x24VGgVjeVZOkhURLUITdfrRR8OzMY_CXyi7A_jHKQ"

# List of versions to delete
versions = ["0.1.0","0.1.2","0.3.0","0.3.0","0.3.1","0.3.2","0.3.3","0.3.4","0.4.0","0.4.2","0.4.3","0.4.10", "0.4.9", "0.4.8"]

# PyPI URL for deleting a release
url_template = "https://pypi.org/manage/project/{package}/release/{version}/"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_token}"
}

# Loop through each version and delete it
for version in versions:
    url = url_template.format(package=package_name, version=version)
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Successfully deleted {package_name} version {version}")
    else:
        print(f"Failed to delete {package_name} version {version}: {response.status_code} {response.text}")