# Alakazam

An end-to-end big data e-commerce solution designed using AWS services, using mock data provided courtesy of sundog-education.com. It is comprised of 5 components:

**_Order History app_** - This component is responsible for loading and storage of order data. The data is generated using the script `LogGenerator.py`, which by default parses 100 records but can be directed on the command line to parse as many as required by the user i.e. `./LogGenerator.py 5000` to parse 5000 records. The data is taken from the `OnlineRetail.csv` file. The script generates the data on an EC2 instance (free tier `t2.micro AMI`), which is then published using Kinesis Data Streams into an AWS Lambda function (`ProcessOrders.py`) which in turn will populate a DynamoDB table which the end user app can use to read from (the `Consumer.py` script is used for DynamoDB population). The `agent.json` file configures the data stream along with other Kinesis services, as well as to intiate Cloudwatch monitoring.

The consumer app requires the Python library `boto3` and needs valid AWS credentials and regional information. Execution permissions need to be changed for both scripts (`chmod a+x`). To test the consumer app and ensure that DynamoDB table is being populated, use the `LogGenerator.py` script to add entries into the EC2 instance and tail the consumer app to see it’s behavior on a different terminal using: `tail -f /your/kinesis/directory/path`.
    
**_Product Recommendations app_** - This component is responsible for recommending similar products as per customer preference based on aggregate data using a Machine Learning model. To accomplish this, the order data is published to a Kinesis Firehose, then stored in an S3 data lake. The model, a simple Alternating Least Squares model, is constructed on an Elastic MapReduce cluster using Apache Spark. The script `als.py` simply modifies the `als_example.py` file available as part of the Spark library to fit the data. 

**_Transaction Rate Alarm app_** - This component is responsible for issuing an SMS alert if there is an irregular surge in product demand, suggesting bots or a potential malicious attack on the app. It should operate in real-time to allow for robust response. As such, the data is published to a Kinesis Data Stream, which in turn sends it to a Kinesis Data Analytics application, which helps monitor incoming orders. Then a Lambda function (`TransactionRateAlarm.py`) is used to issue alerts to our phone using Amazon SNS. The `analytics-query.sql` file specifies an irregular order rate of more than 10 orders in a second.

**_Log Analysis app_** - This component is responsible for log data analysis, an essential tool to monitor operations and ensure the system is running smoothly. This can be done in near-real-time and as such utilizes Kinesis Firehose to publish server log data and Amazon Elasticsearch Service to analyze and visualize the log data. The server log data is contained in the `httpd.zip` file. The `kibana-access.json` file is a configuration file which modifies the access policies for the Elasticsearch cluster and allows access to the AES domain from a local machine. The `index.js` script is responsible for conversion of apache logs to JSON format so that it can be ingested into Elasticsearch, and can be available as part of the AES console options. 

**_Data Warehousing and Visualization app_**: This component is responsible for the warehousing and analysis of order data, another essential capability to analyze and optimize business performance over an extended period of time. To accomplish this, we populate an S3 data lake using cumulative order data published to a Kinesis Data Firehose, and use two alternatives to analyze and visualize data: AWS Redshift + Amazon Quicksight for managed analysis and AWS Athena + AWS Glue for serverless analysis.  

List of AWS services used: **EC2**, **Kinesis**, **AWS Lambda**, **S3**, **DynamoDB**, **Amazon Elasticsearch Service**, **Elastic MapReduce**, **SNS**, **Redshift**, **Glue**, **Athena** and **Quicksight** 
