# shark-games

Games bot for Sharkey
hosted on @games@woem.men

*It might work also on other \*key software, but please keep in mind that it is build around Sharkey's Rate limits and API specifications and so that is the only supported software.*

## Usage
@ping help

note that the ping can be placed anywhere indipendently from the text.

## Hosting
*this maybe gets replaced with proper docs*

### Prerequisite

Python 3.12

**PLEASE NOTE** only python 3.12 is supported currently. It might work also with other versions, but that isn't on the priority list now. As soon as it is finished, I will update the requirements to support also other versions.

1. Navigate where you want the config save directory to be created

2. Create a virtual environment
```
$ python3 -m venv venv
```
3. Activate the environment
```
$ source venv/bin/activate
```
4. Install
```
$ pip install -U wheel
$ pip install -U shark_games 
```
5. Setup
```
$ sharkgames setup
```
Follow the setup guide provided

6. Run
```
$ sharkgames run
```

## Update

Make sure the bot isn't running!

**IMPORTANT** Always check changelog whenever updating. There might be instanced where the automatic update of config doesn't work, for example if you need to enter a value. In that case you need to manually change the config or set up the bot again.

1. Navigate to the directory where you set it up

2. Activate the environment
```
$ source venv/bin/activate
```
3. Update
```
$ pip install -U wheel
$ pip install -U shark_games 
```
4. Run the bot
```
sharkgames run
```
You should see a `Updating…` dialog if there is a config update being done.

## Development

This guide assumes you have already a virtual enviroment set up and activated

1. Build
`python3 -m build`

2. Load the package
`pip install --force-reinstall dist/shark_games-v.v.v-py3-none-any.whl`
*replace v.v.v with the actual version number. The version number can be found in ./shark_games/__init__.py*

3. Test pypi *this isn't mandatory for contributors, you can safely ignore this* **PLEASE NOTE:** make sure only one version is inside the dist directroy
`python3 -m twine upload --repository testpypi dist/*`

4. Run the tests
`test test test` *not available yet*

### Naming etc.
Simply because python doesn't work with -, the package is named shark_games. Commands use sharkgames (for setup etc.) While the rest shark-games should be used.

## Post install config options

The config is saved in `./shark-games/config.json`.

### config options
- `"interval"`(int): how often it checks for new notes. Default: 8, Minimum: 2 (If <2 you hit rate limits)
- `"warnInvalidCommand"` (bool): if it should warn the user when an invalid command is issued. I highly recommend against the usage, as in case of a thread (where responses would automatically ping the bot) it would mean a lot of useless and annoying warnings. Default: false
- `"requestRetries"` (int): How many times it should retry when a request fails. Default: 4

### Rate limit configuring

The rate limit config file is saved in `.shark-games/rate-limits.json`. It is based on Sharkeys limits from the [source](https://activitypub.software/TransFem-org/Sharkey/-/tree/develop/packages/backend/src/server/api/endpoints?ref_type=heads), where for each endpoint in `meta` the `limit` section indicates the parameters. Only the actually used endpoints are actually configured in this software.

## LICENSE

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
