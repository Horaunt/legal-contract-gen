import pytest
import yaml
from pathlib import Path
from dsl.parser import DSLParser, ContractDefinition, Party, Condition, load_legal_rules


class TestDSLParser:
    """Test cases for DSL parser functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = DSLParser()
    
    def test_parse_valid_escrow_contract(self):
        """Test parsing a valid escrow contract definition."""
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
        
        contract_def = self.parser.parse_content(contract_data)
        
        assert contract_def.contract_type == 'escrow'
        assert contract_def.jurisdiction == 'india'
        assert len(contract_def.parties) == 2
        assert len(contract_def.conditions) == 1
        assert len(contract_def.legal_requirements) == 2
        
        # Check parties
        payer = contract_def.parties[0]
        assert payer.name == 'Buyer'
        assert payer.role == 'payer'
        assert payer.address == '0x1234567890123456789012345678901234567890'
        
        payee = contract_def.parties[1]
        assert payee.name == 'Seller'
        assert payee.role == 'payee'
        
        # Check conditions
        condition = contract_def.conditions[0]
        assert condition.trigger == 'delivery_confirmed'
        assert condition.action == 'release_funds'
        assert condition.time_limit == 7
    
    def test_parse_valid_insurance_contract(self):
        """Test parsing a valid insurance contract definition."""
        contract_data = {
            'contract': {
                'type': 'insurance',
                'jurisdiction': 'eu',
                'parties': [
                    {
                        'name': 'Insurance Company',
                        'role': 'insurer',
                        'address': '0x1111111111111111111111111111111111111111'
                    },
                    {
                        'name': 'Policy Holder',
                        'role': 'insured',
                        'address': '0x2222222222222222222222222222222222222222'
                    }
                ],
                'conditions': [
                    {
                        'trigger': 'claim_submitted',
                        'action': 'process_claim',
                        'time_limit': 10
                    }
                ],
                'legal_requirements': ['gdpr_compliance', 'psd2_compliance'],
                'metadata': {'version': '1.0.0'}
            }
        }
        
        contract_def = self.parser.parse_content(contract_data)
        
        assert contract_def.contract_type == 'insurance'
        assert contract_def.jurisdiction == 'eu'
        assert len(contract_def.parties) == 2
        assert len(contract_def.conditions) == 1
        
        # Check parties
        insurer = contract_def.parties[0]
        assert insurer.name == 'Insurance Company'
        assert insurer.role == 'insurer'
        
        insured = contract_def.parties[1]
        assert insured.name == 'Policy Holder'
        assert insured.role == 'insured'
    
    def test_parse_valid_settlement_contract(self):
        """Test parsing a valid settlement contract definition."""
        contract_data = {
            'contract': {
                'type': 'settlement',
                'jurisdiction': 'us',
                'parties': [
                    {
                        'name': 'Plaintiff',
                        'role': 'plaintiff',
                        'address': '0x3333333333333333333333333333333333333333'
                    },
                    {
                        'name': 'Defendant',
                        'role': 'defendant',
                        'address': '0x4444444444444444444444444444444444444444'
                    }
                ],
                'conditions': [
                    {
                        'trigger': 'agreement_reached',
                        'action': 'execute_settlement',
                        'time_limit': 30
                    }
                ],
                'legal_requirements': ['sec_registration', 'state_law_compliance'],
                'metadata': {'version': '1.0.0'}
            }
        }
        
        contract_def = self.parser.parse_content(contract_data)
        
        assert contract_def.contract_type == 'settlement'
        assert contract_def.jurisdiction == 'us'
        assert len(contract_def.parties) == 2
        assert len(contract_def.conditions) == 1
        
        # Check parties
        plaintiff = contract_def.parties[0]
        assert plaintiff.name == 'Plaintiff'
        assert plaintiff.role == 'plaintiff'
        
        defendant = contract_def.parties[1]
        assert defendant.name == 'Defendant'
        assert defendant.role == 'defendant'
    
    def test_invalid_contract_type(self):
        """Test parsing with invalid contract type."""
        contract_data = {
            'contract': {
                'type': 'invalid_type',
                'jurisdiction': 'india',
                'parties': [],
                'conditions': []
            }
        }
        
        with pytest.raises(ValueError, match="Unsupported contract type: invalid_type"):
            self.parser.parse_content(contract_data)
    
    def test_invalid_jurisdiction(self):
        """Test parsing with invalid jurisdiction."""
        contract_data = {
            'contract': {
                'type': 'escrow',
                'jurisdiction': 'invalid_jurisdiction',
                'parties': [],
                'conditions': []
            }
        }
        
        with pytest.raises(ValueError, match="Unsupported jurisdiction: invalid_jurisdiction"):
            self.parser.parse_content(contract_data)
    
    def test_missing_contract_key(self):
        """Test parsing without contract key."""
        contract_data = {
            'invalid_key': {
                'type': 'escrow',
                'jurisdiction': 'india'
            }
        }
        
        with pytest.raises(ValueError, match="Contract definition must contain 'contract' key"):
            self.parser.parse_content(contract_data)
    
    def test_validate_escrow_contract(self):
        """Test validation of escrow contract."""
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
        
        errors = self.parser.validate_contract(contract_def)
        assert len(errors) == 0
    
    def test_validate_escrow_contract_missing_payer(self):
        """Test validation of escrow contract missing payer."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[
                Party(name='Seller', role='payee')
            ],
            conditions=[
                Condition(trigger='delivery_confirmed', action='release_funds')
            ],
            legal_requirements=[],
            metadata={}
        )
        
        errors = self.parser.validate_contract(contract_def)
        assert len(errors) == 2  # Missing payer and insufficient parties
        assert "Contract must have at least two parties" in errors
        assert "Escrow contract must have 'payer' and 'payee' roles" in errors
    
    def test_validate_insurance_contract_missing_insurer(self):
        """Test validation of insurance contract missing insurer."""
        contract_def = ContractDefinition(
            contract_type='insurance',
            jurisdiction='eu',
            parties=[
                Party(name='Policy Holder', role='insured')
            ],
            conditions=[
                Condition(trigger='claim_submitted', action='process_claim')
            ],
            legal_requirements=[],
            metadata={}
        )
        
        errors = self.parser.validate_contract(contract_def)
        assert len(errors) == 2  # Missing insurer and insufficient parties
        assert "Insurance contract must have 'insurer' and 'insured' roles" in errors
    
    def test_validate_settlement_contract_missing_plaintiff(self):
        """Test validation of settlement contract missing plaintiff."""
        contract_def = ContractDefinition(
            contract_type='settlement',
            jurisdiction='us',
            parties=[
                Party(name='Defendant', role='defendant')
            ],
            conditions=[
                Condition(trigger='agreement_reached', action='execute_settlement')
            ],
            legal_requirements=[],
            metadata={}
        )
        
        errors = self.parser.validate_contract(contract_def)
        assert len(errors) == 2  # Missing plaintiff and insufficient parties
        assert "Settlement contract must have 'plaintiff' and 'defendant' roles" in errors
    
    def test_validate_contract_no_conditions(self):
        """Test validation of contract with no conditions."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[
                Party(name='Buyer', role='payer'),
                Party(name='Seller', role='payee')
            ],
            conditions=[],
            legal_requirements=[],
            metadata={}
        )
        
        errors = self.parser.validate_contract(contract_def)
        assert len(errors) == 1
        assert "Contract must have at least one condition" in errors
    
    def test_to_json_conversion(self):
        """Test conversion of contract definition to JSON."""
        contract_def = ContractDefinition(
            contract_type='escrow',
            jurisdiction='india',
            parties=[
                Party(name='Buyer', role='payer', address='0x1234'),
                Party(name='Seller', role='payee', address='0x5678')
            ],
            conditions=[
                Condition(trigger='delivery_confirmed', action='release_funds', time_limit=7)
            ],
            legal_requirements=['kyc_verification'],
            metadata={'version': '1.0.0'}
        )
        
        json_str = self.parser.to_json(contract_def)
        data = yaml.safe_load(json_str)
        
        assert data['contract_type'] == 'escrow'
        assert data['jurisdiction'] == 'india'
        assert len(data['parties']) == 2
        assert len(data['conditions']) == 1
        assert len(data['legal_requirements']) == 1
        
        # Check party data
        assert data['parties'][0]['name'] == 'Buyer'
        assert data['parties'][0]['role'] == 'payer'
        assert data['parties'][0]['address'] == '0x1234'
        
        # Check condition data
        assert data['conditions'][0]['trigger'] == 'delivery_confirmed'
        assert data['conditions'][0]['action'] == 'release_funds'
        assert data['conditions'][0]['time_limit'] == 7


class TestLegalRules:
    """Test cases for legal rules loading."""
    
    def test_load_india_legal_rules(self):
        """Test loading India legal rules."""
        rules = load_legal_rules('india')
        
        assert rules['name'] == 'India'
        assert 'Reserve Bank of India (RBI)' in rules['regulatory_bodies']
        assert 'escrow' in rules['contract_types']
        assert 'insurance' in rules['contract_types']
        assert 'settlement' in rules['contract_types']
        
        # Check escrow specific rules
        escrow_rules = rules['contract_types']['escrow']
        assert 'kyc_verification' in escrow_rules['legal_requirements']
        assert 'gst_compliance' in escrow_rules['legal_requirements']
        assert 'kyc_verification_clause' in escrow_rules['mandatory_clauses']
    
    def test_load_eu_legal_rules(self):
        """Test loading EU legal rules."""
        rules = load_legal_rules('eu')
        
        assert rules['name'] == 'European Union'
        assert 'European Securities and Markets Authority (ESMA)' in rules['regulatory_bodies']
        
        # Check escrow specific rules
        escrow_rules = rules['contract_types']['escrow']
        assert 'gdpr_compliance' in escrow_rules['legal_requirements']
        assert 'psd2_compliance' in escrow_rules['legal_requirements']
    
    def test_load_us_legal_rules(self):
        """Test loading US legal rules."""
        rules = load_legal_rules('us')
        
        assert rules['name'] == 'United States'
        assert 'Securities and Exchange Commission (SEC)' in rules['regulatory_bodies']
        
        # Check escrow specific rules
        escrow_rules = rules['contract_types']['escrow']
        assert 'sec_registration' in escrow_rules['legal_requirements']
        assert 'aml_kyc_requirements' in escrow_rules['legal_requirements']
    
    def test_load_invalid_jurisdiction(self):
        """Test loading legal rules for invalid jurisdiction."""
        with pytest.raises(ValueError, match="Jurisdiction invalid not found in legal rules"):
            load_legal_rules('invalid')


class TestFileParsing:
    """Test cases for file parsing functionality."""
    
    def test_parse_file(self, tmp_path):
        """Test parsing contract definition from file."""
        # Create a temporary contract file
        contract_file = tmp_path / "test_contract.yaml"
        contract_data = {
            'contract': {
                'type': 'escrow',
                'jurisdiction': 'india',
                'parties': [
                    {
                        'name': 'Buyer',
                        'role': 'payer'
                    },
                    {
                        'name': 'Seller',
                        'role': 'payee'
                    }
                ],
                'conditions': [
                    {
                        'trigger': 'delivery_confirmed',
                        'action': 'release_funds'
                    }
                ],
                'legal_requirements': [],
                'metadata': {}
            }
        }
        
        with open(contract_file, 'w') as f:
            yaml.dump(contract_data, f)
        
        parser = DSLParser()
        contract_def = parser.parse_file(str(contract_file))
        
        assert contract_def.contract_type == 'escrow'
        assert contract_def.jurisdiction == 'india'
        assert len(contract_def.parties) == 2
        assert len(contract_def.conditions) == 1 