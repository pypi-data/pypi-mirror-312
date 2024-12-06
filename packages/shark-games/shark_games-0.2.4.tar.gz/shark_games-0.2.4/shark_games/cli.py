"""
 Copyright (C) 2024  sophie (itsme@itssophi.ee)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import click
import requests

import json
import re
import os

import asyncio

from shark_games import __version__
from shark_games.main import Noteprocessing

path = os.path.join(os.getcwd(), "shark-games")

default_config_data = {
        "v" : "", #gets automatically configured
        "base_url" : "https://woem.men/api/",
        "bearer" : "",
        "username": "",
        "interval" : 8, #currently only changeable directly via file
        "lastNoteId": None,
        "warnInvalidCommand": False, #currently only changeable directly via file
        "requestRetries": 4 #currently only changeable directly via file
    }
config_data_filename = str(path) + "/config.json"

default_data_needstoconfig = ["bearer"]

#Rate limits of specific used endpoints. max: amount of requests in "duration" (in seconds)
rate_limits = {
    "v": "", #gets automatically configured, added here for redundancy
    "notes/mentions": {"duration": 5.0, "max": 10, "minInterval": None}, #10 notes per 5 seconds
    "notes/create":  {"duration": 3600.0, "max": 300, "minInterval": 1.0} #300 notes per 1 hour, with a minimum interval of 1 hour
}
rate_limits_filename = str(path) + "/rate-limits.json"


def config_update_v(data):
    data["v"] = __version__
    return data

def read_config_file(path):
    with open(path, "r") as config_file:
        data = json.load(config_file)
    return data

def write_config_file(path, data):
    with open(path, "w") as config_file:
        json.dump(data, config_file)

@click.group()
@click.version_option(version=__version__)
def cli():
    pass

@click.command()
def setup():
    data = default_config_data
    data = config_update_v(data)
    
    previous_attempt:str = ""
    while True:
        attempt = click.prompt("\nPlease enter your base URL", default=data["base_url"])
        if re.match(r"https://.*\.[A-Za-z]+/api/", attempt):
            break
        else:
            if previous_attempt == attempt:
                if click.confirm("Do you want to skip the URL format check? This might break the program later on."):
                    click.echo("You confirmed to skip the base URL check")
                    break
            previous_attempt = attempt
            click.echo("The provided base URL is in an unexpected format. You can skip check by re-entering the same URL again.\nThe URL needs to start via the https protocol (https://) and needs to end with a /. Normally it also ends with /api/")
    
    try:
        response = requests.get(attempt)
    except:
        click.echo("Invalid URL entered")
        click.echo("Exiting…")
        exit()

    data["base_url"] = attempt
    data["bearer"] = click.prompt("\nPlease enter your API token", hide_input=True)
    
    headers = {
        "Authorization": f"Bearer {data["bearer"]}"
    }
    response = requests.post(f"{data["base_url"]}i", headers=headers, json={})
    if response.status_code == 200:
        jsonresponse = response.json()
        data["username"] = jsonresponse["username"]
    else:
        click.echo(f"Invalid token or response: {response.status_code}, {response.json()["error"]["message"]}")
        click.echo("Exiting…")
        exit()
    
    if os.path.exists(path):
        if click.confirm("Overwrite existing config"):
            pass
        else:
            click.echo("Aborting")
            exit()
    
    else:
        os.makedirs(path)

    rate_data = rate_limits
    rate_data = config_update_v(rate_data)

    write_config_file(config_data_filename, data)
    write_config_file(rate_limits_filename, rate_data)

@click.command()
def run():
    def update_configs(data, default_data, filename):        
        if data["v"] != __version__:
            click.echo("Updating…")

            if data["v"] > __version__:
                click.echo("Version downgrading is not supported. Please update to the last version instead.")
                exit()
            
            # removes all the keys that no longer are used
            keys_to_delete = data.keys() - default_data.keys()
            for key in keys_to_delete:
                data.pop(key)

            # adds the new keys with default value
            keys_to_add = default_data.keys() - data.keys()
            for key in keys_to_add:
                if key in default_data_needstoconfig:
                    click.echo(f"Can't update config because key ({key}) needs config. Please reconfigure shark-games or consult release notes in case of a breaking change")
                    exit()
                data[key] = default_data[key]

            #finally, update the version number
            data = config_update_v(data)

            write_config_file(filename, data)
    
    config_data = read_config_file(config_data_filename)
    update_configs(config_data, default_config_data, config_data_filename)

    rate_data = read_config_file(rate_limits_filename)
    update_configs(rate_data, rate_limits, rate_limits_filename)
    
    process = Noteprocessing(config_data_filename, rate_limits_filename)
    process.run()

cli.add_command(setup)
cli.add_command(run)