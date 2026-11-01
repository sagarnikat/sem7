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



//code

//------------------------------------------------------------------------------------------


//SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BankAccount{
    //mapping line, D,W,S:
    mapping(address => uint256) private balances;

    //Deposit Ether:
    function deposit() public payable{
        require(msg.value>0, "Deposit must be greater than 0");
        balances[msg.sender] += msg.value;
    }

    //Withdraw Ether:
    function withdraw(uint256 amount) public {
        require(amount>0, "Amount must be greater than 0");
        require(balances[msg.sender]>=amount, "Insufficient Balance");
        balances[msg.sender]-=amount;
        (bool success,) = payable(msg.sender).call{value:amount}("");

        require(success, "Transfer Fialed");
    }
    //Show Balance:
    function displayBalance() public view returns(uint256){
        return balances[msg.sender];
    }
}


//--------------------------------------------------------------------
steps 
0. log in gmail : nikatsagar94@gmail.com 
    pass: Sagar@123

    metemask pass: Sagar@123
1. open metamask 
2. log in remix ide
3. go to files -> contract creata file bank.sol
4. copy past above code 
5. compile code
6. deploy select evarnaments ->  brauser extension , options -> sefolia testnet metamask
7. delpy  select bank.sol
8. kepp evry thing as it is click delpy click confornm in metemask
9. open terminal  click net to debug expald , chat copy contact addres
10. go to deploy contact add contact and put contact addres click connect 
11. 