# [BurpGraphQl](https://pypi.org/project/BurpGraphQl/1.5/)
This is a Python module for controlling / automating Burpsuite Enterprise via their GraphQL API.

### Usage
```
python3 -m pip install BurpGraphQl
```

```python
import BurpGraphQl
obj = BurpGraphQl("Burpsuite Enterprise GraphQL API Path", "API token")
print(obj.list_scans())
```

### Methods 
- ``BurpGraphQl.run_query(str_query)``
    Run a GraphQL Query. All methods in this class are using this method to run queries.

- ``BurpGraphQl.get_configs()``
    Get Scan configurations.

- ``BurpGraphQl.start_scan(str_siteID, str_config_id)``
    - Start a Scan on Burpsuite Enterprise. Example : 
    ```python
    configs = obj.get_configs()
    siteid = obj.get_site_id("http://insecure-site")
    if siteid is not None:
        scan = obj.start_scan(siteid, "8741f9d8-8624-48b4-af2b-e9bcebf012dd") # Start Scan
    ```
- ``BurpGraphQl.SiteTree()`` Returns all Sites in Burpsuite Enterprise.

- ``BurpGraphQl.new_site(str_folderid, str_sites)`` Create a new Site in Burpsuite Enterprise.

- ``BurpGraphQl.stop_scan(str_scan_id)`` Stop a scan.

- ``BurpGraphQl.scan_info(str_scan_ID)`` Get Scan information.

- ``BurpGraphQl.get_report(str_scan_ID)`` Get Scan Report. (HTML)

- ``BurpGraphQl.get_folder_id(str_folder_name)`` Get Folder ID.

- ``BurpGraphQl.get_site_id(str_site_name)`` Get Site ID.

- ``BurpGraphQl.get_scan_id(str_site_name)`` Get Scan ID.

- ``get_percentage(str_site_name)`` Get Scan Percentage.


### Examples 

#### Start a Scan on burpsuite enterprise.

```python
configs = obj.get_configs()
siteid = obj.get_site_id("http://insecure-site")
if siteid is not None:
    scan = obj.start_scan(siteid, "8741f9d8-8624-48b4-af2b-e9bcebf012dd") # Start Scan

```

#### Create New Folder and Add Sites to it
```python
obj = obj.create_folder("0", "Folder1")
folder_id = obj.get_folder_id("Folder1")
print("Created folder with id {}".format(folder_id))
new_site = obj.new_site(folder_id, "http://insecure-site")
print(new_site)
```


### Contributing
Hello! Help me in improving this module for people who want to integrate the amazing Burpsuite Enterprise. Fork and Create a pull request! 
