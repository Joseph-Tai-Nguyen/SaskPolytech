### 1st terminal window
brew install ethereum
// to install ethereum
mkdir Ethereum-Private-Network
// to create project folder
mkdir node1
// to create folder node 1
mkdir node2
// to create folder node 2
geth --datadir node1 account new
// to create the account for Node 1 to receive some ether at launch
geth --datadir node2 account new
// to create the account for Node 2 to receive some ether at launch
geth init --datadir node1 genesis.json
// to import and sets the genesis block for the new chain in node1
geth init --datadir node2 genesis.json
// to import and sets the genesis block for the new chain in node2
bootnode -genkey boot.key
// to generate a key for the bootnode to run later
bootnode -nodekey boot.key -addr :30305 --verbosity 9
// to run the bootnode on port 30305 and display with --verbosity flag

### Open a new terminal window at the same directory - 2nd terminal window
geth --datadir node1 --port 30306 --bootnodes "enode://ffa207f30f51b9ceddb82d7677009657b55cc47c21619f684e0aaa885a4b5345d7a4939f87be1f2e069cb8a6996dbcae6e7cfbb5ff25d6859dd692c27d5b59af@127.0.0.1:0?discport=30305" --networkid 12345 --unlock 0x05255103599F710AdB8A14603AD4c9e2c0B6316A --password node1/password.txt --authrpc.port 8551 --mine --miner.etherbase 0x05255103599F710AdB8A14603AD4c9e2c0B6316A
// to start the node 1 on port 30306 with bootnodes run on the first terminal, run on networkid 12345 which defined in genesis.json file
// unlock the account with the password inside file node1/password.txt
// use rpc port 8551 and consider at the miner

### Open a new terminal window at the same directory - 3rd terminal window
geth --datadir node2 --port 30307 --bootnodes "enode://ffa207f30f51b9ceddb82d7677009657b55cc47c21619f684e0aaa885a4b5345d7a4939f87be1f2e069cb8a6996dbcae6e7cfbb5ff25d6859dd692c27d5b59af@127.0.0.1:0?discport=30305" --networkid 12345 --unlock 0x47B9460EE4780DA710aF9156e200817525345c37 --password node1/password.txt --authrpc.port 8552
// to start the node 2 on port 30307 with bootnodes run on the first terminal, run on networkid 12345 which defined in genesis.json file
// unlock the account with the password inside file node2/password.txt
// use rpc port 8552

### Open a new terminal window at the same directory - 4th terminal window
geth attach node1/geth.ipc
// to attach a Javascript console to node 1 to query the network properties
net.peerCount
// to check that the node is connected to one other peer
admin.peers
// to check that the peer
eth.getBalance(eth.accounts[0])
// to see the ether funded at the chain genesis