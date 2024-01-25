async function main() {
    const Project = await ethers.getContractFactory("project");
 
    // Start deployment, returning a promise that resolves to a contract object
    const _project = await Project.deploy();   
    console.log("Contract deployed to address:", _project.address);
 }
 
 main()
   .then(() => process.exit(0))
   .catch(error => {
     console.error(error);
     process.exit(1);
   });