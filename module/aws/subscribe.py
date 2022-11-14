from connection import sns_client

response = sns_client.subscribe(
    TopicArn="arn:aws:sns:us-east-1:285223778463:notifiacion", 
    Protocol="email", 
    Endpoint= "joanstevan99@gmail.com",
    ReturnSubscriptionArn=True
)

print(response) 
