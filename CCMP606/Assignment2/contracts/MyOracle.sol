// CCMP 606 Assignment 2
// MyOracle contract for getting the price of Ether in USD

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.1;

contract MyOracle {
    
    // Define the state variables
    uint public ethUSDPrice;
    address public owner;

    // Define the events
    event UpdatePrice(uint ethPrice);

    // Define the constructor if you wish
    constructor() {
        owner = msg.sender;
    }

    // Define the set function to set the ETH price in USD
    function setETHinUSD(uint _ethUSDPrice) external {
        require(msg.sender == owner, "Only the owner can update the price");
        ethUSDPrice = _ethUSDPrice;
        emit UpdatePrice(_ethUSDPrice);
    }

    // Define the get function to get the ETH price in USD
    function getETHinUSD() external view returns (uint) {
        return ethUSDPrice;
    }

    // Define the request update function to request a price update
    function requestPriceUpdate() external {
        emit UpdatePrice(ethUSDPrice);
    }

}
