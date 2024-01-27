// CCMP 606 Assignment 1
// Piggy Bank Smart Contract
// Author: Tai Cong Chi Nguyen

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

// My contract address:  0xAD45EF90803D39a67059c1BAf512cfd672B43485

contract PiggyBank {

    address public immutable owner;
    uint public savingsGoal;
    mapping(address=>uint) public deposits;
    
    // Set any other variables you need


    // Set up so that the owner is the person who deployed the contract.
    // Set a savings goal 
    constructor(uint _savingsGoal) {
        owner = msg.sender;
        savingsGoal = _savingsGoal;
    }
    
    // Create an event to emit once you reach the savings goal
    event SavingsGoalReached(address indexed depositor, uint amount);

    // create modifier onlyOwner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }


    // Function to receive ETH, called depositToTheBank
    // -- Function should log who sent the ETH 
    // -- Function should check balance to know if you've reached savings goal and emit the event if you have. 
    receive() external payable {
        depositToTheBank();
    }

    function depositToTheBank() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");
        
        // Log who sent the ETH
        deposits[msg.sender] += msg.value;

        // Check if savings goal is reached and emit the event
        if (address(this).balance >= savingsGoal) {
            emit SavingsGoalReached(msg.sender, address(this).balance);
        }
    }


    // Function to return the balance of the contract, called getBalance
    // -- Note: you will need to use address(this).balance which returns the balance in Wei.
    // -- 1 Eth = 1 * 10**18 Wei
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }

    // Function to look up how much any depositor has deposited, called getDepositsValue
    function getDepositsValue(address depositor) public view returns (uint) {
        return deposits[depositor];
    }


    // Function to withdraw (send) ETH, called emptyTheBank
    // -- Only the owner of the contract can withdraw the ETH from the contract
   function emptyTheBank() public onlyOwner {
        payable(owner).transfer(address(this).balance);
    }



}
