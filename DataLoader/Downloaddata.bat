#c:\program files\google\google_appengine\

appcfg.pyupdate c:\users\user\workspace\laybuy

appcfg.py create_bulkloader_config --filename=bulkloader.yaml --url=http://memartlbuyhrd.appspot.com/_ah/remote_api


appcfg.py download_data --application=s~memartlbuyhrd --kind=Item --url=http://memartlbuyhrd.appspot.com/_ah/remote_api --filename=malbuy2.csv
appcfg.py download_data --application=s~memartlbuyhrd --url=http://memartlbuyhrd.appspot.com/_ah/remote_api --filename=malbuyAll.csv

appcfg.py upload_data --application=s~memartlbuyhrd --kind=Item --url=http://memartlbuyhrd.appspot.com/_ah/remote_api --filename=Items_bulk_upload.csv --config_file=mal_bul_item.yaml

appcfg.py upload_data --application=dev~memartlbuyhrd --config_file=mal_bul_item.yaml --filename=Items_bulk_upload.csv --kind=Item --url=http://localhost:8080/_ah/remote_api C:\Users\marjo\workspace\laybuy

    - property: bper
      external_name: bper
      import_transform: transform.import_date_time('%Y-%m-%d') 
      export_transform: transform.export_date_time('%Y-%m-%d') 

    - property: eper
      external_name: eper
      import_transform: transform.import_date_time('%Y-%m-%d') 
      export_transform: transform.export_date_time('%Y-%m-%d') 

    - property: author
      external_name: author

    - property: date_added
      external_name: date_added
      import_transform: transform.import_date_time('%Y-%m-%d') 
      export_transform: transform.export_date_time('%Y-%m-%d') 

    - property: date_changed
      external_name: date_changed
      import_transform: transform.import_date_time('%Y-%m-%d') 
      export_transform: transform.export_date_time('%Y-%m-%d') 
