# 1. Installing MetaMask

MetaMask is a browser extension / mobile app that acts as a **crypto wallet**
and a **gateway to the blockchain**. It stores your private keys locally,
signs transactions, and injects a `window.ethereum` provider into web pages
so dApps (like Remix) can talk to the blockchain.

> You do **not** need to buy crypto to do these practicals. Everything can be
> done on a free testnet (Sepolia) using test ETH from a faucet.

---

## Option A — Browser extension (recommended for the practical)

1. Open **Chrome**, **Brave**, **Edge** or **Firefox**.
2. Go to the official site: **https://metamask.io/download/**
   *(always type the URL yourself — fake MetaMask sites are a common scam).*
3. Click **Download** → choose your browser → **Install MetaMask**.
4. When the browser asks *"Add extension?"*, click **Add extension**.
5. Pin MetaMask: click the puzzle-piece icon in the toolbar → pin 📌 next to
   MetaMask.
6. Click the fox icon → **Get started**.

## Option B — Mobile app

1. Install **MetaMask** from the **Google Play Store** or **Apple App Store**
   (check the publisher is *MetaMask / ConsenSys*).
2. Open the app → **Create a new wallet** (or **Import an existing wallet**).

## Option C — Install from source (developers)

```bash
git clone https://github.com/MetaMask/metamask-extension.git
cd metamask-extension
yarn install
yarn start
```

This loads an unpacked extension into a development browser profile. Version
numbers and build instructions change often, so follow the repo README.

---

## First-run checklist

- [ ] MetaMask icon is visible and pinned
- [ ] You are on the **"Welcome"** screen (do not close the tab yet)
- [ ] You have read the security notes below

## Security rules (read before creating a wallet)

1. **The Secret Recovery Phrase (SRP) is the wallet.** Anyone who has those
   12 words owns all your funds. Never type it into a website, chat, Google
   Form, or screenshot. MetaMask support will **never** ask for it.
2. Write the phrase on **paper**, store it offline. Do not keep it in
   Notepad, WhatsApp, email, or cloud notes.
3. Use a **separate wallet** for college practicals. Never put mainnet funds
   in a wallet whose seed phrase has been typed on a lab PC.
4. Install only from the official store/URL. Check the extension ID and
   reviews; fake "MetaMask" extensions steal funds.
5. Turn on **Settings → Security & privacy → Basic attack protection** and a
   **wallet password** (the password only unlocks this device, it is not the
   seed phrase).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Fox icon missing | Browser menu → Extensions → enable MetaMask |
| "MetaMask is not detected" in Remix | Refresh the page; make sure the extension is enabled for that site |
| Wrong network shown | Click the network selector at the top of MetaMask → choose **Sepolia** |
| Extension stuck loading | Disable/re-enable it, or reinstall (you will need your seed phrase to restore) |

Next: [02_CreateWallet.md](02_CreateWallet.md)
