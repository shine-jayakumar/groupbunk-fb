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
- [Examples](#Examples "Examples")
- [License](#LICENSE "License")

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
Required arguments
| Arguments | Description |
| ------ | ------ |
| username | Facebook username |
| password | Facebook password |

Optional arguments
| Option | Description |
| ------ | ------ |
| -eg', '--exgroups | file with group names to exclude (one group per line) |
| -et', '--eltimeout | max timeout for elements to be loaded |
| -sw', '--scrollwait | time to wait after each scroll |
| -gr', '--groupretry | retry count while recapturing group names |
| -dg', '--dumpgroups | do not leave groups; only dump group names to a file |
| -v, --version | show program's version number and exit |

## Usage
**To leave all groups**

```
groupbunk.py username password
```
    
**To view all groups you're member of**
```
groupbunk.py username password --dumpgroups filename
```
    
**To specify groups you don't want to leave**
```
groupbunk.py username password --exgroups filename
```
    
## Examples
```
groupbunk.py bob101@email.com bobspassword101
```
```
groupbunk.py bob101@email.com bobspassword101 -eg keepgroups.txt
```
```
groupbunk.py bob101@email.com bobspassword101 -et 60 --scrollwait 10 -gr 7
```
```
groupbunk.py bob101@email.com bobspassword101 --dumpgroups mygroup.txt --groupretry 5
```
## LICENSE
[MIT](https://github.com/shine-jayakumar/groupbunk-fb/blob/master/LICENSE)
