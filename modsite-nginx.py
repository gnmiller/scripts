import os
import subprocess
import sys
import argparse


def site_exists(site_name):
    '''Check if an nginx site exists at default location.'''

    available_site_path = f"/etc/nginx/sites-available/{site_name}"
    return os.path.exists(available_site_path)

def enable_site(site_name):
    '''Enable an nginx site at default location.'''

    available_site_path = f"/etc/nginx/sites-available/{site_name}"
    enabled_site_path = f"/etc/nginx/sites-enabled/{site_name}"

    if os.path.exists(enabled_site_path):
        print(f"Site '{site_name}' is already enabled.")
        return -1
    else:
        ret = os.symlink(available_site_path, enabled_site_path)
        print(f"Site '{site_name}' enabled.")
        return ret

def disable_site(site_name):
    '''Disable an nginx site at default location.'''

    enabled_site_path = f"/etc/nginx/sites-enabled/{site_name}"
    if os.path.exists(enabled_site_path):
        ret = os.remove(enabled_site_path)
        print(f"Site '{site_name}' disabled.")
        return ret
    else:
        print(f"Site '{site_name}' is not enabled.")
        return -1

def validate_nginx_conf():
    '''Check if nginx is ok to restart'''

    try:
        ret = subprocess.run(['nginx', '-t'], check=True)
        print("nginx is ok")
        return ret
    except subprocess.CalledProcessError:
        print("nginx is not ok")
        return -1

def restart_nginx():
    '''Restart nginx'''

    try:
        ret = subprocess.run(['systemctl', 'restart', 'nginx'], check=True)
        print("nginx restarted")
        return ret
    except subprocess.CalledProcessError:
        print("failed to restart nginx")
        return -1

def parse_arguments():
    '''Parse cli args with argparse'''
    parser = argparse.ArgumentParser(description="Enable or disable an Nginx site.")
    parser.add_argument("site_name", help="The name of the site to enable or disable")
    parser.add_argument("action",
                        choices=["enable", "disable"],
                        help="Action to perform: enable or disable the site")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    site_name = args.site_name
    action = args.action

    if not site_exists(site_name):
        print(f"Error: The site '{site_name}' does not exist in /etc/nginx/sites-available.")
        sys.exit(-1)

    if action == 'enable':
        enable_site(site_name)
    elif action == 'disable':
        disable_site(site_name)

    validate_nginx_conf()
    restart_nginx()
    sys.exit(0)
