# redshift-resize

This project contains source codes in python 3 that conduct elastic resize on a redshift cluster, the lambda is triggered by cloudwatch event schedule.

Folder structure:
- hello_world - Code for the application's Lambda function. 
- template.yaml - A template that defines the application's AWS resources.

## Deploy the Lambda application using SAM

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

To build and deploy your application for the first time, first git clone this repo and then run the following in your shell:

```bash
sam build
sam deploy -g
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts.

> Make sure to deploy the Lambda function to the same AWS region of your Redshift cluster.

## Environment Variables
After the deployment finished, please goto the Lambda function in AWS console, you will see the following environment variables in the function, please modify them to suit your needs: 

| Env. Variables      | Description                                                                                      | Default Value         |
|---------------------|--------------------------------------------------------------------------------------------------|-----------------------|
| REDSHIFT_CLUSTER_ID | The identifier of the Redshift cluster to be resized                                             | redshift-test-cluster |
| TARGET_NODE_COUNT   | The target number of nodes                                                                       | 4                     |
| CHECK_LAST_RESIZE   | "true" then the lambda will only trigger a Redshift elastic resize if last resize attempt failed | true                  |

## Schedule the Lambda function
Go to Cloudwatch Event Rules in AWS console, you can find a rule named ***RedshiftResizeSchedule***, the schedule will trigger the Lambda function to resize Redshift cluster, click it and edit the schedule, remember to **enable** the rule.
> It is suggested to schedule this Lambda one hour after the normal Redshift elastic resize takes place, the Lambda will check if last resize attempt failed, if yes it will try a elastic resize again.
