const { Contract } = require("fabric-contract-api");
const crypto = require("crypto");
const { hashData, compareHash } = require("./hash-helper");
const Client = require("./utils/minio-utils");
const config = require("./config.js");
const { DateTime } = require("luxon");

class KVContract extends Contract {
  async instantiate() {
    // function that will be invoked on chaincode instantiation
  }

  async put(ctx, key, data) {
    const valueObj = JSON.parse(data);
    valueObj.arrivalTimeFromFognode = DateTime.now()
      .setZone("Europe/Helsinki")
      .toISO(); // time when the data arrived at the Primary Blockchain
    const minioClient = new Client(
      config.MINIO_URL,
      config.MINIO_PORT,
      config.MINIO_ACCESS_KEY,
      config.MINIO_SECRET
    );
    valueObj.departureTimeFromPrimaryBlockchain = DateTime.now()
      .setZone("Europe/Helsinki")
      .toISO(); // time when the data left the Primary Blockchain
    const payload = JSON.stringify(valueObj);
    const payloadHash = hashData(payload);
    await ctx.stub.putState(key, payloadHash);
    const bucketName = `${valueObj.org}${valueObj.device}Bucket`.toLowerCase();
    const objectName = `${valueObj.timestamp}-${valueObj.org}-${valueObj.device}.json`;
    minioClient.putJson(
      bucketName,
      objectName,
      valueObj,
      (err) => err && console.log(err)
    );
    return { success: "OK" };
  }

  async get(ctx, key) {
    const buffer = await ctx.stub.getState(key);
    if (!buffer || !buffer.length) return { error: "NOT_FOUND" };
    return { success: buffer.toString() };
  }

  async getAndCompareHash(ctx, data, key) {
    const buffer = await ctx.stub.getState(key); // get the hash from the ledger
    if (!buffer || !buffer.length) return "Key Not Found"; // if the hash is not found, return an error
    const hashMatch = compareHash(data, buffer.toString());
    return { success: hashMatch };
  }

  async delete(ctx, key) {
    const exists = await this.assetExists(ctx, key);
    if (!exists) {
      throw new Error(`The asset ${key} does not exist`);
    }
    return ctx.stub.delete(key);
  }

  // AssetExists returns true when asset with given ID exists in world state.
  async assetExists(ctx, key) {
    const assetJSON = await ctx.stub.get(key);
    return assetJSON && assetJSON.length > 0;
  }
}

exports.contracts = [KVContract];
