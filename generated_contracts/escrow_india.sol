// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./base_contract.sol";

/**
 * @title India Escrow Contract
 * @dev Escrow contract compliant with Indian regulations (RBI, GST, KYC)
 * @custom:jurisdiction India
 * @custom:contract-type Escrow
 * @custom:legal-requirements RBI, GST, KYC, PAN, Aadhaar
 */
contract IndiaEscrowContract is BaseContract {
    // India-specific state variables
    mapping(address => string) public panNumbers;
    mapping(address => string) public aadhaarNumbers;
    mapping(address => string) public gstNumbers;
    mapping(address => bool) public kycVerified;
    mapping(address => bool) public gstCompliant;
    
    // RBI compliance variables
    uint256 public constant MAX_TRANSACTION_LIMIT = 1000000 * 10**18; // 1M INR
    uint256 public constant MIN_KYC_VERIFICATION_DAYS = 7;
    uint256 public constant DISPUTE_RESOLUTION_DAYS = 30;
    uint256 public constant REGULATORY_REPORTING_DAYS = 15;
    
    // Events
    event KYCVerified(address indexed party, string panNumber, string aadhaarNumber);
    event GSTComplianceVerified(address indexed party, string gstNumber);
    event RBIReportingSubmitted(address indexed party, uint256 amount, uint256 timestamp);
    event DisputeEscalated(uint256 indexed contractId, string reason, uint256 timestamp);
    
    // Override jurisdiction-specific variables
    string public constant JURISDICTION = "India";
    string[] public legalRequirements = [
        "kyc_verification",
        "pan_card_verification", 
        "aadhaar_verification",
        "gst_compliance",
        "dispute_resolution_mechanism",
        "rbi_guidelines_compliance"
    ];
    
    // Modifiers
    modifier onlyKYCVerified() {
        require(kycVerified[msg.sender], "KYC verification required");
        _;
    }
    
    modifier onlyGSTCompliant() {
        require(gstCompliant[msg.sender], "GST compliance required");
        _;
    }
    
    modifier withinTransactionLimit(uint256 amount) {
        require(amount <= MAX_TRANSACTION_LIMIT, "Amount exceeds RBI transaction limit");
        _;
    }
    
    // Constructor
    constructor() {
        _initializeJurisdictionSpecific();
    }
    
    // India-specific initialization
    function _initializeJurisdictionSpecific() internal override {
        // Initialize India-specific compliance requirements
    }
    
    // KYC Verification Functions
    function verifyKYC(
        address party,
        string memory panNumber,
        string memory aadhaarNumber
    ) external onlyOwner {
        require(bytes(panNumber).length > 0, "PAN number required");
        require(bytes(aadhaarNumber).length > 0, "Aadhaar number required");
        
        panNumbers[party] = panNumber;
        aadhaarNumbers[party] = aadhaarNumber;
        kycVerified[party] = true;
        verifiedParties[party] = true;
        
        emit KYCVerified(party, panNumber, aadhaarNumber);
    }
    
    // GST Compliance Functions
    function verifyGSTCompliance(
        address party,
        string memory gstNumber
    ) external onlyOwner {
        require(bytes(gstNumber).length > 0, "GST number required");
        
        gstNumbers[party] = gstNumber;
        gstCompliant[party] = true;
        
        emit GSTComplianceVerified(party, gstNumber);
    }
    
    // Override core functions with India-specific requirements
    function createContract(
        address payable _payee,
        uint256 _amount,
        uint256 _deadline
    ) external override onlyKYCVerified onlyGSTCompliant withinTransactionLimit(_amount) returns (uint256) {
        require(kycVerified[_payee], "Payee must be KYC verified");
        require(gstCompliant[_payee], "Payee must be GST compliant");
        
        return super.createContract(_payee, _amount, _deadline);
    }
    
    function fundContract(uint256 contractId) external payable override onlyContractParty(contractId) {
        Contract storage contract = contracts[contractId];
        require(contract.status == ContractStatus.Created, "Contract must be in Created status");
        require(msg.value == contract.amount, "Amount must match contract amount");
        require(msg.value <= MAX_TRANSACTION_LIMIT, "Amount exceeds RBI transaction limit");
        
        contract.status = ContractStatus.Funded;
        _verifyLegalCompliance(contractId);
        _submitRBIReporting(contractId);
    }
    
    // India-specific legal compliance verification
    function _verifyLegalCompliance(uint256 contractId) internal override {
        Contract storage contract = contracts[contractId];
        
        // Verify KYC for both parties
        require(kycVerified[contract.payer], "Payer KYC verification required");
        require(kycVerified[contract.payee], "Payee KYC verification required");
        
        // Verify GST compliance for both parties
        require(gstCompliant[contract.payer], "Payer GST compliance required");
        require(gstCompliant[contract.payee], "Payee GST compliance required");
        
        // Verify transaction limits
        require(contract.amount <= MAX_TRANSACTION_LIMIT, "Amount exceeds RBI transaction limit");
        
        contract.legalComplianceVerified = true;
        emit LegalComplianceVerified(msg.sender, "India legal requirements verified");
    }
    
    // RBI Reporting
    function _submitRBIReporting(uint256 contractId) internal {
        Contract storage contract = contracts[contractId];
        
        // In a real implementation, this would submit to RBI's reporting system
        emit RBIReportingSubmitted(msg.sender, contract.amount, block.timestamp);
    }
    
    // India-specific dispute handling
    function _handleDispute(uint256 contractId) internal override {
        Contract storage contract = contracts[contractId];
        
        // India-specific dispute resolution logic
        // 1. Automatic escalation to regulatory authorities
        // 2. Mandatory cooling-off period
        // 3. RBI intervention if required
        
        emit DisputeEscalated(contractId, "Dispute escalated to Indian regulatory authorities", block.timestamp);
        
        // Set dispute resolution deadline
        uint256 disputeDeadline = block.timestamp + (DISPUTE_RESOLUTION_DAYS * 1 days);
        
        // In a real implementation, this would trigger regulatory reporting
        _submitDisputeToRegulator(contractId);
    }
    
    function _submitDisputeToRegulator(uint256 contractId) internal {
        // Submit dispute to RBI and other relevant authorities
        Contract storage contract = contracts[contractId];
        
        // This would include:
        // - Contract details
        // - Party information (KYC verified)
        // - Dispute reason
        // - Amount involved
        // - Timeline for resolution
    }
    
    // India-specific functions
    function getPartyKYCInfo(address party) external view returns (
        string memory panNumber,
        string memory aadhaarNumber,
        bool isVerified
    ) {
        return (panNumbers[party], aadhaarNumbers[party], kycVerified[party]);
    }
    
    function getPartyGSTInfo(address party) external view returns (
        string memory gstNumber,
        bool isCompliant
    ) {
        return (gstNumbers[party], gstCompliant[party]);
    }
    
    function getRBIComplianceInfo() external view returns (
        uint256 maxTransactionLimit,
        uint256 disputeResolutionDays,
        uint256 regulatoryReportingDays
    ) {
        return (MAX_TRANSACTION_LIMIT, DISPUTE_RESOLUTION_DAYS, REGULATORY_REPORTING_DAYS);
    }
    
    // Override legal requirements
    function _getLegalRequirements() internal view override returns (string[] memory) {
        return legalRequirements;
    }
    
    // Emergency functions for regulatory compliance
    function regulatoryFreeze(uint256 contractId) external onlyOwner {
        Contract storage contract = contracts[contractId];
        contract.status = ContractStatus.Cancelled;
        
        // Return funds to payer if contract is funded
        if (contract.status == ContractStatus.Funded) {
            contract.payer.transfer(contract.amount);
        }
    }
    
    function regulatoryAudit(uint256 contractId) external view returns (
        bool kycCompliant,
        bool gstCompliant,
        bool rbiCompliant,
        uint256 transactionAmount
    ) {
        Contract storage contract = contracts[contractId];
        
        kycCompliant = kycVerified[contract.payer] && kycVerified[contract.payee];
        gstCompliant = gstCompliant[contract.payer] && gstCompliant[contract.payee];
        rbiCompliant = contract.amount <= MAX_TRANSACTION_LIMIT;
        transactionAmount = contract.amount;
        
        return (kycCompliant, gstCompliant, rbiCompliant, transactionAmount);
    }
} 