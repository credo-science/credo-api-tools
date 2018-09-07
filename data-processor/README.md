Example Python script for processing exported data

## Usage

Create custom plugins and place them in the plugins folder

```
$ chmod +x credo-data-processorr.py
$ ./credo-data-processor.py --dir ../credo-data-export --plugin-dir plugins

```

## Help
```
usage: credo-data-processor.py [-h] [--dir DIR] [--plugin-dir PLUGIN_DIR]
                               [--data-type DATA_TYPE] [--delete]

Tool for incremental processing of CREDO data

optional arguments:
  -h, --help            show this help message and exit
  --dir DIR, -d DIR     Path to data directory
  --plugin-dir PLUGIN_DIR
                        Path to directory containing processing plugins
  --data-type DATA_TYPE, -k DATA_TYPE
                        Type of event to process (ping/detection/all)
  --delete              Delete processed files
```

## Objects

[Detection](https://github.com/credo-science/credo-webapp/tree/develop/credoapiv2#detection-object)

[Ping](https://github.com/credo-science/credo-webapp/tree/develop/credoapiv2#apiv2ping)
