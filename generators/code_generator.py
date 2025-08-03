import os
import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader
from dsl.parser import ContractDefinition, load_legal_rules


class CodeGenerator:
    """Generates Solidity code from contract definitions and legal rules."""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / 'templates'
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        self.output_dir = Path(__file__).parent.parent / 'generated_contracts'
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_contract(self, contract_def: ContractDefinition) -> str:
        """Generate Solidity contract code from contract definition."""
        # Load legal rules for the jurisdiction
        legal_rules = load_legal_rules(contract_def.jurisdiction)
        
        # Get contract type specific rules
        contract_rules = legal_rules['contract_types'].get(contract_def.contract_type, {})
        
        # Prepare template context
        context = self._prepare_context(contract_def, legal_rules, contract_rules)
        
        # Select appropriate template
        template_name = self._get_template_name(contract_def)
        template = self.env.get_template(template_name)
        
        # Generate the contract
        contract_code = template.render(**context)
        
        return contract_code
    
    def _prepare_context(self, contract_def: ContractDefinition, legal_rules: Dict, contract_rules: Dict) -> Dict[str, Any]:
        """Prepare context for template rendering."""
        context = {
            'contract_type': contract_def.contract_type,
            'jurisdiction': contract_def.jurisdiction,
            'parties': contract_def.parties,
            'conditions': contract_def.conditions,
            'legal_requirements': contract_def.legal_requirements,
            'metadata': contract_def.metadata,
            'legal_rules': legal_rules,
            'contract_rules': contract_rules,
            'jurisdiction_name': legal_rules['name'],
            'regulatory_bodies': legal_rules['regulatory_bodies'],
            'mandatory_clauses': contract_rules.get('mandatory_clauses', []),
            'time_limits': contract_rules.get('time_limits', {}),
            'legal_requirements_list': contract_rules.get('legal_requirements', [])
        }
        
        # Add jurisdiction-specific variables and functions
        context.update(self._get_jurisdiction_specific_code(contract_def.jurisdiction))
        
        return context
    
    def _get_jurisdiction_specific_code(self, jurisdiction: str) -> Dict[str, str]:
        """Get jurisdiction-specific code snippets."""
        jurisdiction_code = {
            'india': {
                'jurisdiction_specific_variables': '''
    // India-specific variables
    mapping(address => string) public panNumbers;
    mapping(address => string) public aadhaarNumbers;
    mapping(address => string) public gstNumbers;
    mapping(address => bool) public kycVerified;
    mapping(address => bool) public gstCompliant;
    uint256 public constant MAX_TRANSACTION_LIMIT = 1000000 * 10**18;
    uint256 public constant DISPUTE_RESOLUTION_DAYS = 30;
''',
                'jurisdiction_initialization': '''
        // Initialize India-specific compliance requirements
        // RBI guidelines, GST compliance, KYC requirements
''',
                'legal_compliance_verification': '''
        // India-specific legal verification
        require(kycVerified[contract.payer], "Payer KYC verification required");
        require(kycVerified[contract.payee], "Payee KYC verification required");
        require(gstCompliant[contract.payer], "Payer GST compliance required");
        require(gstCompliant[contract.payee], "Payee GST compliance required");
        require(contract.amount <= MAX_TRANSACTION_LIMIT, "Amount exceeds RBI limit");
''',
                'legal_requirements_return': '''
        string[] memory requirements = new string[](6);
        requirements[0] = "kyc_verification";
        requirements[1] = "pan_card_verification";
        requirements[2] = "aadhaar_verification";
        requirements[3] = "gst_compliance";
        requirements[4] = "dispute_resolution_mechanism";
        requirements[5] = "rbi_guidelines_compliance";
        return requirements;
''',
                'dispute_handling_logic': '''
        // India-specific dispute resolution
        emit DisputeEscalated(contractId, "Dispute escalated to RBI", block.timestamp);
        _submitDisputeToRegulator(contractId);
''',
                'jurisdiction_specific_functions': '''
    // India-specific functions
    function verifyKYC(address party, string memory panNumber, string memory aadhaarNumber) external onlyOwner {
        panNumbers[party] = panNumber;
        aadhaarNumbers[party] = aadhaarNumber;
        kycVerified[party] = true;
        verifiedParties[party] = true;
    }
    
    function verifyGSTCompliance(address party, string memory gstNumber) external onlyOwner {
        gstNumbers[party] = gstNumber;
        gstCompliant[party] = true;
    }
'''
            },
            'eu': {
                'jurisdiction_specific_variables': '''
    // EU-specific variables
    mapping(address => bool) public gdprCompliant;
    mapping(address => bool) public psd2Compliant;
    mapping(address => string) public dataProtectionOfficer;
    uint256 public constant GDPR_RESPONSE_DAYS = 30;
    uint256 public constant PSD2_COMPLIANCE_DAYS = 14;
''',
                'jurisdiction_initialization': '''
        // Initialize EU-specific compliance requirements
        // GDPR, PSD2, MiCA regulations
''',
                'legal_compliance_verification': '''
        // EU-specific legal verification
        require(gdprCompliant[contract.payer], "Payer GDPR compliance required");
        require(gdprCompliant[contract.payee], "Payee GDPR compliance required");
        require(psd2Compliant[contract.payer], "Payer PSD2 compliance required");
        require(psd2Compliant[contract.payee], "Payee PSD2 compliance required");
''',
                'legal_requirements_return': '''
        string[] memory requirements = new string[](5);
        requirements[0] = "gdpr_compliance";
        requirements[1] = "psd2_compliance";
        requirements[2] = "aml_kyc_requirements";
        requirements[3] = "consumer_protection_laws";
        requirements[4] = "mica_compliance";
        return requirements;
''',
                'dispute_handling_logic': '''
        // EU-specific dispute resolution
        emit DisputeEscalated(contractId, "Dispute escalated to ESMA", block.timestamp);
        _submitDisputeToEUAuthorities(contractId);
''',
                'jurisdiction_specific_functions': '''
    // EU-specific functions
    function verifyGDPRCompliance(address party, string memory dpo) external onlyOwner {
        gdprCompliant[party] = true;
        dataProtectionOfficer[party] = dpo;
    }
    
    function verifyPSD2Compliance(address party) external onlyOwner {
        psd2Compliant[party] = true;
    }
'''
            },
            'us': {
                'jurisdiction_specific_variables': '''
    // US-specific variables
    mapping(address => bool) public secRegistered;
    mapping(address => bool) public finraRegistered;
    mapping(address => string) public stateOfResidence;
    uint256 public constant SEC_FILING_DAYS = 10;
    uint256 public constant STATE_COMPLIANCE_DAYS = 15;
''',
                'jurisdiction_initialization': '''
        // Initialize US-specific compliance requirements
        // SEC, FINRA, state-specific regulations
''',
                'legal_compliance_verification': '''
        // US-specific legal verification
        require(secRegistered[contract.payer], "Payer SEC registration required");
        require(secRegistered[contract.payee], "Payee SEC registration required");
        require(finraRegistered[contract.payer], "Payer FINRA registration required");
        require(finraRegistered[contract.payee], "Payee FINRA registration required");
''',
                'legal_requirements_return': '''
        string[] memory requirements = new string[](5);
        requirements[0] = "sec_registration";
        requirements[1] = "aml_kyc_requirements";
        requirements[2] = "state_specific_laws";
        requirements[3] = "ucc_compliance";
        requirements[4] = "consumer_protection";
        return requirements;
''',
                'dispute_handling_logic': '''
        // US-specific dispute resolution
        emit DisputeEscalated(contractId, "Dispute escalated to SEC", block.timestamp);
        _submitDisputeToSEC(contractId);
''',
                'jurisdiction_specific_functions': '''
    // US-specific functions
    function verifySECRegistration(address party, string memory secNumber) external onlyOwner {
        secRegistered[party] = true;
    }
    
    function verifyFINRARegistration(address party, string memory finraNumber) external onlyOwner {
        finraRegistered[party] = true;
    }
    
    function setStateOfResidence(address party, string memory state) external onlyOwner {
        stateOfResidence[party] = state;
    }
'''
            }
        }
        
        return jurisdiction_code.get(jurisdiction, {})
    
    def _get_template_name(self, contract_def: ContractDefinition) -> str:
        """Get the appropriate template name based on contract type and jurisdiction."""
        if contract_def.contract_type == 'escrow':
            return f"{contract_def.jurisdiction}_escrow.sol"
        elif contract_def.contract_type == 'insurance':
            return f"{contract_def.jurisdiction}_insurance.sol"
        elif contract_def.contract_type == 'settlement':
            return f"{contract_def.jurisdiction}_settlement.sol"
        else:
            return "base_contract.sol"
    
    def save_contract(self, contract_code: str, contract_def: ContractDefinition) -> str:
        """Save generated contract to file."""
        filename = f"{contract_def.contract_type}_{contract_def.jurisdiction}.sol"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(contract_code)
        
        return str(filepath)
    
    def generate_all_contracts(self, contract_def: ContractDefinition) -> List[str]:
        """Generate all contract variants for a given definition."""
        generated_files = []
        
        # Generate for all supported jurisdictions
        for jurisdiction in ['india', 'eu', 'us']:
            contract_def.jurisdiction = jurisdiction
            contract_code = self.generate_contract(contract_def)
            filepath = self.save_contract(contract_code, contract_def)
            generated_files.append(filepath)
        
        return generated_files
    
    def create_deployment_script(self, contract_def: ContractDefinition) -> str:
        """Create a deployment script for the generated contract."""
        template = self.env.get_template('deployment_script.js')
        
        context = {
            'contract_type': contract_def.contract_type,
            'jurisdiction': contract_def.jurisdiction,
            'contract_name': f"{contract_def.contract_type.capitalize()}Contract",
            'constructor_args': self._get_constructor_args(contract_def)
        }
        
        deployment_script = template.render(**context)
        
        # Save deployment script
        filename = f"deploy_{contract_def.contract_type}_{contract_def.jurisdiction}.js"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(deployment_script)
        
        return str(filepath)
    
    def _get_constructor_args(self, contract_def: ContractDefinition) -> List[str]:
        """Get constructor arguments for the contract."""
        if contract_def.jurisdiction == 'india':
            return ['"RBI_GUIDELINES", "GST_COMPLIANCE", "KYC_VERIFICATION"']
        elif contract_def.jurisdiction == 'eu':
            return ['"GDPR_COMPLIANCE", "PSD2_COMPLIANCE", "MICA_REGULATIONS"']
        elif contract_def.jurisdiction == 'us':
            return ['"SEC_REGISTRATION", "FINRA_COMPLIANCE", "STATE_LAWS"']
        else:
            return []
    
    def create_test_script(self, contract_def: ContractDefinition) -> str:
        """Create a test script for the generated contract."""
        template = self.env.get_template('test_script.js')
        
        context = {
            'contract_type': contract_def.contract_type,
            'jurisdiction': contract_def.jurisdiction,
            'contract_name': f"{contract_def.contract_type.capitalize()}Contract",
            'test_cases': self._get_test_cases(contract_def)
        }
        
        test_script = template.render(**context)
        
        # Save test script
        filename = f"test_{contract_def.contract_type}_{contract_def.jurisdiction}.js"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(test_script)
        
        return str(filepath)
    
    def _get_test_cases(self, contract_def: ContractDefinition) -> List[Dict[str, Any]]:
        """Get test cases for the contract."""
        base_cases = [
            {
                'name': 'Contract Creation',
                'description': 'Test contract creation with valid parameters',
                'function': 'createContract',
                'args': ['payee', 'amount', 'deadline']
            },
            {
                'name': 'Legal Compliance',
                'description': 'Test legal compliance verification',
                'function': 'verifyLegalCompliance',
                'args': ['contractId']
            }
        ]
        
        # Add jurisdiction-specific test cases
        if contract_def.jurisdiction == 'india':
            base_cases.extend([
                {
                    'name': 'KYC Verification',
                    'description': 'Test KYC verification for parties',
                    'function': 'verifyKYC',
                    'args': ['party', 'panNumber', 'aadhaarNumber']
                },
                {
                    'name': 'GST Compliance',
                    'description': 'Test GST compliance verification',
                    'function': 'verifyGSTCompliance',
                    'args': ['party', 'gstNumber']
                }
            ])
        
        return base_cases 