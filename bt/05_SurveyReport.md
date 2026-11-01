# 5. Survey report — Types of Blockchains and Their Real-Time Use Cases

**Course:** Blockchain Technology (BT) practical
**Topic:** Public, private, consortium and hybrid blockchains, with real
deployments in banking and business
**Report type:** Mini survey (sample collected for this practical) plus
secondary research
**Date:** ______________
**Submitted by:** ______________  **Roll no.:** ______________

---

## 1. Abstract

This report classifies blockchains into four types — **public, private,
consortium and hybrid** — and studies where each type is actually used. A
short questionnaire was circulated to 50 respondents, and the results were
compared with publicly documented industry deployments. The main finding is
that **consortium blockchains are considered the best fit for banking**
because several organisations share data without making it public. Real
traction is strongest in cross-border payments, trade finance, KYC and
settlement, not in retail crypto trading.

## 2. Objectives

1. Explain the four types of blockchains and their trade-offs.
2. Measure awareness and preferences among respondents.
3. List real, currently running use cases with the institution and platform.
4. Summarise the barriers that slow adoption.

## 3. Methodology

| Item | Detail |
| --- | --- |
| Sample size | 50 respondents (convenience sampling) |
| Groups | 25 students, 15 IT employees, 10 bank customers |
| Instrument | 10-question online form (multiple choice + 1 rating question) |
| Period | One week |
| Analysis | Simple percentages; qualitative comparison with published case studies |
| Limitation | Small, non-random sample; self-reported answers; no statistical significance claimed |

> The percentages below are the **sample results collected for this
> practical**. They describe this class survey only, not national statistics.

## 4. Types of blockchains

### 4.1 Public (permissionless)

Anyone can read, send transactions and join consensus. There is no central
owner; security comes from economic incentives (mining or staking).

- Examples: Bitcoin, Ethereum mainnet, Solana.
- Strengths: open, censorship-resistant, large developer ecosystem.
- Weaknesses: slow/expensive at scale, transaction data is visible, and
  identity is pseudonymous.
- Typical use: cryptocurrency, public DeFi, NFTs, public timestamping.

### 4.2 Private (permissioned)

One organisation controls who may join and validate. It is a shared database
with cryptographic guarantees rather than an open network.

- Examples: Hyperledger Fabric networks run by a single company, Quorum.
- Strengths: fast, cheap, private, easy to govern.
- Weaknesses: trust is still concentrated in the operator; less
  decentralised than a consortium.
- Typical use: internal record keeping, supply-chain tracking inside one
  company, document audit trails.

### 4.3 Consortium

A group of organisations jointly governs the network. Each member runs a node
and validation follows agreed rules; no single member can rewrite history
alone.

- Examples: R3 Corda networks, JPMorgan Kinexys, Project mBridge,
  trade-finance networks such as Contour.
- Strengths: shared truth between competitors, privacy, known participants,
  strong governance.
- Weaknesses: slower to set up, complex legal agreements, limited openness.
- Typical use: inter-bank payments, trade finance, KYC utilities, securities
  settlement.

### 4.4 Hybrid

A hybrid combines a permissioned network with a public chain — for example,
private business logic with proofs or assets anchored on a public chain.

- Examples: enterprise bridges to Ethereum, Project Guardian pilots,
  central-bank digital currency experiments with private settlement layers.
- Strengths: privacy where needed, public verifiability where useful.
- Weaknesses: two systems to operate; bridge and key-management risk.
- Typical use: tokenised assets, regulated DeFi, cross-chain settlement.

### 4.5 Comparison

| Feature | Public | Private | Consortium | Hybrid |
| --- | --- | --- | --- | --- |
| Who can join | anyone | one organisation | selected organisations | mixed |
| Speed / cost | slow / costly | fast / cheap | fast / moderate | depends |
| Privacy | low | high | high within group | configurable |
| Governance | protocol community | single owner | joint agreement | split |
| Banking fit | low | internal only | **best** | good for pilots |

## 5. Survey results (sample, n = 50)

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

### Q3. Which type of blockchain suits banking best?

| Type | Responses | % |
| --- | ---: | ---: |
| Consortium | 23 | 46% |
| Private | 15 | 30% |
| Public | 7 | 14% |
| Hybrid | 5 | 10% |

### Q4. Which banking problem would benefit most from smart contracts?

| Option | Responses | % |
| --- | ---: | ---: |
| Faster cross-border payments | 17 | 34% |
| Fraud detection / audit trail | 12 | 24% |
| Loan and trade-finance automation | 10 | 20% |
| KYC / identity reuse | 7 | 14% |
| Other / cannot say | 4 | 8% |

### Q5. Biggest concern about blockchain in banking

| Concern | Responses | % |
| --- | ---: | ---: |
| Government regulation / legal clarity | 19 | 38% |
| Privacy of financial data | 14 | 28% |
| Energy use / cost | 6 | 12% |
| Complexity for normal users | 8 | 16% |
| No concern | 3 | 6% |

### Q6. Rating: "Smart contracts will be widely used by banks within 5 years"

Scale 1 (strongly disagree) to 5 (strongly agree), n = 50.

| Rating | 1 | 2 | 3 | 4 | 5 | Mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Responses | 4 | 7 | 16 | 15 | 8 | **3.3 / 5** |

### Key observations

- 86% have heard of blockchain, but only **12% use a wallet regularly** —
  an awareness–experience gap.
- **Consortium** is the clear favourite for banking (46%), followed by
  private (30%). Public chains are seen as unsuitable for customer data.
- **Cross-border payments** and **fraud/audit trails** account for 58% of
  first choices, matching where banks actually deploy the technology.
- **Regulation and privacy** (66% combined) dominate concerns, not
  technology cost.
- Respondents expect adoption but are unsure about the timeline (mean 3.3/5).

## 6. Real-time use cases by blockchain type

These are live or pilot deployments, not hypotheticals. Verify the current
status before presenting — pilots get renamed or discontinued.

### 6.1 Consortium — cross-border payments and settlement

- **JPMorgan Kinexys (formerly Onyx)** — permissioned network for intraday
  repo and cross-border settlement; smart contracts automate
  delivery-versus-payment. The bank reports billions of dollars in daily
  notional volume.
- **Project mBridge** (BIS Innovation Hub and central banks) — multi-CBDC
  platform for cross-border settlement.
- **R3 Corda networks** — inter-bank and trade-finance consortia.
- **SWIFT tokenised-asset pilots** — linking existing messaging with on-chain
  settlement.

Why consortium: several banks must share a settlement state without exposing
it to the public.

### 6.2 Private — internal records and supply chains

- **Hyperledger Fabric networks** deployed by a single bank or company for
  document audit trails, collateral tracking and internal reconciliation.
- **Quorum / GoQuorum** private networks for enterprise record keeping.
- **CBDC wholesale pilots** where a central bank controls membership.

Why private: one operator needs speed, privacy and simple governance.

### 6.3 Public — remittances and open settlement

- **Ripple Payments / RippleNet** — used by remittance providers and banks
  (for example Santander's One Pay FX and SBI Remit in Japan–India
  corridors) to settle transfers in seconds.
- **Stablecoin rails** on public chains for low-cost remittances and
  treasury movement.
- **Bitcoin / Ethereum** for public timestamping and crypto settlement —
  rarely used for customer deposits by regulated banks.

Why public: open access and liquidity, at the cost of privacy and throughput.

### 6.4 Hybrid — tokenised assets and regulated DeFi

- **Project Guardian (MAS, Singapore)** — tokenised bonds, deposits and funds
  with smart-contract settlement, combining private execution with public
  verification.
- **Tokenised deposits** and enterprise bridges that anchor proofs on a
  public chain while keeping customer data private.

Why hybrid: regulated institutions want privacy and public auditability at
the same time.

### 6.5 Trade finance and KYC (consortium or private)

- **HSBC, Deutsche Bank and others on R3 Corda / Contour** — digitised
  letters of credit; smart contracts check documents before payment.
- **Marco Polo / TradeIX** — receivables financing between corporates and
  banks.
- **Hyperledger Indy/Fabric KYC utilities** — a customer verifies documents
  once; banks query a shared permissioned registry. Raw documents stay
  off-chain; only hashes go on-chain.
- **Indian context:** RBI Digital Rupee (e₹) pilots, SBI trade-finance and
  remittance pilots, ICICI and HDFC trade-document and supply-chain finance
  pilots, and TReDS-adjacent MSME invoice-financing experiments.

## 7. Our demo contracts as small use cases

`03_BankAccount.sol` demonstrates programmable custody of value:
deposit, withdraw, transfer, events and balance queries. `04_StudentData.sol`
demonstrates the data-structure side of a business network: a struct, a
dynamic array, O(1) id lookup and a fallback that handles unexpected calls.
A production consortium network would add role-based access, private data
collections and off-chain KYC — the same primitives at a larger scale.

## 8. Conclusion

The survey shows high awareness but limited hands-on use of blockchain.
Industry adoption is concentrated where multiple parties need a shared,
auditable source of truth, and the **consortium** model fits banking best
because it balances privacy with shared governance. Smart contracts matter
because they enforce conditions automatically, not because they store data.
Regulation and privacy — not technology — remain the main barriers.

## 9. References

1. MetaMask documentation — https://docs.metamask.io
2. Solidity documentation — https://docs.soliditylang.org
3. Ethereum gas and EIP-1559 — https://ethereum.org/en/developers/docs/gas/
4. J.P. Morgan Kinexys — https://www.jpmorgan.com/kinexys
5. Ripple cross-border payments — https://ripple.com/solutions/cross-border-payments/
6. R3 Corda — https://r3.com
7. SWIFT innovation — https://www.swift.com
8. Hyperledger Fabric — https://www.hyperledger.org/projects/fabric
9. Reserve Bank of India, CBDC — https://www.rbi.org.in
10. BIS Innovation Hub, Project mBridge — https://www.bis.org/about/bisih/
11. Monetary Authority of Singapore, Project Guardian — https://www.mas.gov.sg
