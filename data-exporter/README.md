A tool for incremental data export.

## Usage

```
$ chmod +x credo-data-exporter.py
$ ./credo-data-exporter.py --user yourusername --password '3p7Cs3U9TepAfZsXkN7x9VtLz'

```

## Help
```
$ ./credo-data-exporter.py --help

usage: credo-data-exporter.py [-h] [--username USERNAME] [--password PASSWORD]
                              [--endpoint ENDPOINT] [--dir DIR]
                              [--token TOKEN] [--data-type DATA_TYPE]

Tool for incremental data export from CREDO

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME, -u USERNAME
                        Username
  --password PASSWORD, -p PASSWORD
                        Password
  --endpoint ENDPOINT   API endpoint
  --dir DIR, -d DIR     Path to data directory
  --token TOKEN, -t TOKEN
                        Access token, used instead of username and password to
                        authenticate
  --data-type DATA_TYPE, -k DATA_TYPE
                        Type of event to update (ping/detection/all)


```
