# 2. Creating your own wallet with MetaMask

A wallet is a **public address** (safe to share, like an account number) plus a
**private key / Secret Recovery Phrase** (never share, like a password + OTP).
MetaMask derives many accounts from one 12-word phrase.

---

## Step-by-step: create a new wallet

1. Open MetaMask → **Get started**.
2. Choose **Create a new wallet** (not "Import").
3. Create a **password** (minimum 8 characters). This encrypts the wallet on
   this device only. It is *not* the recovery phrase.
4. Read the security tips → **Secure my wallet**.
5. MetaMask shows **12 words** — your **Secret Recovery Phrase**.
   - Write them **in order** on paper.
   - Store the paper somewhere safe and offline.
   - Click **Confirm** only after writing them down.
6. Re-enter the words in the correct order to verify.
7. **Done.** MetaMask opens your first account, e.g. `Account 1`.

## Understanding what you see

| Item | Meaning |
| --- | --- |
| `0x8f3A...c21B` | Public address — share freely to receive funds |
| Network selector ("Ethereum Mainnet") | Which chain you are using |
| Balance | ETH on the **selected network only** |
| Activity tab | Your transaction history |
| Three-dot menu → Account details | Reveal address, export private key (avoid) |

## Switch to the Sepolia testnet

1. Click the network dropdown at the top-left of MetaMask.
2. Enable **Show test networks** if Sepolia is hidden
   (Settings → Advanced → *Show test networks*).
3. Select **Sepolia**.
4. Copy your address and get free test ETH from a faucet:
   - https://cloud.google.com/application/web3/faucet/ethereum/sepolia
   - https://sepoliafaucet.com
5. Wait ~1 minute, then refresh MetaMask. You should see test ETH.

> Test ETH has **no real value** and cannot be converted to real money.
> That is exactly why we use it in the lab.

## Back up and restore

- **Backup:** Settings → Security & privacy → **Reveal Secret Recovery
  Phrase** (requires password). Copy it to paper; never to a file.
- **Restore:** On a new device choose **Import an existing wallet** → enter
  the 12 words → set a new local password. All accounts and funds reappear.
- **Add another account:** profile icon → **Add account**. Each account has a
  different address but the same recovery phrase.

## Useful test actions

- **Send test ETH to a classmate:** click **Send** → paste their `0x...`
  address → enter a small amount (e.g. `0.01`) → **Confirm**.
- **View the transaction:** click it in the Activity tab → **View on
  Etherscan** (Sepolia explorer) to see block, gas fee and status.

## Common mistakes

| Mistake | Consequence |
| --- | --- |
| Screenshotting the seed phrase | Malware/cloud backup can steal it |
| Sharing the private key "for testing" | Funds gone instantly |
| Sending to the wrong network | Funds may be unreachable without a bridge |
| Losing the seed phrase + device | Wallet is **unrecoverable**, no support line exists |
| Using a mainnet wallet in the lab | Real money at risk — always create a fresh test wallet |

## Verify your wallet works

- [ ] Address starts with `0x` and has 40 hex characters
- [ ] Network is **Sepolia**
- [ ] Balance shows test ETH
- [ ] A test transaction appears in the Activity tab

Next: [03_BankAccount.sol](03_BankAccount.sol)
