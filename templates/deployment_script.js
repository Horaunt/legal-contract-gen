const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying {{contract_type}} contract for {{jurisdiction}} jurisdiction...");

  // Get the contract factory
  const {{contract_name}} = await ethers.getContractFactory("{{contract_name}}");
  
  // Deploy the contract with constructor arguments
  const contract = await {{contract_name}}.deploy({{constructor_args}});
  
  // Wait for deployment to complete
  await contract.deployed();
  
  console.log("{{contract_name}} deployed to:", contract.address);
  
  // Verify the contract on Etherscan (if not on localhost)
  if (network.name !== "localhost" && network.name !== "hardhat") {
    console.log("Waiting for block confirmations...");
    await contract.deployTransaction.wait(6);
    
    try {
      await hre.run("verify:verify", {
        address: contract.address,
        constructorArguments: [{{constructor_args}}],
      });
      console.log("Contract verified on Etherscan");
    } catch (error) {
      console.log("Verification failed:", error.message);
    }
  }
  
  // Log deployment information
  console.log("\n=== Deployment Summary ===");
  console.log("Contract Type: {{contract_type}}");
  console.log("Jurisdiction: {{jurisdiction}}");
  console.log("Contract Address:", contract.address);
  console.log("Network:", network.name);
  console.log("Deployer:", await contract.signer.getAddress());
  
  // Save deployment info to file
  const fs = require("fs");
  const deploymentInfo = {
    contractType: "{{contract_type}}",
    jurisdiction: "{{jurisdiction}}",
    contractAddress: contract.address,
    network: network.name,
    deployer: await contract.signer.getAddress(),
    deploymentTime: new Date().toISOString(),
    constructorArgs: [{{constructor_args}}]
  };
  
  fs.writeFileSync(
    `deployment_{{contract_type}}_{{jurisdiction}}.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );
  
  console.log("Deployment info saved to deployment_{{contract_type}}_{{jurisdiction}}.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 