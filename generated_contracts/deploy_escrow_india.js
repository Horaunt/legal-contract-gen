const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying escrow contract for india jurisdiction...");

  // Get the contract factory
  const EscrowContract = await ethers.getContractFactory("EscrowContract");
  
  // Deploy the contract with constructor arguments
  const contract = await EscrowContract.deploy(['"RBI_GUIDELINES", "GST_COMPLIANCE", "KYC_VERIFICATION"']);
  
  // Wait for deployment to complete
  await contract.deployed();
  
  console.log("EscrowContract deployed to:", contract.address);
  
  // Verify the contract on Etherscan (if not on localhost)
  if (network.name !== "localhost" && network.name !== "hardhat") {
    console.log("Waiting for block confirmations...");
    await contract.deployTransaction.wait(6);
    
    try {
      await hre.run("verify:verify", {
        address: contract.address,
        constructorArguments: [['"RBI_GUIDELINES", "GST_COMPLIANCE", "KYC_VERIFICATION"']],
      });
      console.log("Contract verified on Etherscan");
    } catch (error) {
      console.log("Verification failed:", error.message);
    }
  }
  
  // Log deployment information
  console.log("\n=== Deployment Summary ===");
  console.log("Contract Type: escrow");
  console.log("Jurisdiction: india");
  console.log("Contract Address:", contract.address);
  console.log("Network:", network.name);
  console.log("Deployer:", await contract.signer.getAddress());
  
  // Save deployment info to file
  const fs = require("fs");
  const deploymentInfo = {
    contractType: "escrow",
    jurisdiction: "india",
    contractAddress: contract.address,
    network: network.name,
    deployer: await contract.signer.getAddress(),
    deploymentTime: new Date().toISOString(),
    constructorArgs: [['"RBI_GUIDELINES", "GST_COMPLIANCE", "KYC_VERIFICATION"']]
  };
  
  fs.writeFileSync(
    `deployment_escrow_india.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );
  
  console.log("Deployment info saved to deployment_escrow_india.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 