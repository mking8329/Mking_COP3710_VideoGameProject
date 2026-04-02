Steps to make this thing work

1: Run 'create_db.sql', preferably in Oracle SQL Developer.
2) Place 'preprocess.py' into the 'data' folder
3) Open 'preprocess.py', and replace the address in BASE with the data folder's path.
4) Run 'py [ADDRESS OF preprocess.py]'. 
5) Should see "Cleaned CSV files written to [location]". Generates a folder 'oracle_etl_v2' which contains the folder 'cleaned', which contains cleaned versions of the CSV files.
6) Open 'dataload.py' and replace the Base, User, Password, and DSN values as necessary
7) Link the folder address of instant client in oracledb.init_oracle_client.
7) Run 'py [ADDRESS OF dataload.py]'.
8) Hopefully, it will work

I have a word document with screenshots of my filled-out database as proof that it worked for me at the very least.