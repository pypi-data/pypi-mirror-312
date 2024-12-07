import logging
import boto3
import phonenumbers
from botocore.exceptions import ClientError


class AuctionManager:
   
    def __init__(self, queue_name, region, bucket_name):
       self.queue_name = queue_name
       self.region = region
       self.bucket_name = bucket_name

       
    def send_bid_sqs(self, message):
        logging.info("AuctionManager:send_bid_sqs queue = " + self.queue_name )
        try:
            logging.info("AuctionManager:send_bid_sqs message = " + message )
            session = boto3.session.Session()
            sqs_client = session.client('sqs', region_name=self.region)
            response = sqs_client.get_queue_url(QueueName=self.queue_name)
            queue_url = response['QueueUrl']
            logging.info("AuctionManager:send_bid_sqs queue_url = " + queue_url )
            response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message)
            logging.info("AuctionManager:send_bid_sqs message sent")
        except ClientError as e:
            logging.error("AuctionManager:send_bid_sqs:ClientError" )
            logging.error(e)
            return False
        return True
   
    def check_subscribed_to_topic(self, sns_client, topic_arn, email):
        paginator = sns_client.get_paginator('list_subscriptions_by_topic')
        for page in paginator.paginate(TopicArn=topic_arn):
            for subscription in page['Subscriptions']:
                if subscription['Protocol'] == 'email' and subscription['Endpoint'] == email:
                    return True
        return False

    def create_new_auction(self, auction_name, email_addr):
        return self.subscribe_user_to_auction(auction_name, email_addr)

    def subscribe_user_to_auction(self, auction_name, email_addr, phone = ''):
        sns_topic = auction_name
        logging.info("AuctionManager:subscribe_user_to_auction email " + email_addr + " to topic " + sns_topic )
        try:
            # Create sns topic if not created already
            logging.info("Creating session")
            session = boto3.session.Session()
            logging.info("Creating client")
            sns_client = session.client('sns', region_name=self.region)
            logging.info("Creating SNS topic " + sns_topic)
            response = sns_client.create_topic(Name=sns_topic)
            topic_arn = response['TopicArn']
            logging.info("subscribe arn =  " + topic_arn)
           
            # First check if already subscribed
            if (self.check_subscribed_to_topic(sns_client, topic_arn, email_addr) == True):
                logging.info("AuctionManager:subscribe_user_to_auction email " + email_addr + " already subscribed to topic " + sns_topic )
                return True
            sns_client.subscribe(TopicArn=topic_arn, Protocol='email', Endpoint=email_addr)
            logging.info("AuctionManager:subscribe_user_to_auction email " + email_addr + " successfully subscribed to topic " + sns_topic )
            if (phone != ''):
                # Check phone number format
                formatted_phone_no = phonenumbers.parse(phone, "IE")
                formatted_phone = f"+353{phone}";
                logging.info(f"AuctionManager:subscribe_user phone {formatted_phone} to topic {sns_topic}" )
                sns_client.subscribe(TopicArn=topic_arn, Protocol='sms', Endpoint=formatted_phone)
                logging.info("AuctionManager:subscribe_user phone {formatted_phone} successfully subscribed to topic {sns_topic}" )
            
        except ClientError as boto_exception:
            logging.error("AuctionManager:boto_exception")
            logging.error(boto_exception)
            #raise boto_exception
        except Exception as general_exception:
            logging.error("AuctionManager:general_exception")
            logging.error(general_exception)
            raise general_exception
        return True



    #Perform sanity check on bids
    def validate_bid(self, bid_amount, max_bid, bid_time, auction_close) :
        ## Check that a bid is valid
        # Is it high enough?
        if (bid_amount < max_bid):
            return False
        # Is the auction closed?
        if (bid_time > auction_close):
            return False
        return True



    def store_primary_image(self, primary_image, property_id) :
        try:
            logging.info(f"store_primary_image:File {primary_image} with property_id  {property_id} of size {primary_image.size} and content type {primary_image.content_type}.")
            
            file_name = f"{primary_image}_id_{property_id}"
            logging.info(f"store_primary_image:Uploading {file_name} to bucket {self.bucket_name} ")
            
            primary_image.seek(0)
            s3_client = boto3.client('s3', region_name=self.region)
            s3_client.upload_fileobj(
                primary_image,
                self.bucket_name,
                file_name,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': primary_image.content_type
                }
            )

            file_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_name}"
            logging.info(f"File '{file_name}' uploaded successfully to {file_url}.")
        except ClientError as boto_exception:
            logging.error("AuctionManager:store_primary_image:boto_exception")
            logging.error(boto_exception)
            raise boto_exception
        except Exception as general_exception:
            logging.error("AuctionManager:store_primary_image:general_exception")
            logging.error(general_exception)
            raise general_exception
        return file_url

        
