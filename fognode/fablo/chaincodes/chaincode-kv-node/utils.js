const fetch = require("node-fetch");
async function getToken() {
  const TOKEN_ENDPOINT = "http://44.203.194.115:8801/user/enroll";
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
  const ENDPOINT =
    "http://3.84.37.18:8801/invoke/tartucitycouncilchannel/tartucitycouncil";
  const headers = {
    Authorization: "Bearer " + (await getToken()),
    "Content-Type": "application/json",
  };
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(data),
  });
  console.log("Sending data to endpoint: " + ENDPOINT);
  return await response.json();
  //console.log(_data);
}
module.exports = {
  sendDatatoBlockchain,
};
