# BT — Blockchain Technology practicals

Hands-on lab work for blockchain basics: set up a wallet, deploy Solidity
smart contracts, understand `receive` / `fallback`, and study real banking use
cases.

**No paid tools are required.** Contracts run on the free **Sepolia** testnet
using Remix IDE and MetaMask.

## Contents

| # | Practical | File | Type |
| --- | --- | --- | --- |
| 1 | Install MetaMask | [`01_MetaMaskInstallation.md`](01_MetaMaskInstallation.md) | Instructions |
| 2 | Create your own wallet | [`02_CreateWallet.md`](02_CreateWallet.md) | Instructions |
| 3 | Smart contract for a bank account | [`03_BankAccount.sol`](03_BankAccount.sol) | Solidity |
| 4 | Smart contract with fallback | [`04_BankWithFallback.sol`](04_BankWithFallback.sol) | Solidity |
| 5 | Survey report + real-time use cases | [`05_SurveyReport.md`](05_SurveyReport.md) | Report |

## Prerequisites

- Chrome / Brave / Edge / Firefox
- MetaMask extension ([install guide](01_MetaMaskInstallation.md))
- A wallet on the **Sepolia** network with test ETH
  ([faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia))
- Internet access to open [Remix IDE](https://remix.ethereum.org)

No Node.js, Hardhat or local blockchain is needed. (If you want to compile
locally: `npm install -g solc` then
`solcjs --bin --abi bt/03_BankAccount.sol`.)

---

## Practical 3 — Bank account contract

[`03_BankAccount.sol`](03_BankAccount.sol) implements per-customer balances,
deposit, withdraw, transfer, ownership transfer and events.

### Deploy in Remix (10 steps)

1. Open **https://remix.ethereum.org**.
2. In the **File Explorer** (left panel) click **Create new file** and name it
   `BankAccount.sol`.
3. Paste the full contents of `03_BankAccount.sol`.
4. Click the **Solidity compiler** icon (the "S" logo).
5. Set **Compiler** to `0.8.20` or newer (e.g. `0.8.26`).
6. Click **Compile BankAccount.sol** — a green checkmark means success.
7. Click the **Deploy & Run Transactions** icon (Ethereum logo).
8. Set **Environment** to **Injected Provider - MetaMask**.
9. Approve the connection in MetaMask and confirm the network is **Sepolia**.
10. Click **Deploy** → **Confirm** in MetaMask. Your contract appears under
    **Deployed Contracts**.

### Test it

Expand the deployed contract and use the orange/blue buttons:

| Action | How | Expected result |
| --- | --- | --- |
| Deposit 0.5 ETH | Put `0.5` in **Value** (unit = Ether, red field next to Deploy) → click **deposit** → confirm | `Deposited(...)` event, `balanceOf(yourAddress)` = `500000000000000000` |
| Check balance | Call **balanceOf** with your address | wei value as above |
| Withdraw 0.2 ETH | Call **withdraw** with `200000000000000000` | `Withdrawn(...)`, balance drops to 0.3 ETH |
| Over-withdraw | Call **withdraw** with `999000000000000000` | Transaction **reverts**: `InsufficientBalance(requested, available)` |
| Transfer | Call **transferTo** with a classmate's address + `100000000000000000` | `Transferred(...)`, their `balanceOf` = 0.1 ETH |
| Owner check | Call **owner** | the address that deployed the contract |
| Transfer ownership | Call **transferOwnership** with another address | `OwnershipTransferred(...)` |
| Contract balance | Call **contractBalance** | equals the sum of all customer balances |

> **Wei reminder:** 1 ETH = 10¹⁸ wei. In Remix you can write
> `0.5 ether` directly in a `uint256` field — Solidity-style literals are
> accepted in the input box.

### Security points to explain in the viva

- `msg.sender` (not `tx.origin`) identifies the caller.
- Balance is reduced **before** the external `call` — checks-effects-
  interactions, which blocks re-entrancy.
- `call` is used instead of `transfer` so the receiver can use more than
  2300 gas; the return value is checked.
- Custom errors (`error InsufficientBalance(...)`) are cheaper than long
  `require` strings.
- `totalDeposits` and `contractBalance` should stay in sync — a mismatch means
  someone sent ETH without calling `deposit` (see practical 4).

---

## Practical 4 — Contract with fallback

[`04_BankWithFallback.sol`](04_BankWithFallback.sol) adds:

```solidity
receive()  external payable   // plain ETH, empty calldata
fallback() external payable   // unknown function / ETH + calldata
```

Deploy it exactly like practical 3 (new file `BankWithFallback.sol`,
same compiler). Then test:

| Test | How in Remix | Expected result |
| --- | --- | --- |
| Plain ETH → `receive` | In **Low level interactions**, leave **Calldata** empty, set **Value** = `0.1` Ether, click **Transact** (or send 0.1 ETH from MetaMask to the contract address) | `Received(...)` event; `balances(yourAddress)` = 0.1 ETH |
| Unknown function → `fallback` | **Low level interactions** → Calldata = `0xdeadbeef`, Value = `0.1` Ether → **Transact** | `FallbackTriggered(...)` event with `0xdeadbeef`; `lastFallbackSender` = you; `lastFallbackData` = `0xdeadbeef` |
| Read the selector | Call **lastFallbackSelector** | `0xdeadbeef` |
| Unknown call, no ETH | Calldata = `0x12345678`, Value = 0 | Still succeeds and logs; balance unchanged |
| Withdraw | Call **withdraw** with an amount ≤ balance | ETH returned, `Withdrawn(...)` |
| Over-withdraw | Amount > balance | Reverts with `InsufficientBalance` |
| No `receive` case | (explain) remove/rename `receive` and repeat the plain-ETH test | ETH then lands in `fallback`, still accepted because it is payable |

### Why `receive` and `fallback` matter

- Wallets and exchanges send plain ETH with **no calldata** — that is
  `receive`.
- Proxies, multicall contracts and users can send **unknown selectors** —
  that is `fallback`.
- If both are missing, the contract **rejects** plain ETH. If they are
  non-payable, ETH transfers revert.
- A payable fallback is convenient but risky: it accepts anything. Keep it
  minimal (log + return) unless you deliberately want to accept stray
  payments.
- `fallback` is also the hook used by **proxy/upgradeable** contracts to
  `delegatecall` into an implementation contract.

---

## Practical 5 — Survey and real-time use cases

See [`05_SurveyReport.md`](05_SurveyReport.md). It contains the questionnaire
results (n = 50 sample), analysis, and documented deployments in cross-border
payments, trade finance, KYC, CBDC and settlement, plus Indian examples
(RBI e₹, SBI, ICICI, HDFC).

---

## Quick verification checklist

- [ ] MetaMask installed and pinned
- [ ] Fresh wallet created; seed phrase written on paper only
- [ ] Network = Sepolia; test ETH visible
- [ ] `03_BankAccount.sol` compiles with solc ≥ 0.8.20
- [ ] Deposit / withdraw / transfer / over-withdraw tested
- [ ] `04_BankWithFallback.sol` compiles
- [ ] `receive` triggered by plain ETH
- [ ] `fallback` triggered by `0xdeadbeef`
- [ ] `lastFallbackSelector()` returns `0xdeadbeef`
- [ ] Survey report filled with your name/roll number

## Safety

- Use a **dedicated test wallet** for labs; never reuse a wallet that holds
  real funds.
- Test ETH is worthless — do not buy ETH for this practical.
- Never share your seed phrase or private key, including in screenshots and
  lab reports.
- Always confirm the **network** in MetaMask before signing — a mainnet
  transaction costs real money.

## Viva questions

1. What is the difference between `receive()` and `fallback()`?
2. Why is `msg.sender` preferred over `tx.origin`?
3. What is re-entrancy, and how does checks-effects-interactions prevent it?
4. Why are events used instead of storing an array of transaction history?
5. What happens if a contract has a payable fallback but no `receive`?
6. How does a smart contract differ from a normal bank database record?
7. Why use a testnet instead of mainnet for development?
8. What is gas, and why does storage cost more than computation?
