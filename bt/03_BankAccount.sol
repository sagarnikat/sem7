// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * QUESTION 3 (BT): Smart contract for a bank account.
 *
 * HOW IT WORKS
 *   Each address that calls deposit() gets its own balance in the
 *   `balances` mapping. Deposits are payable: the ETH sent with the
 *   transaction is credited to msg.sender. withdraw() checks the caller's
 *   balance, updates state BEFORE sending ETH (checks-effects-interactions
 *   pattern, so re-entrancy cannot drain the contract), then transfers the
 *   money with a low-level call and verifies it succeeded. The owner can
 *   hand over the contract with transferOwnership().
 *
 * COMPLEXITY / COST
 *   deposit        : O(1) time, ~45k gas (one fresh storage slot)
 *   withdraw       : O(1) time, ~30k gas + 2300 gas stipend for the receiver
 *   balanceOf      : O(1), free when called with eth_call (view function)
 *
 * NOTES / INFO
 *   - Never use tx.origin for authorisation; use msg.sender.
 *   - Update balances before the external call to prevent re-entrancy.
 *   - This is a teaching contract: it holds real ETH on a testnet only.
 *     A production bank would additionally use access control roles,
 *     upgradeable proxies, interest accounting and off-chain KYC.
 */
contract BankAccount {
    // ---------- State ----------
    address public owner;
    mapping(address => uint256) private balances;
    uint256 public totalDeposits;

    // ---------- Events ----------
    event Deposited(address indexed account, uint256 amount, uint256 newBalance);
    event Withdrawn(address indexed account, uint256 amount, uint256 newBalance);
    event Transferred(address indexed from, address indexed to, uint256 amount);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    // ---------- Errors (cheaper than require strings) ----------
    error NotOwner();
    error ZeroAmount();
    error InsufficientBalance(uint256 requested, uint256 available);
    error InvalidRecipient();
    error TransferFailed();

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    /// The deployer becomes the bank owner.
    constructor() {
        owner = msg.sender;
    }

    /// Deposit ETH into the caller's bank account.
    function deposit() external payable {
        if (msg.value == 0) revert ZeroAmount();

        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;

        emit Deposited(msg.sender, msg.value, balances[msg.sender]);
    }

    /// Withdraw `amount` wei from the caller's own account.
    function withdraw(uint256 amount) external {
        if (amount == 0) revert ZeroAmount();

        uint256 current = balances[msg.sender];
        if (amount > current) revert InsufficientBalance(amount, current);

        // Effects before interaction: the balance is already reduced, so a
        // malicious receiver re-entering withdraw() sees the new balance.
        balances[msg.sender] = current - amount;
        totalDeposits -= amount;

        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        if (!ok) revert TransferFailed();

        emit Withdrawn(msg.sender, amount, balances[msg.sender]);
    }

    /// Move funds from the caller's account to another customer.
    function transferTo(address payable recipient, uint256 amount) external {
        if (recipient == address(0)) revert InvalidRecipient();
        if (amount == 0) revert ZeroAmount();

        uint256 current = balances[msg.sender];
        if (amount > current) revert InsufficientBalance(amount, current);

        balances[msg.sender] = current - amount;
        balances[recipient] += amount;

        emit Transferred(msg.sender, recipient, amount);
    }

    /// Balance of one customer (in wei).
    function balanceOf(address account) external view returns (uint256) {
        return balances[account];
    }

    /// ETH actually held by the contract (should equal sum of all balances).
    function contractBalance() external view returns (uint256) {
        return address(this).balance;
    }

    /// Owner-only: transfer control of the bank to a new address.
    function transferOwnership(address newOwner) external onlyOwner {
        if (newOwner == address(0)) revert InvalidRecipient();

        address previous = owner;
        owner = newOwner;

        emit OwnershipTransferred(previous, newOwner);
    }
}
