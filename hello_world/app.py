import json
import boto3
import os

client = boto3.client('redshift')
redshiftClusterId = os.environ['REDSHIFT_CLUSTER_ID']
checkLastResize = (os.environ['CHECK_LAST_RESIZE'] == 'true')
targetNodeCount = int(os.environ['TARGET_NODE_COUNT'])

def lambda_handler(event, context):

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    #if(event['queryStringParameters']['target']):
    #    resizeTarget = event['queryStringParameters']['target']
    #else:
    #    resizeTarget = 2

    print('redshiftClusterId: ' + redshiftClusterId + ', checkLastResize: ' + str(checkLastResize) + '. targetNodeCount: ' + str(targetNodeCount))

    currentNodeCount = 0
    try:
        response = client.describe_clusters(ClusterIdentifier = redshiftClusterId)
        currentNodeCount = response['Clusters'][0]['NumberOfNodes']
    except client.exceptions.ClusterNotFoundFault:
        currentNodeCount = 0
    print('currentNodeCount: ' + str(currentNodeCount))

    if(currentNodeCount == targetNodeCount or currentNodeCount == 0):
        msg = 'No cluster found or current node count already = target, no action done!'
        print(msg)
        return {
            "statusCode": 400,
            "body": msg
        }

    if(checkLastResize):
        lastResizeFailed = False
    else:
        lastResizeFailed = True

    try:
        response = client.describe_resize(ClusterIdentifier = redshiftClusterId)
        print('Resize status = ' + response['Status'])
        print('Resize type = ' + response['ResizeType'])
        if(response['Status'] == 'FAILED'):
            print('Last resize failed!')
            lastResizeFailed = True;
    except client.exceptions.ResizeNotFoundFault:
        print('No previous resize action found! No action done.')

    if(lastResizeFailed):
        print('last resize failed, do the resize here! target no. of nodes = ' + str(targetNodeCount))
        response = client.resize_cluster(
            ClusterIdentifier=redshiftClusterId,
            NumberOfNodes=targetNodeCount
            )
        result = json.dumps(response, indent = 4, sort_keys=True, default=str)
    else:
        result = 'No last resize or last resize not failed, do nothing!'

    print(result)

    return {
        "statusCode": 200,
        "body": result
    }
