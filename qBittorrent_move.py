import requests
import re
import os
import json
import logging

logging.basicConfig(filename='Torrent_Move.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config.json")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    required_fields = ['qbittorrent', 'target_dir', 'patterns']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Config is missing required field: {field}")
    return config

# login qBittorrent Web UI
def login(config):
    session = requests.Session()
    login_data = {
        'username': config['qbittorrent']['username'],
        'password': config['qbittorrent']['password']
    }
    response = session.post(f"{config['qbittorrent']['url']}/api/v2/auth/login", data=login_data)
    if response.status_code == 200:
        logging.info("Login Successful")
        return session
    else:
        logging.error('Login Failed, please check the username or password')
        raise Exception('Login Failed, please check the username or password')

# Get the status info of all current torrents
def get_torrents(session, config):
    response = session.get(f"{config['qbittorrent']['url']}/api/v2/torrents/info")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error('Failed to get torrent info')
        raise Exception('Failed to get torrent info')

# use qBittorrent API to set new save path
def set_new_location(session, hash_id, new_path, config):
    response = session.post(f"{config['qbittorrent']['url']}/api/v2/torrents/setLocation", data={
        'hashes': hash_id,
        'location': new_path
    })
    if response.status_code == 200:
        logging.info(f"The seed storage path has been updated to: {new_path}")
    else:
        logging.error('Failed to update seed path')
        raise Exception('Failed to update seed path')

# Match multiple RE based on filename and move torrents
def process_torrents(session, config):
    torrents = get_torrents(session, config)

    for torrent in torrents:
        if torrent['state'] == 'downloading':
            continue 

        torrent_name = torrent['name']
        torrent_hash = torrent['hash']

        torrent_match = False
        for folder_name, pattern in config['patterns'].items():
            match = re.search(pattern, torrent_name, re.IGNORECASE)
            if match:
                torrent_match = True
                target_folder = os.path.join(config['target_dir'], folder_name)
                save_path = torrent['save_path']

                if os.path.normpath(save_path) != os.path.normpath(target_folder):
                    os.makedirs(target_folder, exist_ok=True)
                    set_new_location(session, torrent_hash, target_folder, config)
                    logging.info(f"Torrent {torrent_name} has been moved to {target_folder}")
                    break
                else:
                    logging.info(f"Torrent {torrent_name} does not need to be moved")
        
        if not torrent_match:
            logging.info(f"Torrent {torrent_name} does not match any rules.")

def main():
    try:
        config = load_config("config.json")
        session = login(config)
        process_torrents(session, config)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
