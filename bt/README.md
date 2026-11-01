# BT — Blockchain Technology practicals

Hands-on lab work for the Blockchain Technology syllabus: MetaMask, wallets,
Solidity smart contracts, a Hyperledger business network, and a survey of
blockchain types and use cases.

Everything except Hyperledger runs on the free **Sepolia** testnet with
MetaMask and Remix — no paid tools.

## Contents

| # | Practical | File | Type |
| --- | --- | --- | --- |
| 1 | Install MetaMask + study Ether spent per transaction | [`01_MetaMaskInstallation.md`](01_MetaMaskInstallation.md) | Instructions |
| 2 | Create your own wallet with MetaMask | [`02_CreateWallet.md`](02_CreateWallet.md) | Instructions |
| 3 | Bank account smart contract (deposit / withdraw / balance) | [`03_BankAccount.sol`](03_BankAccount.sol) | Solidity |
| 4 | Student data using structs, arrays and fallback | [`04_StudentData.sol`](04_StudentData.sol) | Solidity |
| 5 | Survey: blockchain types and real-time use cases | [`05_SurveyReport.md`](05_SurveyReport.md) | Report |
| 6 | Business network on Hyperledger Fabric | [`06_HyperledgerBusinessNetwork/`](06_HyperledgerBusinessNetwork/) | Chaincode + instructions |

## Prerequisites

- Chrome / Brave / Edge / Firefox
- MetaMask extension ([install guide](01_MetaMaskInstallation.md))
- A wallet on **Sepolia** with test ETH
  ([faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia))
- [Remix IDE](https://remix.ethereum.org)

Hyperledger practical 6 additionally needs Docker, Node.js, Go and the
official `fabric-samples` repository; see its README.

---

## Practical 3 — Bank account contract

[`03_BankAccount.sol`](03_BankAccount.sol) implements per-customer balances,
`deposit`, `withdraw`, `transferTo`, `balanceOf`, ownership transfer and
events.

### Deploy in Remix

1. Open **https://remix.ethereum.org**.
2. Create a new file named `BankAccount.sol` and paste the contract.
3. Open the **Solidity compiler** tab. Choose compiler **0.8.20** or newer.
4. Click **Compile BankAccount.sol** — wait for the green checkmark.
5. Open **Deploy & Run Transactions**.
6. Set **Environment** to **Injected Provider - MetaMask**.
7. Confirm MetaMask is on **Sepolia** and approve the connection.
8. Click **Deploy** → **Confirm** in MetaMask.
9. Expand the contract under **Deployed Contracts**.

### Test cases

| Action | Input in Remix | Expected result |
| --- | --- | --- |
| Deposit | Value = `0.5` Ether → **deposit** | `Deposited` event; `balanceOf(you)` = `500000000000000000` |
| Show balance | **balanceOf** with your address | the same wei value |
| Withdraw | **withdraw** `200000000000000000` | `Withdrawn` event; balance 0.3 ETH |
| Over-withdraw | **withdraw** `999000000000000000` | transaction reverts with `InsufficientBalance` |
| Transfer | **transferTo** classmate address + `100000000000000000` | `Transferred` event; their balance 0.1 ETH |
| Owner | **owner** | address that deployed the contract |
| Contract balance | **contractBalance** | total ETH held |

Wei reminder: `1 ETH = 10^18 wei`. Remix accepts `0.5 ether` directly in a
`uint256` field.

### What to explain

- `msg.sender` is the caller; never use `tx.origin` for authorisation.
- The balance is reduced **before** the external `call` (checks-effects-
  interactions), which prevents re-entrancy.
- Custom errors are cheaper than long `require` strings.
- `contractBalance` should equal the sum of all customer balances.

---

## Practical 4 — Student data: structs, arrays, fallback

[`04_StudentData.sol`](04_StudentData.sol) uses:

- a **struct** `Student { id, name, course, age }`
- a dynamic **array** `Student[] students`
- a **mapping** `id -> array position` for O(1) lookup
- a payable **fallback** (and `receive`) that records unknown calls

### Deploy

Same Remix steps as practical 3, but create `StudentData.sol` and deploy
`StudentData`.

### Test cases

| Action | Input | Expected result |
| --- | --- | --- |
| Add student | `1, "Asha", "Computer", 20` → **addStudent** | `StudentAdded` event; `studentCount` = 1 |
| Read one | **getStudent** `1` | tuple `(1, "Asha", "Computer", 20)` |
| Read all | **getAllStudents** | array containing the record |
| Duplicate id | add id `1` again | reverts with `StudentAlreadyExists` |
| Update | `1, "Asha Patil", "IT", 21` → **updateStudent** | `StudentUpdated`; `getStudent` shows new values |
| Remove | **removeStudent** `1` | `StudentRemoved`; `studentCount` = 0 |
| Plain ETH | Low level interactions → Value `0.1`, empty calldata → **Transact** | `Received` event; `totalDonations` = 0.1 ETH |
| Fallback | Calldata `0xdeadbeef`, Value `0.1` Ether → **Transact** | `FallbackReceived`; `lastFallbackData` = `0xdeadbeef` |
| Bad student | empty name or age 0 | reverts with `InvalidStudentData` |

### Observe gas and transaction fee

Open the Remix terminal after each transaction. It shows **gas used**; the
transaction details show **gas price** and **transaction cost**.

```
transaction fee (ETH) = gas used × gas price (gwei) / 10^9
```

Record at least these in your journal:

| Operation | Gas used | Gas price (gwei) | Fee (ETH) |
| --- | ---: | ---: | ---: |
| Deploy StudentData | | | |
| addStudent (first) | | | |
| addStudent (second) | | | |
| updateStudent | | | |
| removeStudent | | | |
| receive (plain ETH) | | | |
| fallback (unknown calldata) | | | |

The first `addStudent` is expensive because it creates new storage; later
writes into existing slots cost less. Reading (`getStudent`,
`getAllStudents`, `studentCount`) is free when called as a view.

### Why fallback matters

- `receive()` runs for plain ETH with empty calldata.
- `fallback()` runs for an unknown function selector.
- Both are **payable** here, so stray payments are recorded instead of
  reverting.
- A fallback is also the hook used by proxy/upgradeable contracts.
- Keep fallback logic minimal: it can be called with arbitrary data and gas.

---

## Practical 5 — Survey report

See [`05_SurveyReport.md`](05_SurveyReport.md): blockchain types (public,
private, consortium, hybrid), a 50-respondent sample survey, and real
deployments in payments, trade finance, KYC, CBDC and audit.

## Practical 6 — Hyperledger business network

See [`06_HyperledgerBusinessNetwork/README.md`](06_HyperledgerBusinessNetwork/README.md).
It contains a JavaScript chaincode contract for a simple business registry
(create / read / update / delete / list) and step-by-step commands to run it
on the official Fabric `test-network`.

---

## Verification checklist

- [ ] MetaMask installed, wallet created, seed phrase on paper only
- [ ] Network = Sepolia, test ETH available
- [ ] `03_BankAccount.sol` compiles with solc ≥ 0.8.20
- [ ] Deposit / withdraw / transfer / over-withdraw tested
- [ ] `04_StudentData.sol` compiles
- [ ] add / get / update / remove student tested
- [ ] `receive` triggered by plain ETH
- [ ] `fallback` triggered by `0xdeadbeef`
- [ ] Gas used recorded for deploy, add, update, remove, receive, fallback
- [ ] Survey report filled with name and roll number
- [ ] Hyperledger chaincode packaged and invoked on `test-network`

## Safety

- Use a dedicated test wallet; never reuse a wallet that holds real funds.
- Test ETH has no value — do not buy ETH for this practical.
- Never share the seed phrase or private key, including in screenshots.
- Confirm the network in MetaMask before signing; mainnet costs real money.

## Viva questions

1. Difference between `receive()` and `fallback()`?
2. Why is `msg.sender` preferred over `tx.origin`?
3. What is re-entrancy, and how does checks-effects-interactions prevent it?
4. Why use a struct and a dynamic array for student records?
5. How does the `indexOf` mapping make lookup and removal O(1)?
6. What is gas, and why does storage cost more than computation?
7. How is the transaction fee calculated from gas used and gas price?
8. Public vs private vs consortium vs hybrid blockchain — one example each.
9. What does Hyperledger Fabric use instead of public mining?
10. Why use a testnet instead of mainnet for development?
