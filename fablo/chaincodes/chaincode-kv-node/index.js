const { Contract } = require("fabric-contract-api");
const crypto = require("crypto");
const { encrypt, decrypt } = require("./crypto");
const Client = require("./utils/minio-utils");

class KVContract extends Contract {
  async instantiate() {
    // function that will be invoked on chaincode instantiation
  }

  async put(ctx, key, value) {
    // encrypt data before storing on ledger
    const hash = encrypt(Buffer.from(value, "utf8"));
    //console.log(typeof hash);
    const hashS = JSON.stringify(hash);
    // encrypt data before storing on ledger
    await ctx.stub.putState(key, hashS);
    //const hash = encrypt(Buffer.from(value, "utf8"));
    await ctx.stub.putState(key, hash);
    // send unencrypted data to minio
    const minioClient = new Client(
      process.env.MINIO_URL,
      process.env.MINIO_PORT,
      process.env.MINIO_ACCESS_KEY,
      process.env.MINIO_SECRET
    );
    const valueObj = JSON.parse(value);
    const bucketName = (
      valueObj.org +
      valueObj.device +
      "Bucket"
    ).toLowerCase();
    const objectName =
      "json/" +
      valueObj.timestamp.toString() +
      "-" +
      valueObj.org +
      "-" +
      valueObj.device +
      ".json";

    minioClient.putJson(bucketName, objectName, valueObj, function (err) {
      if (err) {
        return console.log(err);
      }
      console.log("File uploaded successfully.");
    });
    return { success: "OK" };
  }

  async get(ctx, key) {
    const buffer = await ctx.stub.getState(key);
    if (!buffer || !buffer.length) return { error: "NOT_FOUND" };
    return { success: buffer.toString() };
  }

  async putPrivateMessage(ctx, collection) {
    const transient = ctx.stub.getTransient();
    const message = transient.get("message");
    await ctx.stub.putPrivateData(collection, "message", message);
    return { success: "OK" };
  }

  async getPrivateMessage(ctx, collection) {
    const message = await ctx.stub.getPrivateData(collection, "message");
    const messageString = message.toBuffer
      ? message.toBuffer().toString()
      : message.toString();
    return { success: messageString };
  }

  async verifyPrivateMessage(ctx, collection) {
    const transient = ctx.stub.getTransient();
    const message = transient.get("message");
    const messageString = message.toBuffer
      ? message.toBuffer().toString()
      : message.toString();
    const currentHash = crypto
      .createHash("sha256")
      .update(messageString)
      .digest("hex");
    const privateDataHash = (
      await ctx.stub.getPrivateDataHash(collection, "message")
    ).toString("hex");
    if (privateDataHash !== currentHash) {
      return { error: "VERIFICATION_FAILED" };
    }
    return { success: "OK" };
  }
}

exports.contracts = [KVContract];
