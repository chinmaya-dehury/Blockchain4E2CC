const { Contract } = require("fabric-contract-api");
const crypto = require("crypto");

class KVContract extends Contract {
  constructor() {
    super("KVContract");
  }

  async instantiate() {
    // function that will be invoked on chaincode instantiation
  }

  async put(ctx, key, value) {
    value = JSON.parse(value.replaceAll("'", '"'));

    // We could store the data on the ledger as is, but we want to
    // send it off-chain to another blockchain where it would be hashed and
    // stored and then the actual hash would be stored off chain to minio

    let data = {
      temperature: value.temperature,
      timestamp: value.timestamp,
      org: value.org,
      device: value.device,
      arrivalTime: new Date().toISOString(), // time when the data arrived at the fog node
    };
    await ctx.stub.putState(key, Buffer.from(JSON.stringify(data)));
    return { success: "OK" };
  }

  async get(ctx, key) {
    const buffer = await ctx.stub.getState(key);
    if (!buffer || !buffer.length) return { error: "NOT_FOUND" };
    return { success: buffer.toString() };
  }
}

exports.contracts = [KVContract];
