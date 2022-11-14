from connection import sns_client

response = sns_client.publish(
    TopicArn="arn:aws:sns:us-east-1:285223778463:notifiacion",
    Message="Hola mundo",
    Subject="Prueba"
)

print(response)