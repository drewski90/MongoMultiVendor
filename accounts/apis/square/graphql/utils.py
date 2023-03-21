import datetime 
make_timestamp = lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()