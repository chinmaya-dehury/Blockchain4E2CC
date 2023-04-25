const fs = require("fs");
const Minio = require("minio");

class Client {
  constructor(endPoint, port, accessKey, secretKey) {
    this.client = new Minio.Client({
      endPoint,
      port,
      accessKey,
      secretKey,
      useSSL: false,
    });
  }

  async putJson(bucketName, objectName, d) {
    // create a new bucket, if not existing yet
    if (!(await this.client.bucketExists(bucketName))) {
      await this.client.makeBucket(bucketName, "eu-west-1");
    }

    // prepare data and corresponding data stream
    const data = JSON.stringify(d);

    // put data as object into the bucket
    await this.client.putObject(bucketName, objectName, data);
  }
}

module.exports = Client;
