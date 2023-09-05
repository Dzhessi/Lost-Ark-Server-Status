from bs4 import BeautifulSoup
from plyer import notification
import requests
import time
import argparse
import os

def get_server_status():
    url = "https://www.playlostark.com/en-us/support/server-status"
    r = requests.get(url)

    if r.status_code == 200:
        html_content = r.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        na_west = soup.find("div", class_="ags-ServerStatus-content-responses-response ags-ServerStatus-content-responses-response--centered ags-js-serverResponse is-active")
        region_list = [na_west] 
        
        region_responses = soup.find_all('div', class_='ags-ServerStatus-content-responses-response ags-ServerStatus-content-responses-response--centered ags-js-serverResponse')
        region_list.extend(region_responses)

        regions = ["NA West", "NA East", "EU Central", "South America"]
        
        server_status_data = {}

        for region_name, region in zip(regions, region_list):
            server_responses = region.find_all('div', class_='ags-ServerStatus-content-responses-response-server')
            region_servers = []

            for response in server_responses:
                server_name = response.find('div', class_='ags-ServerStatus-content-responses-response-server-name').text.strip()
                raw_server_status = response.find('div', class_='ags-ServerStatus-content-responses-response-server-status')['class'][1]
                server_status = raw_server_status.split("-")[-1].capitalize()
                
                region_servers.append({"name": server_name, "status": server_status})
            
            server_status_data[region_name] = region_servers
        
        return server_status_data
    else:
        print(f"Failed to retrieve HTML. Status code: {r.status_code}")
        return None

def print_server_status(server_status_data):
    for region_name, region_servers in server_status_data.items():
        print(f"\n--- {region_name} ---")
        for server in region_servers:
            print("{:<10} {:<15}".format(server['name'], server['status']))

def search_server(data, server_name):
    server_name_lower = server_name.lower()
    for region, servers in data.items():
        for server in servers:
            if server["name"].lower() == server_name_lower:
                return region, server["status"]
    return None, None

def print_countdown(seconds, status_message):
    for remaining in range(seconds, 0, -1):
        os.system('cls' if os.name == 'nt' else 'clear')
        if status_message:
            print(status_message)
        print(f"\nChecking again in {remaining} seconds...")
        time.sleep(1)

def send_system_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Lost Ark Server Status Checker"
    )

def main():
    parser = argparse.ArgumentParser(description="Search for a server's region and status.")
    parser.add_argument("-w", "--watchserver", help="Server name to monitor.")

    args = parser.parse_args()

    if args.watchserver:
        while True:

            regions_and_servers = get_server_status()
            server_name = args.watchserver
            region, status = search_server(regions_and_servers, server_name)

            if region:
                if status == "Good":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    send_system_notification("Loa Server Status", f"Server: {server_name.capitalize()}\nStatus: Online")
                    status_message = f"Region: {region}\nServer: {server_name.capitalize()}\nStatus: {status}"
                    print(status_message)
                    break  # Exit the loop when the server is online
                else:
                    status_message = f"Region: {region}\nServer: {server_name.capitalize()}\nStatus: {status}"
                    print(status_message)
            else:
                status_message = f"Server '{server_name}' not found or region offline."
                print(status_message)

            print_countdown(60, status_message)

        print(f"\nServer: {server_name.capitalize()}, is online")
    else:
        server_data = get_server_status()
        if server_data:
            print_server_status(server_data)

if __name__ == "__main__":
    main()