// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * QUESTION 4 (BT): Smart contract with a fallback (and receive) function.
 *
 * HOW IT WORKS
 *   Solidity gives a contract two special entry points for calls that do
 *   not match any declared function:
 *
 *   receive()  external payable
 *       Runs when ETH is sent with EMPTY calldata (a plain wallet transfer).
 *
 *   fallback() external payable
 *       Runs for everything else: an unknown function selector, or ETH sent
 *       together with calldata that matches no function.
 *
 *   This contract behaves like a bank that ACCEPTS any stray payment:
 *   the sender is credited, the call is logged in an event, and the raw
 *   calldata is stored so the owner can inspect what was sent. A dispatch
 *   helper decodes the first 4 bytes (the selector) for reporting.
 *
 * COMPLEXITY / COST
 *   receive  : O(1), ~25k gas for the first deposit (one new balance slot)
 *   fallback : O(1) for the balance update + O(k) to store k bytes of
 *              calldata, where k = msg.data.length
 *
 * NOTES / INFO
 *   - If `receive()` is absent, plain ETH transfers fall through to
 *     `fallback()`. If `fallback()` is non-payable, plain ETH is rejected.
 *   - A fallback that writes to storage is not free: unknown calls cost
 *     gas and can be spammed, so production contracts often keep it
 *     minimal (e.g. just emit an event) or delegate to a proxy.
 *   - Never put business logic that can revert in a fallback unless you
 *     intend to reject unknown calls: reverting there makes the whole
 *     transaction fail.
 */
contract BankWithFallback {
    // ---------- State ----------
    address public owner;
    mapping(address => uint256) public balances;
    uint256 public totalReceived;

    /// Raw calldata of the most recent fallback call, for debugging.
    bytes public lastFallbackData;
    address public lastFallbackSender;

    // ---------- Events ----------
    event Received(address indexed sender, uint256 amount, uint256 newBalance);
    event FallbackTriggered(address indexed sender, uint256 amount, bytes data);
    event Withdrawn(address indexed account, uint256 amount);

    error InsufficientBalance(uint256 requested, uint256 available);
    error TransferFailed();

    constructor() payable {
        owner = msg.sender;
        if (msg.value > 0) {
            balances[msg.sender] = msg.value;
            totalReceived = msg.value;
            emit Received(msg.sender, msg.value, msg.value);
        }
    }

    /// Plain ETH transfer: no calldata at all.
    receive() external payable {
        balances[msg.sender] += msg.value;
        totalReceived += msg.value;

        emit Received(msg.sender, msg.value, balances[msg.sender]);
    }

    /// Unknown function selector, or ETH sent with non-empty calldata.
    /// Accepts the money instead of reverting, and records the call.
    fallback() external payable {
        balances[msg.sender] += msg.value;
        totalReceived += msg.value;

        lastFallbackData = msg.data;
        lastFallbackSender = msg.sender;

        emit FallbackTriggered(msg.sender, msg.value, msg.data);
    }

    /// Customer withdraws from their own balance.
    function withdraw(uint256 amount) external {
        uint256 current = balances[msg.sender];
        if (amount > current) revert InsufficientBalance(amount, current);

        balances[msg.sender] = current - amount;

        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        if (!ok) revert TransferFailed();

        emit Withdrawn(msg.sender, amount);
    }

    /// First 4 bytes of the last fallback calldata = the unknown selector.
    /// Returns 0x00000000 when the calldata was shorter than 4 bytes.
    function lastFallbackSelector() external view returns (bytes4 selector) {
        bytes memory data = lastFallbackData; // copy storage → memory
        if (data.length < 4) return bytes4(0);
        assembly {
            selector := mload(add(data, 32))
        }
    }
}
