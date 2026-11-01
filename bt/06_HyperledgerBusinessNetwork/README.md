# 6. Business network on Hyperledger Fabric

Hyperledger Fabric is a **permissioned** blockchain framework. Members are
known organisations, each running a peer; an ordering service puts
transactions in blocks, and a channel keeps the ledger private to its
members. There is **no mining and no gas fee** — the cost is the
infrastructure you run.

This practical deploys a small **business registry** chaincode:

| Function | Purpose |
| --- | --- |
| `createBusiness` | add `{id, name, owner, category, active}` |
| `readBusiness` | read one business |
| `updateBusiness` | change an existing record |
| `deleteBusiness` | remove a record |
| `businessExists` | check an id |
| `getAllBusinesses` | list every record |

The chaincode is in [`chaincode/index.js`](chaincode/index.js) and its
dependencies are in [`chaincode/package.json`](chaincode/package.json).

---

## Prerequisites

| Tool | Check |
| --- | --- |
| Docker + Docker Compose | `docker --version` |
| Go 1.20+ | `go version` |
| Node.js 18+ | `node --version` |
| jq | `jq --version` |
| git, curl | `git --version` |

Install Docker Desktop or Docker Engine, then add your user to the docker
group on Linux (`sudo usermod -aG docker $USER`, log out and back in).

## Step 1 — Get Fabric samples and binaries

```bash
cd ~
git clone https://github.com/hyperledger/fabric-samples.git
cd fabric-samples
curl -sSL https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh \
  | bash -s -- --fabric-version 2.5.9 --ca-version 1.5.15
```

This downloads the peer/orderer binaries into `fabric-samples/bin` and the
Fabric Docker images. Verify:

```bash
./bin/peer version
```

## Step 2 — Copy this chaincode into fabric-samples

```bash
cp -r /path/to/collage/bt/06_HyperledgerBusinessNetwork/chaincode \
      ~/fabric-samples/business-network
```

Remove any `node_modules` copied from another machine; Fabric installs the
dependencies inside its Docker builder.

## Step 3 — Start the test network

```bash
cd ~/fabric-samples/test-network
./network.sh down
./network.sh up createChannel -c mychannel -ca
```

Expected: both organisations (`Org1`, `Org2`) and the orderer start, and a
channel named `mychannel` is created. Wait until you see
`Channel 'mychannel' created` and `Both orgs have successfully joined`.

## Step 4 — Deploy the chaincode

```bash
./network.sh deployCC \
  -ccn business \
  -ccp ../business-network \
  -ccl javascript \
  -c mychannel
```

Expected: `Chaincode definition approved on peer0.org1`, `... org2`, then
`Committed chaincode definition for 'business' on channel 'mychannel'`.

## Step 5 — Set the Org1 environment

Run this in the same terminal:

```bash
export PATH=${PWD}/../bin:$PATH
export FABRIC_CFG_PATH=$PWD/../config/
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
```

The long certificate path is why the official tutorial also provides a
`setOrg1.sh`-style script; exporting once is enough for this practical.

## Step 6 — Invoke and query

Create a business:

```bash
peer chaincode invoke \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n business \
  -c '{"function":"createBusiness","Args":["B001","Acme Traders","Asha","Retail","true"]}'
```

Expected:

```
Chaincode invoke successful. result: status:200 payload:"{\"id\":\"B001\",...}"
```

Read it back (query is free and does not create a block):

```bash
peer chaincode query -C mychannel -n business \
  -c '{"function":"readBusiness","Args":["B001"]}'
```

Expected:

```json
{"id":"B001","name":"Acme Traders","owner":"Asha","category":"Retail","active":true,"updatedBy":"...","updatedAt":"..."}
```

List everything:

```bash
peer chaincode query -C mychannel -n business \
  -c '{"function":"getAllBusinesses","Args":[]}'
```

Update and delete:

```bash
peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n business \
  -c '{"function":"updateBusiness","Args":["B001","Acme Traders Pvt Ltd","Asha","Wholesale","true"]}'

peer chaincode invoke -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel -n business \
  -c '{"function":"deleteBusiness","Args":["B001"]}'
```

## Step 7 — Write the observation

Record for the report:

| Observation | Value |
| --- | --- |
| Channel name | `mychannel` |
| Organisations | Org1, Org2 |
| Chaincode language | JavaScript |
| Create latency | time from invoke to status 200 |
| Query latency | almost instant (no block) |
| Consensus | ordering service (no mining/gas) |
| Access control | MSP identities + channel membership |

## Step 8 — Clean up

```bash
cd ~/fabric-samples/test-network
./network.sh down
docker system prune -f
```

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `peer: command not found` | Add `fabric-samples/bin` to `PATH` (Step 5) |
| Docker permission denied | Add user to the `docker` group and re-login |
| `failed to connect to orderer` | Run `./network.sh down` then start again |
| Chaincode build fails | Check Node version and that `fabric-contract-api` is declared |
| `business B001 already exists` | Use a new id or delete the old record first |
| Wrong org context | Re-export the Org1 variables from Step 5 |

## What to explain in the viva

- Fabric is permissioned: membership is controlled by MSP certificates.
- A channel is a private ledger shared only by its members.
- The ordering service orders transactions; peers validate and commit.
- There is no gas; performance depends on block size, endorsement policy and
  the number of peers.
- Chaincode state is a key-value world state backed by an immutable
  blockchain history.
- `getStateByRange` scans keys; production contracts usually maintain an
  index or use rich queries for large datasets.
