const core = require('@actions/core');
const github = require('@actions/github');
const exec = require('@actions/exec');

function run() {
    core.notice('Hello From Custom JavaScript Action !');
    // 1) Get Some Input Values
    const bucket = core.getInput('bucket', { required: true });
    const bucketRegion = core.getInput('bucket-region', { required: true });
    const distFolder = core.getInput('dist-folder', { required: true });

    // 2) Upload Files to S3
    const s3URI = `s3://${bucket}`;
    exec.exec(`aws s3 sync ${distFolder} ${s3URI} --region ${bucketRegion}`)

   // http://gha-custom-action-kode.s3-website-ap-southeast-2.amazonaws.com/
     const webSiteUrl = `http://${bucket}.s3-website-${bucketRegion}.amazonaws.com`;
     core.setOutput('website-url', webSiteUrl);
}

run();