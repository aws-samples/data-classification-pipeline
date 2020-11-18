const fs = require('fs').promises;

const response = require('cfn-response-promise');
const AWS = require('aws-sdk');
const s3 = new AWS.S3();

const FUNCTION_TIMEOUT = 10 * 1000;
const GLUE_CURATED_BUCKET = process.env.GLUE_CURATED_BUCKET;
const GLUE_ASSETS_BUCKET = process.env.GLUE_ASSETS_BUCKET;
const ACCOUNT_ID = process.env.ACCOUNT_ID;

const SCRIPT_FILENAME = 'dcp-script.py';
const SCRIPT_KEY = `scripts/${SCRIPT_FILENAME}`;

exports.handler = async(event, context) => {
    logRequest(event, context);
    try {
        setTimeoutWatchDog(event, context);

        let data = await fs.readFile(SCRIPT_FILENAME);
        let script = data.toString().replace(/GLUE_CURATED_BUCKET/g, `${GLUE_CURATED_BUCKET}`);
        let body = script.toString().replace(/ACCOUNT_ID/g, `${ACCOUNT_ID}`);
        let params = { Key: SCRIPT_KEY, Bucket: GLUE_ASSETS_BUCKET, Body: body };

        if (event.RequestType == 'Create' || event.RequestType == 'Update') {
            console.log('Creating Glue script.');
            await s3.putObject(params).promise();
        }

        await response.send(event, context, response.SUCCESS);
    } catch (err) {
        await response.send(event, context, response.FAILED, err);
    }
};

function setTimeoutWatchDog(event, context) {
    const timeoutHandler = async() => {
        await response.send(event, context, response.FAILED, { 'error': 'Resource timeout' });
    };

    setTimeout(timeoutHandler, FUNCTION_TIMEOUT);
}

function logRequest(event, context) {
    console.log(`"${event.StackId}" "${event.RequestId}" "${context.logStreamName}" "${event.LogicalResourceId}" "${event.ResponseURL}"`);
}