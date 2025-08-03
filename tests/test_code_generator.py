import pytest
import tempfile
import os
from pathlib import Path
from generators.code_generator import CodeGenerator
from dsl.parser import ContractDefinition, Party, Condition


class TestCodeGenerator:
    """Test cases for code generator functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = CodeGenerator()
    
    def test_generate_india_escrow_contract(self):
        """Test generating India escrow contract."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[
                Party(name='Buyer', role='payer'),
                Party(name='Seller', role='payee')
            ],
            conditions=[
                Condition(trigger='delivery_confirmed', action='release_funds')
            ],
            legal_requirements=['kyc_verification', 'gst_compliance'],
            metadata={}
        )
        
        contract_code = self.generator.generate_contract(contract_def)
        
        # Check that the generated code contains India-specific elements
        assert 'India' in contract_code
        assert 'panNumbers' in contract_code
        assert 'aadhaarNumbers' in contract_code
        assert 'gstNumbers' in contract_code
        assert 'kycVerified' in contract_code
        assert 'gstCompliant' in contract_def
        assert 'MAX_TRANSACTION_LIMIT' in contract_code
        assert 'RBI' in contract_code
        assert 'verifyKYC' in contract_code
        assert 'verifyGSTCompliance' in contract_code
    
    def test_generate_eu_insurance_contract(self):
        """Test generating EU insurance contract."""
        contract_def = ContractDefinition(
            contract_type='insurance',
            jurisdiction='eu',
            parties=[
                Party(name='Insurance Company', role='insurer'),
                Party(name='Policy Holder', role='insured')
            ],
            conditions=[
                Condition(trigger='claim_submitted', action='process_claim')
            ],
            legal_requirements=['gdpr_compliance', 'psd2_compliance'],
            metadata={}
        )
        
        contract_code = self.generator.generate_contract(contract_def)
        
        # Check that the generated code contains EU-specific elements
        assert 'European Union' in contract_code or 'EU' in contract_code
        assert 'gdprCompliant' in contract_code
        assert 'psd2Compliant' in contract_code
        assert 'dataProtectionOfficer' in contract_code
        assert 'GDPR_RESPONSE_DAYS' in contract_code
        assert 'PSD2_COMPLIANCE_DAYS' in contract_code
        assert 'verifyGDPRCompliance' in contract_code
        assert 'verifyPSD2Compliance' in contract_code
    
    def test_generate_us_settlement_contract(self):
        """Test generating US settlement contract."""
        contract_def = ContractDefinition(
            contract_type='settlement',
            jurisdiction='us',
            parties=[
                Party(name='Plaintiff', role='plaintiff'),
                Party(name='Defendant', role='defendant')
            ],
            conditions=[
                Condition(trigger='agreement_reached', action='execute_settlement')
            ],
            legal_requirements=['sec_registration', 'finra_compliance'],
            metadata={}
        )
        
        contract_code = self.generator.generate_contract(contract_def)
        
        # Check that the generated code contains US-specific elements
        assert 'United States' in contract_code or 'US' in contract_code
        assert 'secRegistered' in contract_code
        assert 'finraRegistered' in contract_code
        assert 'stateOfResidence' in contract_code
        assert 'SEC_FILING_DAYS' in contract_code
        assert 'STATE_COMPLIANCE_DAYS' in contract_code
        assert 'verifySECRegistration' in contract_code
        assert 'verifyFINRARegistration' in contract_code
        assert 'setStateOfResidence' in contract_code
    
    def test_save_contract(self):
        """Test saving generated contract to file."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[
                Party(name='Buyer', role='payer'),
                Party(name='Seller', role='payee')
            ],
            conditions=[
                Condition(trigger='delivery_confirmed', action='release_funds')
            ],
            legal_requirements=[],
            metadata={}
        )
        
        contract_code = self.generator.generate_contract(contract_def)
        filepath = self.generator.save_contract(contract_code, contract_def)
        
        assert filepath.endswith('escrow_india.sol')
        assert os.path.exists(filepath)
        
        # Check that the file contains the generated code
        with open(filepath, 'r') as f:
            saved_code = f.read()
            assert contract_code == saved_code
    
    def test_generate_all_contracts(self):
        """Test generating contracts for all jurisdictions."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',  # Will be overridden for each jurisdiction
            parties=[
                Party(name='Buyer', role='payer'),
                Party(name='Seller', role='payee')
            ],
            conditions=[
                Condition(trigger='delivery_confirmed', action='release_funds')
            ],
            legal_requirements=[],
            metadata={}
        )
        
        generated_files = self.generator.generate_all_contracts(contract_def)
        
        assert len(generated_files) == 3
        assert any('escrow_india.sol' in f for f in generated_files)
        assert any('escrow_eu.sol' in f for f in generated_files)
        assert any('escrow_us.sol' in f for f in generated_files)
        
        # Check that all files exist
        for filepath in generated_files:
            assert os.path.exists(filepath)
    
    def test_create_deployment_script(self):
        """Test creating deployment script."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[
                Party(name='Buyer', role='payer'),
                Party(name='Seller', role='payee')
            ],
            conditions=[
                Condition(trigger='delivery_confirmed', action='release_funds')
            ],
            legal_requirements=[],
            metadata={}
        )
        
        deployment_script = self.generator.create_deployment_script(contract_def)
        
        assert deployment_script.endswith('deploy_escrow_india.js')
        assert os.path.exists(deployment_script)
        
        # Check that the deployment script contains expected content
        with open(deployment_script, 'r') as f:
            script_content = f.read()
            assert 'escrow' in script_content
            assert 'india' in script_content
            assert 'EscrowContract' in script_content
            assert 'RBI_GUIDELINES' in script_content
    
    def test_create_test_script(self):
        """Test creating test script."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[
                Party(name='Buyer', role='payer'),
                Party(name='Seller', role='payee')
            ],
            conditions=[
                Condition(trigger='delivery_confirmed', action='release_funds')
            ],
            legal_requirements=[],
            metadata={}
        )
        
        test_script = self.generator.create_test_script(contract_def)
        
        assert test_script.endswith('test_escrow_india.js')
        assert os.path.exists(test_script)
    
    def test_jurisdiction_specific_code(self):
        """Test jurisdiction-specific code generation."""
        # Test India-specific code
        india_code = self.generator._get_jurisdiction_specific_code('india')
        assert 'panNumbers' in india_code['jurisdiction_specific_variables']
        assert 'aadhaarNumbers' in india_code['jurisdiction_specific_variables']
        assert 'gstNumbers' in india_code['jurisdiction_specific_variables']
        assert 'verifyKYC' in india_code['jurisdiction_specific_functions']
        assert 'verifyGSTCompliance' in india_code['jurisdiction_specific_functions']
        
        # Test EU-specific code
        eu_code = self.generator._get_jurisdiction_specific_code('eu')
        assert 'gdprCompliant' in eu_code['jurisdiction_specific_variables']
        assert 'psd2Compliant' in eu_code['jurisdiction_specific_variables']
        assert 'verifyGDPRCompliance' in eu_code['jurisdiction_specific_functions']
        assert 'verifyPSD2Compliance' in eu_code['jurisdiction_specific_functions']
        
        # Test US-specific code
        us_code = self.generator._get_jurisdiction_specific_code('us')
        assert 'secRegistered' in us_code['jurisdiction_specific_variables']
        assert 'finraRegistered' in us_code['jurisdiction_specific_variables']
        assert 'verifySECRegistration' in us_code['jurisdiction_specific_functions']
        assert 'verifyFINRARegistration' in us_code['jurisdiction_specific_functions']
    
    def test_get_constructor_args(self):
        """Test getting constructor arguments for different jurisdictions."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[],
            conditions=[],
            legal_requirements=[],
            metadata={}
        )
        
        # Test India constructor args
        contract_def.jurisdiction = 'india'
        india_args = self.generator._get_constructor_args(contract_def)
        assert len(india_args) == 1
        assert 'RBI_GUIDELINES' in india_args[0]
        assert 'GST_COMPLIANCE' in india_args[0]
        assert 'KYC_VERIFICATION' in india_args[0]
        
        # Test EU constructor args
        contract_def.jurisdiction = 'eu'
        eu_args = self.generator._get_constructor_args(contract_def)
        assert len(eu_args) == 1
        assert 'GDPR_COMPLIANCE' in eu_args[0]
        assert 'PSD2_COMPLIANCE' in eu_args[0]
        assert 'MICA_REGULATIONS' in eu_args[0]
        
        # Test US constructor args
        contract_def.jurisdiction = 'us'
        us_args = self.generator._get_constructor_args(contract_def)
        assert len(us_args) == 1
        assert 'SEC_REGISTRATION' in us_args[0]
        assert 'FINRA_COMPLIANCE' in us_args[0]
        assert 'STATE_LAWS' in us_args[0]
    
    def test_get_test_cases(self):
        """Test getting test cases for different jurisdictions."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[],
            conditions=[],
            legal_requirements=[],
            metadata={}
        )
        
        # Test base test cases
        test_cases = self.generator._get_test_cases(contract_def)
        assert len(test_cases) >= 2
        
        # Check for base test cases
        base_case_names = [case['name'] for case in test_cases]
        assert 'Contract Creation' in base_case_names
        assert 'Legal Compliance' in base_case_names
        
        # Test India-specific test cases
        contract_def.jurisdiction = 'india'
        india_test_cases = self.generator._get_test_cases(contract_def)
        india_case_names = [case['name'] for case in india_test_cases]
        assert 'KYC Verification' in india_case_names
        assert 'GST Compliance' in india_case_names
    
    def test_template_name_selection(self):
        """Test template name selection for different contract types."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[],
            conditions=[],
            legal_requirements=[],
            metadata={}
        )
        
        # Test escrow template
        template_name = self.generator._get_template_name(contract_def)
        assert template_name == 'india_escrow.sol'
        
        # Test insurance template
        contract_def.contract_type = 'insurance'
        template_name = self.generator._get_template_name(contract_def)
        assert template_name == 'india_insurance.sol'
        
        # Test settlement template
        contract_def.contract_type = 'settlement'
        template_name = self.generator._get_template_name(contract_def)
        assert template_name == 'india_settlement.sol'
        
        # Test unknown contract type
        contract_def.contract_type = 'unknown'
        template_name = self.generator._get_template_name(contract_def)
        assert template_name == 'base_contract.sol'


class TestCodeGeneratorIntegration:
    """Integration tests for code generator."""
    
    def test_end_to_end_contract_generation(self):
        """Test end-to-end contract generation from DSL to Solidity."""
        from dsl.parser import DSLParser
        
        # Create a contract definition
        contract_data = {
            'contract': {
                'type': 'escrow',
                'jurisdiction': 'india',
                'parties': [
                    {
                        'name': 'Buyer',
                        'role': 'payer',
                        'address': '0x1234567890123456789012345678901234567890'
                    },
                    {
                        'name': 'Seller',
                        'role': 'payee',
                        'address': '0x0987654321098765432109876543210987654321'
                    }
                ],
                'conditions': [
                    {
                        'trigger': 'delivery_confirmed',
                        'action': 'release_funds',
                        'time_limit': 7
                    }
                ],
                'legal_requirements': ['kyc_verification', 'gst_compliance'],
                'metadata': {'version': '1.0.0'}
            }
        }
        
        # Parse the contract definition
        parser = DSLParser()
        contract_def = parser.parse_content(contract_data)
        
        # Generate the contract
        generator = CodeGenerator()
        contract_code = generator.generate_contract(contract_def)
        
        # Verify the generated code
        assert 'contract' in contract_code
        assert 'India' in contract_code
        assert 'escrow' in contract_code.lower()
        assert 'panNumbers' in contract_code
        assert 'aadhaarNumbers' in contract_code
        assert 'gstNumbers' in contract_code
        assert 'verifyKYC' in contract_code
        assert 'verifyGSTCompliance' in contract_code
        
        # Save the contract
        filepath = generator.save_contract(contract_code, contract_def)
        assert os.path.exists(filepath)
        
        # Create deployment script
        deployment_script = generator.create_deployment_script(contract_def)
        assert os.path.exists(deployment_script)
        
        # Create test script
        test_script = generator.create_test_script(contract_def)
        assert os.path.exists(test_script) 