// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title Base Smart Contract Template
 * @dev Base contract with jurisdiction-specific legal compliance
 * @custom:jurisdiction {{JURISDICTION}}
 * @custom:contract-type {{CONTRACT_TYPE}}
 * @custom:legal-requirements {{LEGAL_REQUIREMENTS}}
 */
contract BaseContract is ReentrancyGuard, Ownable {
    using Counters for Counters.Counter;
    
    // Events
    event ContractCreated(address indexed creator, uint256 contractId);
    event LegalComplianceVerified(address indexed party, string requirement);
    event DisputeRaised(uint256 indexed contractId, address indexed party, string reason);
    event SettlementReached(uint256 indexed contractId, address indexed party, uint256 amount);
    
    // State variables
    Counters.Counter private _contractIds;
    mapping(uint256 => Contract) public contracts;
    mapping(address => bool) public verifiedParties;
    mapping(uint256 => Dispute[]) public disputes;
    
    // Structs
    struct Contract {
        uint256 id;
        address payable payer;
        address payable payee;
        uint256 amount;
        ContractStatus status;
        uint256 createdAt;
        uint256 deadline;
        string jurisdiction;
        string[] legalRequirements;
        bool legalComplianceVerified;
    }
    
    struct Dispute {
        address party;
        string reason;
        uint256 timestamp;
        bool resolved;
    }
    
    enum ContractStatus {
        Created,
        Funded,
        InProgress,
        Completed,
        Disputed,
        Settled,
        Cancelled
    }
    
    // Jurisdiction-specific variables
    {{JURISDICTION_SPECIFIC_VARIABLES}}
    
    // Modifiers
    modifier onlyContractParty(uint256 contractId) {
        require(
            msg.sender == contracts[contractId].payer || 
            msg.sender == contracts[contractId].payee,
            "Only contract parties can perform this action"
        );
        _;
    }
    
    modifier onlyVerifiedParty() {
        require(verifiedParties[msg.sender], "Party must be verified for legal compliance");
        _;
    }
    
    modifier onlyLegalCompliant(uint256 contractId) {
        require(
            contracts[contractId].legalComplianceVerified,
            "Contract must meet legal compliance requirements"
        );
        _;
    }
    
    // Constructor
    constructor() {
        _initializeJurisdictionSpecific();
    }
    
    // Jurisdiction-specific initialization
    function _initializeJurisdictionSpecific() internal virtual {
        {{JURISDICTION_INITIALIZATION}}
    }
    
    // Core contract functions
    function createContract(
        address payable _payee,
        uint256 _amount,
        uint256 _deadline
    ) external onlyVerifiedParty returns (uint256) {
        require(_payee != address(0), "Invalid payee address");
        require(_amount > 0, "Amount must be greater than 0");
        require(_deadline > block.timestamp, "Deadline must be in the future");
        
        _contractIds.increment();
        uint256 contractId = _contractIds.current();
        
        contracts[contractId] = Contract({
            id: contractId,
            payer: payable(msg.sender),
            payee: _payee,
            amount: _amount,
            status: ContractStatus.Created,
            createdAt: block.timestamp,
            deadline: _deadline,
            jurisdiction: "{{JURISDICTION}}",
            legalRequirements: _getLegalRequirements(),
            legalComplianceVerified: false
        });
        
        emit ContractCreated(msg.sender, contractId);
        return contractId;
    }
    
    function fundContract(uint256 contractId) external payable onlyContractParty(contractId) {
        Contract storage contract = contracts[contractId];
        require(contract.status == ContractStatus.Created, "Contract must be in Created status");
        require(msg.value == contract.amount, "Amount must match contract amount");
        
        contract.status = ContractStatus.Funded;
        _verifyLegalCompliance(contractId);
    }
    
    function completeContract(uint256 contractId) external onlyContractParty(contractId) onlyLegalCompliant(contractId) {
        Contract storage contract = contracts[contractId];
        require(contract.status == ContractStatus.Funded, "Contract must be funded");
        
        contract.status = ContractStatus.Completed;
        contract.payee.transfer(contract.amount);
    }
    
    function raiseDispute(uint256 contractId, string memory reason) external onlyContractParty(contractId) {
        Contract storage contract = contracts[contractId];
        require(contract.status != ContractStatus.Completed, "Cannot dispute completed contract");
        
        contract.status = ContractStatus.Disputed;
        
        disputes[contractId].push(Dispute({
            party: msg.sender,
            reason: reason,
            timestamp: block.timestamp,
            resolved: false
        }));
        
        emit DisputeRaised(contractId, msg.sender, reason);
        _handleDispute(contractId);
    }
    
    // Legal compliance functions
    function _verifyLegalCompliance(uint256 contractId) internal {
        Contract storage contract = contracts[contractId];
        
        // Jurisdiction-specific legal verification
        {{LEGAL_COMPLIANCE_VERIFICATION}}
        
        contract.legalComplianceVerified = true;
        emit LegalComplianceVerified(msg.sender, "All legal requirements verified");
    }
    
    function _getLegalRequirements() internal view returns (string[] memory) {
        {{LEGAL_REQUIREMENTS_RETURN}}
    }
    
    // Jurisdiction-specific dispute handling
    function _handleDispute(uint256 contractId) internal virtual {
        {{DISPUTE_HANDLING_LOGIC}}
    }
    
    // Jurisdiction-specific functions
    {{JURISDICTION_SPECIFIC_FUNCTIONS}}
    
    // View functions
    function getContract(uint256 contractId) external view returns (Contract memory) {
        return contracts[contractId];
    }
    
    function getDisputes(uint256 contractId) external view returns (Dispute[] memory) {
        return disputes[contractId];
    }
    
    function isPartyVerified(address party) external view returns (bool) {
        return verifiedParties[party];
    }
    
    // Emergency functions
    function emergencyWithdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
    
    // Receive function
    receive() external payable {}
} 