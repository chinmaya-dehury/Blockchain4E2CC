const crypto = require("crypto");

function hashData(data, salt = "ut@ie@hlf") {
  return crypto
    .createHash("sha256")
    .update(data)
    .update(salt, "utf8")
    .digest("hex");
}

function compareHash(data, hash, salt = "ut@ie@hlf") {
  const newHash = hashData(Buffer.from(JSON.stringify(data), "utf8"), salt);
  return newHash === hash;
}

module.exports = {
  hashData,
  compareHash,
};
