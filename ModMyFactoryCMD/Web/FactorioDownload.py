import sys
import requests
import packaging.version
import shutil
import ApiDefinitions


API_DOMAIN = "https://www.factorio.com"
DOWNLOAD_ENDPOINT = API_DOMAIN + "/get-download"


def download(version, build, platform, file_name, username, token):
    if (not isinstance(packaging.version.parse(version), packaging.version.Version)):
        raise ApiDefinitions.ApiError("Invalid version format.")
    if (build not in ApiDefinitions.Build.list()):
        raise ApiDefinitions.ApiError("Unknown build string.")
    if (platform not in ApiDefinitions.Platform.list()):
        raise ApiDefinitions.ApiError("Unknown platform string.")

    url = DOWNLOAD_ENDPOINT + "/{0}/{1}/{2}?username={3}&token={4}".format(version, build, platform, username, token)
    response = requests.get(url, stream=True)

    if (response.status_code == requests.codes.forbidden):
        raise ApiDefinitions.AuthError()
    if (response.status_code != requests.codes.ok):
        raise ApiDefinitions.ServerError(response.status_code)

    with open(file_name, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
            


if (__name__ == '__main__'):
    args = sys.argv[1:]

    if (len(args) != 6):
        print("Usage: FactorioDownload.py <version> <build> <platform> <file-name> <username> <token>")
        sys.exit()

    try:
        print("Starting download, please wait.")
        download(args[0], args[1], args[2], args[3], args[4], args[5])
    except ApiDefinitions.ServerError as err:
        print("Donwload failed! Status code:", err.status_code)
    except ApiDefinitions.ApiError as err:
        print("Download failed!", err.message)
    else:
        print("Successfully downloaded Factorio to '{0}'.".format(args[3]))