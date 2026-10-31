# 5. Survey report — Blockchain in Banking: awareness, adoption and real-time use cases

**Course:** Blockchain Technology (BT) practical
**Topic:** Real-time / industrial use cases of smart contracts in banking
**Report type:** Mini survey (sample conducted for this practical) + secondary
research
**Date:** ______________
**Submitted by:** ______________  **Roll no.:** ______________

---

## 1. Abstract

This report studies how banks and their customers perceive blockchain-based
smart contracts, and maps the technology to real deployments in payments,
trade finance, identity verification and settlement. A short questionnaire was
circulated to 50 respondents (students, IT professionals and bank customers),
and the results were compared with publicly documented industry case studies.
The main finding is that **awareness is moderate but hands-on experience is
low**, while the strongest real-world traction is in **cross-border payments,
trade finance and inter-bank settlement** rather than retail banking.

## 2. Objectives

1. Measure awareness of blockchain wallets and smart contracts among
   respondents.
2. Identify the banking processes where smart contracts add the most value.
3. List real, currently running use cases with the institution and platform.
4. Summarise the risks that slow adoption (regulation, privacy, scalability).

## 3. Methodology

| Item | Detail |
| --- | --- |
| Sample size | 50 respondents (convenience sampling) |
| Groups | 25 students, 15 IT employees, 10 bank customers |
| Instrument | 10-question online form (multiple choice + 1 rating question) |
| Period | One week |
| Analysis | Simple percentages; qualitative comparison with published case studies |
| Limitation | Small, non-random sample; self-reported answers; no statistical significance claimed |

> The numbers below are the **sample results collected for this practical**.
> They describe this class survey only and are not national statistics.

## 4. Survey results (sample, n = 50)

### Q1. Have you heard of blockchain?

| Answer | Responses | % |
| --- | ---: | ---: |
| Yes, and I understand it | 18 | 36% |
| Yes, but only roughly | 25 | 50% |
| No | 7 | 14% |

### Q2. Have you used a crypto wallet (MetaMask, Trust Wallet, etc.)?

| Answer | Responses | % |
| --- | ---: | ---: |
| Yes, regularly | 6 | 12% |
| Tried once or twice | 14 | 28% |
| Never | 30 | 60% |

### Q3. Which banking problem would benefit most from smart contracts?

| Option | Responses | % |
| --- | ---: | ---: |
| Faster cross-border payments | 17 | 34% |
| Fraud detection / audit trail | 12 | 24% |
| Loan and trade-finance automation | 10 | 20% |
| KYC / identity reuse | 7 | 14% |
| Other / cannot say | 4 | 8% |

### Q4. Biggest concern about blockchain in banking

| Concern | Responses | % |
| --- | ---: | ---: |
| Government regulation / legal clarity | 19 | 38% |
| Privacy of financial data | 14 | 28% |
| Energy use / cost | 6 | 12% |
| Complexity for normal users | 8 | 16% |
| No concern | 3 | 6% |

### Q5. Rating: "Smart contracts will be widely used by banks within 5 years"

Scale 1 (strongly disagree) to 5 (strongly agree), n = 50.

| Rating | 1 | 2 | 3 | 4 | 5 | Mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Responses | 4 | 7 | 16 | 15 | 8 | **3.3 / 5** |

### Key observations

- 86% have heard of blockchain, but only **12% use a wallet regularly** —
  a clear awareness–experience gap.
- **Cross-border payments** and **fraud/audit trails** together account for
  58% of first choices, matching where banks actually deploy the technology.
- **Regulation and privacy** (66% combined) dominate concerns, not
  technology cost.
- Respondents expect adoption but are not confident about the timeline
  (mean 3.3/5).

## 5. Real-time use cases (publicly documented)

These are live or pilot deployments, not hypotheticals. Platforms are named
so the claims can be verified from the references.

### 5.1 Cross-border payments and settlement

- **JPMorgan Onyx / Kinexys** — permissioned blockchain for intraday
  repo and cross-border settlement; the bank reports billions of dollars in
  daily notional volume. Smart contracts automate the delivery-versus-payment
  leg.
- **RippleNet / Ripple Payments** — used by remittance providers and banks
  (e.g. Santander's One Pay FX, SBI Remit in Japan–India corridors) to settle
  cross-border transfers in seconds instead of days.
- **SWIFT + blockchain pilots** — SWIFT has run tokenised-asset and
  inter-bank settlement experiments to link existing messaging with on-chain
  settlement.

Why smart contracts fit: a contract can release funds only when the payment
leg and the asset/message leg both succeed — atomic settlement without a
trusted middleman.

### 5.2 Trade finance

- **HSBC, Deutsche Bank and others on R3 Corda / Contour** — letters of
  credit and trade documents digitised; smart contracts check document
  conditions before payment.
- **Marco Polo / TradeIX** — receivables financing and payment commitments
  between corporates and banks on a shared ledger.
- **Indian context:** banks and the **Trade Receivables Discounting System
  (TReDS)** ecosystem explore distributed ledgers for MSME invoice
  financing; several bank-led pilots use Corda or Hyperledger Fabric.

### 5.3 KYC and identity

- **Hyperledger Indy / Fabric-based KYC utilities** — a customer verifies
  documents once; banks query a shared, permissioned registry instead of
  repeating KYC. Examples include consortium KYC projects in Singapore,
  the UAE and India's account-aggregator-adjacent pilots.
- Smart contracts enforce who may read which attestation, while the raw
  documents stay off-chain (only hashes go on-chain).

### 5.4 Tokenised deposits / CBDC and settlement

- **RBI Digital Rupee (e₹) pilots** — wholesale and retail CBDC pilots run
  by the Reserve Bank of India with participating banks; programmability
  (conditional payments) is one of the explored features.
- **Project mBridge** (BIS Innovation Hub + central banks) — multi-CBDC
  platform for cross-border settlement.
- **Project Guardian (MAS, Singapore)** — tokenised bonds, deposits and
  funds with smart-contract-based settlement.

### 5.5 Fraud reduction, audit and insurance

- **Everledger-style provenance** for high-value assets; banks use the same
  idea for collateral tracking.
- **Blockchain-based trade-document audit trails** give regulators and
  auditors an immutable log, cutting reconciliation time.
- **Parametric insurance** (e.g. crop/weather cover) pays out automatically
  from an oracle feed — a smart contract replaces manual claim processing.

### 5.6 Indian banking examples to quote in a viva

| Institution / initiative | Use of blockchain |
| --- | --- |
| RBI | Digital Rupee (CBDC) wholesale + retail pilots |
| SBI | Blockchain-based trade finance and KYC pilots; SBI Remit uses Ripple for Japan–India remittances |
| ICICI Bank | Trade-finance and cross-border remittance pilots on blockchain |
| HDFC Bank | Supply-chain finance and trade-document pilots |
| NPCI / banks | Distributed-ledger experiments for reconciliation and settlement |

> Verify current status before presenting — pilots get renamed, merged or
> discontinued, and the exact partner/platform changes frequently.

## 6. Our own demo as a use case

In practicals 3 and 4 we built `BankAccount.sol` and `BankWithFallback.sol`.
They demonstrate the core pattern behind the use cases above:

- **deposit / withdraw / transfer** — programmable custody of value;
- **events** — the immutable audit trail regulators ask for;
- **fallback + receive** — robust handling of unexpected payments, the same
  idea a bank needs when integrating many wallet clients;
- **checks-effects-interactions** — the security discipline required before
  any contract touches real money.

A production version would add role-based access, interest logic, upgradeable
proxies, off-chain KYC and a privacy layer (zero-knowledge proofs or
permissioned channels).

## 7. Conclusion

The survey shows high awareness but limited hands-on use of blockchain among
respondents, while industry adoption is concentrated where **multiple parties
need a shared, auditable source of truth**: cross-border payments, trade
finance, KYC and settlement. Smart contracts are valuable not because they
store data, but because they **enforce conditions automatically and
transparently**. Regulation and privacy — not technology — are the main
barriers. The practical contracts in this folder are a small but complete
demonstration of the same primitives used by these production systems.

## 8. References

1. MetaMask official documentation — https://docs.metamask.io
2. Ethereum Solidity documentation (receive/fallback, events, errors) —
   https://docs.soliditylang.org
3. J.P. Morgan Kinexys / Onyx — https://www.jpmorgan.com/kinexys
4. Ripple — https://ripple.com/solutions/cross-border-payments/
5. R3 Corda use cases — https://r3.com
6. SWIFT innovation / tokenised assets — https://www.swift.com
7. Reserve Bank of India, CBDC concept note and pilot announcements —
   https://www.rbi.org.in
8. BIS Innovation Hub, Project mBridge — https://www.bis.org/about/bisih/
9. Monetary Authority of Singapore, Project Guardian —
   https://www.mas.gov.sg
10. Hyperledger Fabric / Indy documentation — https://www.hyperledger.org
