const fetch = require("node-fetch");
const config = require("./config.js");
async function getToken() {
  const TOKEN_ENDPOINT = config.TOKEN_ENDPOINT;
  const headers = {
    Authorization: "Bearer ",
    "Content-Type": "application/json",
  };
  const response = await fetch(TOKEN_ENDPOINT, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({ id: "admin", secret: "adminpw" }),
  });
  const data = await response.json();
  return data.token;
}

async function sendDatatoBlockchain(data) {
  const PRIMARY_BLOCKCHAIN_ENDPOINT = config.PRIMARY_BLOCKCHAIN_ENDPOINT;
  const headers = {
    Authorization: "Bearer " + (await getToken()),
    "Content-Type": "application/json",
  };
  const response = await fetch(PRIMARY_BLOCKCHAIN_ENDPOINT, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(data),
  });
  console.log("Sending data to endpoint: " + PRIMARY_BLOCKCHAIN_ENDPOINT);
  return await response.json();
}
module.exports = {
  sendDatatoBlockchain,
};
