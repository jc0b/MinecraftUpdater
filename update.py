#!/usr/bin/python3
import re
import os
import time
import logging
import requests


# paper specific configuration
PAPER_API_BASE = "https://papermc.io/api/v1"
LOG_FILENAME = 'paper_updater.log'
LOG_FORMAT = '%(asctime)s %(message)s'

logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, format=LOG_FORMAT)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
def check_version(match, latest_paper_ver, latest_paper_build):
    version_array = latest_paper_ver.split(".")
    if match.group(4):
        patch_version = int(match.group(4).strip("."))

    if(int(version_array[1]) > int(match.group(3))):
        logging.info(f"{version_array[1]} > {match.group(3)}")
    elif(int(version_array[1]) >= int(match.group(3)) and int(version_array[2]) > patch_version):
        logging.info(f"{version_array[1]} >= {match.group(3)} AND {version_array[2]} > {patch_version}")
    elif(int(version_array[1]) >= int(match.group(3)) and int(version_array[2]) >= patch_version and latest_paper_build > int(match.group(5))):
        logging.info(f"{version_array[2]} >= {patch_version} AND {latest_paper_build} > {match.group(5)}")

    return (int(version_array[1]) > int(match.group(3))) or (int(version_array[1]) >= int(match.group(3)) and int(version_array[2]) > patch_version) or (int(version_array[1]) >= int(match.group(3)) and int(version_array[2]) >= patch_version and latest_paper_build > int(match.group(5)))

def download_server(version, build):
    logging.info(f"Downloading Paper version {version}, build number {build}.")
    jar_data = requests.get(PAPER_API_BASE + "/paper/" + version + "/latest/download")
    with open(f"paper-{version}-{build}.jar", "wb") as jar_file:
        jar_file.write(jar_data.content)
    jar_file.close()
    logging.info(f"Written updated jar file to paper-{version}-{build}.jar.")
    logging.info("Update complete. Please make any necessary changes to any start scripts, and restart the server.")

def remove_old_servers(filelist):
    logging.info(f"Cleaning up {len(filelist)} old server(s)...")
    for file in filelist:
        logging.info(f"Deleting {file}...")
        os.remove(file)
    logging.info("Cleanup complete.")

def main():
    logging.info("Starting update run...")
    # retrieve version manifest
    logging.info("Getting Paper release versions...")
    response = requests.get(PAPER_API_BASE + "/paper")
    data = response.json()
    latest_paper_ver = data["versions"][0]
    response = requests.get(PAPER_API_BASE + "/paper/" + latest_paper_ver)
    latest_paper_build = int(response.json()["builds"]["latest"])

    logging.info(f'The latest version of Paper is {latest_paper_ver}, build {latest_paper_build}.')

    # check for any servers we have, and see whether they need updating
    logging.info("Checking versions of local servers...")
    match = ""
    existing_servers = [f for f in os.listdir() if re.search(r"(paper-)(\d{1})\.(\d{,2})(\.\d{,2})?-(\d+).jar", f)]
    logging.info(f"{len(existing_servers)} existing servers have been found. Checking the version of the most recent one...")
    if existing_servers:
        match = re.search("(paper-)(\d{1})\.(\d{,2})(\.\d{,2})?-(\d+).jar", existing_servers[0], re.IGNORECASE)
        if match.group(4):
            logging.info(f"You are currently running Paper version {match.group(2)}.{match.group(3)}{match.group(4)}, build number {match.group(5)}")
        else:
            logging.info(f"You are currently running Paper version {match.group(2)}.{match.group(3)}, build number {match.group(5)}")
        if check_version(match, latest_paper_ver, latest_paper_build):
            download_server(latest_paper_ver, latest_paper_build)
            remove_old_servers(existing_servers)
            logging.info("\n")
            exit(0)
        else:
            logging.info("You are up to date!\n")
            exit(0)
    else:
        logging.info("No existing servers could be found.")
        download_server(latest_paper_ver, latest_paper_build)
        exit(0)

if __name__ == "__main__":
    main()
    logging.info("\n")