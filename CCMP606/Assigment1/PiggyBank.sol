// CCMP 606 Assignment 1
// Piggy Bank Smart Contract
// Author: <<Update me>>

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

// My contract address:  <<Update me>>

contract PiggyBank {

    address public immutable owner;
    uint public savingsGoal;
    mapping(address=>uint) public deposits;
    
    // Set any other variables you need


    // Set up so that the owner is the person who deployed the contract.
    // Set a savings goal 
    constructor() {
        owner = msg.sender;

    }
    
    // Create an event to emit once you reach the savings goal 


    // create modifier onlyOwner
    modifier onlyOwner() {

    }


    // Function to receive ETH, called depositToTheBank
    // -- Function should log who sent the ETH 
    // -- Function should check balance to know if you've reached savings goal and emit the event if you have. 



    // Function to return the balance of the contract, called getBalance
    // -- Note: you will need to use address(this).balance which returns the balance in Wei.
    // -- 1 Eth = 1 * 10**18 Wei


    // Function to look up how much any depositor has deposited, called getDepositsValue



    // Function to withdraw (send) ETH, called emptyTheBank
    // -- Only the owner of the contract can withdraw the ETH from the contract
   



}
