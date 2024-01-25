const Lottery = artifacts.require('./Lottery');
module.exports = function (_deployer) {
  // Use deployer to state migration tasks.
  _deployer.deploy(Lottery);
};
