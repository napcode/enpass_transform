Import Enpass JSON export into LastPass
=======================================

Transforms the Enpass json export into CSV that can be used in LastPass as import format.

Usage
-----

Export your Enpass vault as json to a file. Using an explicit group is recommended. This will import all items into a seaprate folder within LastPass. In case of problems, the entire folder can easily be erased.  
```bash
python enpass_transform.py -h
python enpass_transform.py -i myexport.json
```

