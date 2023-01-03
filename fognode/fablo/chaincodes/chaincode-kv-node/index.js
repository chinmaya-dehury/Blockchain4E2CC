const { Contract } = require("fabric-contract-api");
const crypto = require("crypto");
const { encrypt, decrypt } = require("./crypto");

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
    // send it off-chain to another blockchain where it would be hashed and
    // stored and then the actual hash would be stored off chain to minio

    let data = {
      temperature: value.temperature,
      timestamp: value.timestamp,
      org: value.org,
      device: value.device,
      arrivalTime: new Date().toISOString(), // time when the data arrived at the fog node
    };

    const buffer = await ctx.stub.getState("TartuCityCouncil:sensorOne");
    const hash = encrypt(Buffer.from("Hello World!", "utf8"));

    const hashed_secret = encrypt(
      Buffer.from("TartuCityCouncil:sensorOne@ut", "utf8")
    );
    if (!buffer || !buffer.length) return { error: "Sensor is not registered" };
    if (decrypt(JSON.parse(buffer.toString())) !== decrypt(hashed_secret)) {
      return { error: "Sensor is not registered" };
    }

    await ctx.stub.putState(key, Buffer.from(JSON.stringify(data)));
    return { success: "OK" };
  }

  async get(ctx, key) {
    const buffer = await ctx.stub.getState(key);
    if (!buffer || !buffer.length) return { error: "NOT_FOUND" };
    return { success: buffer.toString() };
  }
}
const hash = encrypt(Buffer.from("Hello World!", "utf8"));

const hash_2 = encrypt(Buffer.from("Hello World!", "utf8"));

console.log(typeof hash);
console.log(typeof hash_2);

console.log(decrypt(hash) !== decrypt(hash_2));

exports.contracts = [KVContract];
