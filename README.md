# GroupBunk
![MIT License](https://img.shields.io/github/license/shine-jayakumar/Covid19-Exploratory-Analysis-With-SQL)

### Leave your Facebook groups quietly

GroupBunk is a command-line python script that allows you to leave Facebook groups.

**Table of Contents**
- [Features](#Features "Features")
- [Requirements](#Requirements "Requirements")
- [Installation](#Installation "Installation")
- [Options](#Options "Options")
- [Usage](#Usage "Usage")

## Features
- Get names of groups you've joined
- Specify groups you want to keep
- Allows you to leave all the groups

## Requirements
- Python 3
- Chrome Browser

View the [requirements.txt](https://github.com/shine-jayakumar/Rubber-Price-Telegram-Bot/blob/master/requirements.txt)

## Installation
```sh
pip install -r requirements.txt
```
## Options
| Option | Description |
| ------ | ------ |
| -u | Facebook username |
| -p | Facebook password |
| -exgrp | filename containing line separated group names to exclude (optional) |
| -elloadto | max timeout for elements to be loaded (optional) |
| -grloadto | time to wait after each scroll (optional) |
| -maxret | max number of retries while recapturing group names (optional) |
| -dumpgrps | Only dumps group names into a file (optional) |

## Usage
- To leave all groups
    ```
    python groupbunk.py -u yourusername@email.com -p yourpassword
    ```
- To view all groups you're member of 
    ```
    groupbunk.py -u yourusername@emial.com -p yourpassword -dumpgrps allgroups.txt
    ```
    *dumps group names to allgroups.txt*
    
- To specify groups you don't want to leave
    ```
    groupbunk.py -u yourusername@emial.com -p yourpassword -exgrp excludegroups.txt
    ```
    *Only group name per line is allowed* 
