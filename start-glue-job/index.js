const AWS = require('aws-sdk');
var glue = new AWS.Glue();

const WORKFLOW_NAME = process.env.WORKFLOW_NAME;

exports.handler = async(event) => {
    let s3 = event.Records[0].s3;
    console.log(`Starting DCP Glue Workflow for s3://${s3.bucket.name}/${s3.object.key}`);
    
    return await glue.startWorkflowRun({ Name: WORKFLOW_NAME }).promise();
};