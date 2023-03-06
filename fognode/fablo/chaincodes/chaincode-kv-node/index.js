const { Contract } = require("fabric-contract-api");
const crypto = require("crypto");
const { encrypt, decrypt } = require("./crypto");
const { sendDatatoBlockchain } = require("./utils");

class KVContract extends Contract {
  constructor() {
    super("KVContract");
  }

  async instantiate() {
    // function that will be invoked on chaincode instantiation
  }

  async registerSensor(ctx, key, value) {
    const hash = encrypt(Buffer.from(value, "utf8"));
    await ctx.stub.putState(key, Buffer.from(JSON.stringify(hash)));
    return { success: "Ok: Sensor Registered on Network" };
  }

  async getSensor(ctx, key) {
    const buffer = await ctx.stub.getState(key);
    if (!buffer || !buffer.length) return { error: "NOT_FOUND" };
    //const hash = buffer.toString();
    return { success: "Ok: Sensor is registered" };
  }

  async put(ctx, key, value) {
    value = JSON.parse(value.replaceAll("'", '"'));

    // We could store the data on the ledger as is, but we want to
    // send it  to another blockchain where it would be hashed and
    // stored and then the actual data would be stored off chain on minio

    let data = {
      temperature: value.temperature,
      timestamp: value.timestamp,
      org: value.org,
      device: value.device,
      arrivalTime: new Date().toISOString(), // time when the data arrived at the fog node
    };

    const buffer = await ctx.stub.getState("TartuCityCouncil:sensorOne"); //TODO: This should be the key of the sensor. Using a Static value for now

    const hashed_secret = encrypt(
      Buffer.from("TartuCityCouncil:sensorOne@ut", "utf8")
    );
    if (!buffer || !buffer.length) return { error: "Sensor is not registered" };
    if (decrypt(JSON.parse(buffer.toString())) !== decrypt(hashed_secret)) {
      return { error: "Sensor not registered" };
    }

    const blockchainID = data.org + ":" + data.device + ":" + data.timestamp; // this is the unique ID for the data on the blockchain. It is a combination of the org, device and timestamp and its the same from the fog node to the blockchain
    data.departTimeFromFogNode = new Date().toISOString(); // time when the data left the fog node
    // ? Unsure, should the payload be constructed here or in the utils.js file?
    let payload = {
      method: "KVContract:put",
      args: [blockchainID, JSON.stringify(data)],
    };

    // send data to blockchain
    console.log("Sending data to blockchain");
    sendDatatoBlockchain(payload);
    // TODO: We do not need to store anything on the ledger. Commenting out for later
    await ctx.stub.putState(key, Buffer.from(JSON.stringify(data)));
    return { success: "OK" };
  }

  async get(ctx, key) {
    const buffer = await ctx.stub.getState(key);
    if (!buffer || !buffer.length) return { error: "NOT_FOUND" };
    return { success: buffer.toString() };
  }

  async delete(ctx, id) {
    const exists = await this.assetExists(ctx, id);
    if (!exists) {
      throw new Error(`The asset ${id} does not exist`);
    }
    return ctx.stub.delete(id);
  }

  // AssetExists returns true when asset with given ID exists in world state.
  async assetExists(ctx, id) {
    const assetJSON = await ctx.stub.get(id);
    return assetJSON && assetJSON.length > 0;
  }
}

exports.contracts = [KVContract];
