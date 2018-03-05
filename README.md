This is a small utility to import [AWS flow logs ](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/flow-logs.html#flow-log-records) 
into a sqlite3 database which makes searching much easier.

First [export your flow logs to S3](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/S3Export.html) 
then download the logs. This will give you several folders named with the network interface containing gzipped 
plain text files.

Use `zcat path/to/file/1 path/to/file/2 | python3 import-aws-flow-logs-to-sqlite.py -f logs.db` to decompress then 
pipe the logs into the script which will generate a database logs.db, you can then query this db using 
your favourite sqlite interface.
