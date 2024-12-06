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

import asyncio
import aiohttp
import aiofiles

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(module)s, %(funcName)s: %(message)s")
log = logging.getLogger(__name__)

import json
import time

import signal

import re

from shark_games import __version__

from shark_games.dices import roll
from shark_games.dices import coin
from shark_games.praise import praise

import dice

class Noteprocessing():
    def __init__ (self, main_config_path, rate_limits_path):
        with open(rate_limits_path, "r") as config_file: #read only
            self.rate_data = json.load(config_file)
        
        self.main_config_path = main_config_path #read and write
        with open(self.main_config_path, "r") as config_file:
            self.data = json.load(config_file)
        
        self.is_running = True
        self.tasks = set()
        self.usertag_pattern = rf"@{self.data["username"]}" # DOES NOT INCLUDE HOST

        self.shutdown_in_progress = False

        self.rate_limit_semaphores = {}
        self.last_request_times = {}
        
    async def base_url(self):
        return self.data["base_url"]

    async def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.data["bearer"]}"
        }
    
    async def lastNoteId (self):
        return self.data["lastNoteId"]
    
    async def tell_invalid_command(self):
        return self.data["warnInvalidCommand"]
    
    async def request_retries(self):
        return self.data["requestRetries"]
        
    async def interval(self):
        return self.data["interval"]
    
    async def get_endpoint_rate_limits(self, endpoint:str):
        return self.rate_data[endpoint]
    
    async def elapsed_time(self, clock):
        return time.time() - clock
    
    async def update_request_times(self, endpoint):
        request_rates = self.rate_data[endpoint]
        reset_time_elapsed:bool = (self.last_request_times[endpoint]["reset_time"] > time.time())

        if reset_time_elapsed or int(self.last_request_times[endpoint]["reset_time"]) == -1: #second one is the default first config one
            self.last_request_times[endpoint]["reset_time"] = time.time() + request_rates["duration"]
        
        if reset_time_elapsed:
            self.last_request_times[endpoint]["amount"] = 0
        else:
            self.last_request_times[endpoint]["amount"] += 1
        
        self.last_request_times[endpoint]["lastReqTime"] = time.time()
        
        
    
    async def enforce_delay(self, endpoint): #does not update anything
        request_rates = self.rate_data[endpoint]
        last_req_times = self.last_request_times[endpoint]

        last_request_time = last_req_times["lastReqTime"]
        interval = request_rates["minInterval"] #can be None
        if interval:
            elapsed = await self.elapsed_time(last_request_time)
            if elapsed < interval:
                await asyncio.sleep(interval - elapsed)

        if last_req_times["amount"] > request_rates["max"]:
            await asyncio.sleep(last_req_times["reset_time"] - time.time())
        
    
    async def handle_request(self, endpoint:str, json_req):
        default_delay = 8.0 #in s
        async with self.rate_limit_semaphores[endpoint]:
            await self.enforce_delay(endpoint)
            
            for attempt in range(await self.request_retries() + 1):
                async with aiohttp.ClientSession() as session:
                    response = await session.post(await self.base_url() + endpoint, json = json_req, headers= await self.headers())
                
                await self.update_request_times(endpoint)
                
                try:
                    respjson = await response.json()
                except Exception as e:
                    log.error(f"Failed to get response.json() for {e}")
                    respjson = None

                match response.status:
                    case 200:
                        return respjson
                    case 429:
                        log.warning(f"Rate limit hit at {endpoint}")
                        if respjson:
                            reset_time = respjson.get("error", {}).get("info", {}).get("resetMs", None) #in ms
                        else:
                            reset_time = None
                        if reset_time:
                            delay = (reset_time / 1000) - time.time() #in s
                        else:
                            log.warning(f"Rate limit: failed to get retry time. Falling back to default")
                            delay = default_delay #in s

                        log.warning(f"Rate limit: retrying in {delay}")

                        await asyncio.sleep(delay)
                    case _:
                        log.error(f"Got {response.status} on {endpoint}: {respjson}\n{response}\nRetrying in {default_delay}")
                        await asyncio.sleep(default_delay)

                if attempt == await self.request_retries():
                    log.critical(f"Failed {await self.request_retries() + 1} times on {endpoint} with the last time {response.status}. Skipping this task")

        return None
    
    def create_add_task(self, task): #not async bacause asyncio.create_task isn't
        actual_task = asyncio.create_task(task)
        self.tasks.add(actual_task)
        actual_task.add_done_callback(self.tasks.discard)

    async def update_lastNoteId(self, noteId:str):
        self.data["lastNoteId"] = noteId
        data_to_write = json.dumps(self.data)
        async with aiofiles.open(self.main_config_path, mode="w") as config_file:
            await config_file.write(data_to_write)

    async def return_help_message(self):
        return f"""
<center>$[x3 **HELP PAGE**]</center>
$[x2 Usage]
Write the command text and ping the bot. The bot ping needs to be in first place. The bot will reply with the same visibility (including if federate or not, in case of local users) and cw. The bot will not ping you on reply.
$[x2 Commands]
<required-argument> [optional-argument] (alias)
**help** () - shows this page
**ping** - replies with pong
**pong** - replies with ping
**roll [min:int] [max:int]** - Replies with a random number number between min and max. min and max default to 1 and 100 respectively
**dice <combination:str>** - Replies with the dices. ?[Learn more about the dice notation](https://github.com/borntyping/python-dice?tab=readme-ov-file#notation)
**coin** (flip) - Flips a coin: replies with either Head or Tails
**praise [mention]** (compliment) - compliment person you mention. This will still reply to your note. When no arguments are given, will praise author.
<small>shark-games | version: {__version__} | ?[Source](https://codeberg.org/itssophie/shark-games) | ?[GPL-3.0-or-later](https://codeberg.org/itssophie/shark-games/src/branch/main/LICENSE)</small>
"""

    async def tell_missing_argument(self, n_arguments, command:str):
        return f"ERROR {n_arguments} missing argument(s) in command {command}"
    
    async def get_user_info(self, mention:str):
        if mention[0] == "@":
            mention = mention[1:]
        if "@" in mention:
            user_host = mention.split("@")
        else:
            user_host = [mention, None]

        json_req = {
            "username": user_host[0],
            "host": user_host[1]
        }

        return await self.handle_request("users/show", json_req)

    async def execute_command(self, text:str, author):
        try:
            return_text = None
            cw = None
            
            text = text.strip()
            splitted_text = text.split()
            if self.usertag_pattern in splitted_text[0]:
                splitted_text.pop(0)
            else:
                return_text = "The bot mention needs to be on first place. It seems like it isn't."
            length_splitted_text = len(splitted_text)
            if length_splitted_text == 0:
                splitted_text = [""]
            
            match splitted_text[0]:
                case "ping":
                    return_text = "pong"
                case "pong":
                    return_text = "ping"
                case "help" | "":
                    return_text = await self.return_help_message()
                case "roll":
                    match length_splitted_text:
                        case 1:
                            return_text = roll.main()
                        case 2:
                            return_text = roll.main(max = int(splitted_text[1]))
                        case 3:
                            return_text = roll.main(min = int(splitted_text[1]), max = int(splitted_text[2]))
                case "dice":
                    if length_splitted_text == 1:
                        return_text = await self.tell_missing_argument(1, "dice")
                    try: 
                        return_text = str(dice.roll(splitted_text[1]))
                    except Exception:
                        return_text = "Error processing dice request. ?[Learn more about the dice notation](https://github.com/borntyping/python-dice?tab=readme-ov-file#notation)"
                case "coin" | "flip":
                    return_text = coin.main()
                case "praise" | "compliment":
                    cw = "Praise"
                    if length_splitted_text == 1:
                        return_text = praise.main(author)
                    else:
                        user_info = await self.get_user_info(splitted_text[1])
                        if user_info:
                            return_text = praise.main(user_info)
                        else:
                            log.error("Something went wrong with trying to get user info to praise")
                            return_text = "An error occured trying to get mentioned user info"
                            cw = None
                case _:
                    if await self.tell_invalid_command():
                        return_text = "It seems like you misspelled something. Reply (and mention) `help` to find out about my commands"

        except Exception as e:
            log.error(f"Unknow error processing {text} with Exception: {e}")
            return_text = "An unknown error happened"

        return return_text, cw

        


    async def process_item(self, item):
        text, cw = await self.execute_command(item["text"], item["user"])
        if not text:
            return
        if not cw:
            cw = item["cw"]

        json_req = {
            "visibility": item["visibility"],
            "localOnly": item["localOnly"],
            "replyId": item["id"],
            "cw": cw,
            "text": text
        }
        await self.handle_request("notes/create", json_req)
        return

    async def req_json (self):
        if await self.lastNoteId() == None:
            return {
                "limit": 10
            }
        else:
            return {
            "limit": 100,
            "sinceId": await self.lastNoteId()
            }
    
    async def fetch(self):
        respjson =  await self.handle_request("notes/mentions", await self.req_json())

        if not respjson:
            return
        if respjson == [] or respjson[0]["id"] == await self.lastNoteId():
            return
        
        if len(respjson) >= 95:
            log.warning("The amount of new fetched notes is >= 95. You can safely ignore this if it happens after a long downtime")
        
        await self.update_lastNoteId(respjson[0]["id"])

        for item in respjson:
            self.create_add_task(self.process_item(item))

    def stop(self):
        if self.shutdown_in_progress:
            return
        self.shutdown_in_progress = True
        self.is_running = False
        log.info("Shutting down…")

    async def shutdown(self):
        if self.tasks:
            previous_len_task = len(self.tasks) + 1
            while self.tasks:
                if previous_len_task != len(self.tasks):
                    previous_len_task = len(self.tasks)
                    log.info(f"There are still {previous_len_task} left. Waiting for them to finish.")
                await asyncio.sleep(0.5)

            log.info("All tasks complete. Proceeding to shutdown")
    
    async def start(self):
        log.info("Started")
        while self.is_running:
            self.create_add_task(self.fetch())

            await asyncio.sleep(await self.interval())
    
    async def set_rate_semaphores_times(self):
        for key in self.rate_data:
            self.rate_limit_semaphores[key] = asyncio.Semaphore(1)
            self.last_request_times[key] = {"lastReqTime": 0.0, "amount": 0, "reset_time": -1.0}

    async def async_run(self):
        await self.set_rate_semaphores_times()

        loop = asyncio.get_event_loop()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(
                sig, 
                lambda s=sig: self.stop()
            )
        
        await self.start()
        await self.shutdown()

    def run(self):
        log.info("Starting up…")
        asyncio.run(self.async_run())