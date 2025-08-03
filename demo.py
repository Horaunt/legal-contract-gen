#!/usr/bin/env python3
"""
Demonstration Script for Jurisdiction-Specific Smart Contract Generator

This script demonstrates the complete workflow:
1. Parse DSL contract definitions
2. Generate jurisdiction-specific Solidity contracts
3. Create deployment and test scripts
4. Show legal compliance features
"""

import sys
import os
from pathlib import Path
import yaml
import json

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from dsl.parser import DSLParser, ContractDefinition, Party, Condition
from generators.code_generator import CodeGenerator


def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def print_section(title):
    """Print a formatted section."""
    print(f"\n--- {title} ---")


def demo_dsl_parsing():
    """Demonstrate DSL parsing functionality."""
    print_header("DSL PARSING DEMONSTRATION")
    
    # Create a sample contract definition
    contract_data = {
        'contract': {
            'type': 'escrow',
            'jurisdiction': 'india',
            'parties': [
                {
                    'name': 'Buyer',
                    'role': 'payer',
                    'address': '0x1234567890123456789012345678901234567890',
                    'verification_required': True
                },
                {
                    'name': 'Seller',
                    'role': 'payee',
                    'address': '0x0987654321098765432109876543210987654321',
                    'verification_required': True
                }
            ],
            'conditions': [
                {
                    'trigger': 'delivery_confirmed',
                    'action': 'release_funds',
                    'time_limit': 7,
                    'parameters': {
                        'confirmation_method': 'digital_signature',
                        'delivery_proof_required': True
                    }
                },
                {
                    'trigger': 'dispute_raised',
                    'action': 'freeze_funds',
                    'time_limit': 30,
                    'parameters': {
                        'dispute_resolution_authority': 'rbi',
                        'cooling_off_period': 7
                    }
                }
            ],
            'legal_requirements': [
                'kyc_verification',
                'pan_card_verification',
                'aadhaar_verification',
                'gst_compliance',
                'dispute_resolution_mechanism',
                'rbi_guidelines_compliance'
            ],
            'metadata': {
                'description': 'India-compliant escrow contract',
                'version': '1.0.0',
                'author': 'Smart Contract Generator'
            }
        }
    }
    
    print("Sample Contract Definition (YAML):")
    print(yaml.dump(contract_data, default_flow_style=False, indent=2))
    
    # Parse the contract definition
    parser = DSLParser()
    contract_def = parser.parse_content(contract_data)
    
    print_section("Parsed Contract Definition")
    print(f"Contract Type: {contract_def.contract_type}")
    print(f"Jurisdiction: {contract_def.jurisdiction}")
    print(f"Number of Parties: {len(contract_def.parties)}")
    print(f"Number of Conditions: {len(contract_def.conditions)}")
    print(f"Legal Requirements: {len(contract_def.legal_requirements)}")
    
    print_section("Parties")
    for party in contract_def.parties:
        print(f"  - {party.name} ({party.role})")
        if party.address:
            print(f"    Address: {party.address}")
        print(f"    Verification Required: {party.verification_required}")
    
    print_section("Conditions")
    for i, condition in enumerate(contract_def.conditions, 1):
        print(f"  {i}. Trigger: {condition.trigger}")
        print(f"     Action: {condition.action}")
        print(f"     Time Limit: {condition.time_limit} days")
        if condition.parameters:
            print(f"     Parameters: {condition.parameters}")
    
    print_section("Legal Requirements")
    for req in contract_def.legal_requirements:
        print(f"  - {req}")
    
    # Validate the contract
    errors = parser.validate_contract(contract_def)
    if errors:
        print_section("Validation Errors")
        for error in errors:
            print(f"  ❌ {error}")
    else:
        print_section("Validation")
        print("  ✅ Contract definition is valid!")
    
    return contract_def


def demo_legal_rules():
    """Demonstrate legal rules loading."""
    print_header("LEGAL RULES DEMONSTRATION")
    
    from dsl.parser import load_legal_rules
    
    jurisdictions = ['india', 'eu', 'us']
    
    for jurisdiction in jurisdictions:
        print_section(f"Legal Rules for {jurisdiction.upper()}")
        
        try:
            rules = load_legal_rules(jurisdiction)
            print(f"Jurisdiction Name: {rules['name']}")
            print(f"Regulatory Bodies:")
            for body in rules['regulatory_bodies']:
                print(f"  - {body}")
            
            print(f"Contract Types:")
            for contract_type in rules['contract_types']:
                contract_rules = rules['contract_types'][contract_type]
                print(f"  - {contract_type}:")
                print(f"    Legal Requirements: {len(contract_rules['legal_requirements'])}")
                print(f"    Mandatory Clauses: {len(contract_rules['mandatory_clauses'])}")
                print(f"    Time Limits: {len(contract_rules['time_limits'])}")
        
        except Exception as e:
            print(f"Error loading rules for {jurisdiction}: {e}")


def demo_contract_generation(contract_def):
    """Demonstrate contract generation."""
    print_header("CONTRACT GENERATION DEMONSTRATION")
    
    generator = CodeGenerator()
    
    # Generate contract for India
    print_section("Generating India Escrow Contract")
    contract_code = generator.generate_contract(contract_def)
    
    # Save the contract
    filepath = generator.save_contract(contract_code, contract_def)
    print(f"Contract saved to: {filepath}")
    
    # Show key features of the generated contract
    print_section("Generated Contract Features")
    
    features_to_check = [
        ('India-specific variables', ['panNumbers', 'aadhaarNumbers', 'gstNumbers']),
        ('KYC verification', ['kycVerified', 'verifyKYC']),
        ('GST compliance', ['gstCompliant', 'verifyGSTCompliance']),
        ('RBI compliance', ['MAX_TRANSACTION_LIMIT', 'RBI']),
        ('Dispute resolution', ['DisputeEscalated', 'dispute_resolution']),
        ('Legal compliance', ['legalComplianceVerified', 'LegalComplianceVerified'])
    ]
    
    for feature_name, keywords in features_to_check:
        found = all(keyword in contract_code for keyword in keywords)
        status = "✅" if found else "❌"
        print(f"  {status} {feature_name}")
    
    # Generate for all jurisdictions
    print_section("Generating Contracts for All Jurisdictions")
    generated_files = generator.generate_all_contracts(contract_def)
    
    for filepath in generated_files:
        print(f"  ✅ {os.path.basename(filepath)}")
    
    # Create deployment and test scripts
    print_section("Creating Deployment and Test Scripts")
    deployment_script = generator.create_deployment_script(contract_def)
    test_script = generator.create_test_script(contract_def)
    
    print(f"  ✅ Deployment script: {os.path.basename(deployment_script)}")
    print(f"  ✅ Test script: {os.path.basename(test_script)}")
    
    return contract_code


def demo_jurisdiction_comparison():
    """Demonstrate differences between jurisdictions."""
    print_header("JURISDICTION COMPARISON")
    
    generator = CodeGenerator()
    
    # Create a basic contract definition
    contract_def = ContractDefinition(
        contract_type='escrow',
        jurisdiction='india',  # Will be overridden
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
    
    jurisdictions = ['india', 'eu', 'us']
    
    print_section("Legal Requirements Comparison")
    print(f"{'Jurisdiction':<12} {'Legal Requirements':<50} {'Key Features'}")
    print("-" * 80)
    
    for jurisdiction in jurisdictions:
        contract_def.jurisdiction = jurisdiction
        legal_rules = generator._get_jurisdiction_specific_code(jurisdiction)
        
        # Extract key features
        key_features = []
        if 'panNumbers' in legal_rules.get('jurisdiction_specific_variables', ''):
            key_features.append('KYC/PAN')
        if 'gdprCompliant' in legal_rules.get('jurisdiction_specific_variables', ''):
            key_features.append('GDPR')
        if 'secRegistered' in legal_rules.get('jurisdiction_specific_variables', ''):
            key_features.append('SEC')
        
        print(f"{jurisdiction.upper():<12} {'Multiple compliance requirements':<50} {', '.join(key_features)}")
    
    print_section("Code Generation Comparison")
    for jurisdiction in jurisdictions:
        contract_def.jurisdiction = jurisdiction
        contract_code = generator.generate_contract(contract_def)
        
        # Count jurisdiction-specific elements
        jurisdiction_name = jurisdiction.upper()
        if jurisdiction == 'india':
            specific_elements = ['panNumbers', 'aadhaarNumbers', 'gstNumbers', 'RBI']
        elif jurisdiction == 'eu':
            specific_elements = ['gdprCompliant', 'psd2Compliant', 'GDPR', 'PSD2']
        else:  # us
            specific_elements = ['secRegistered', 'finraRegistered', 'SEC', 'FINRA']
        
        found_elements = sum(1 for element in specific_elements if element in contract_code)
        print(f"{jurisdiction.upper()}: {found_elements}/{len(specific_elements)} jurisdiction-specific elements")


def demo_cli_usage():
    """Demonstrate CLI usage."""
    print_header("COMMAND LINE INTERFACE DEMONSTRATION")
    
    print_section("Available Commands")
    commands = [
        ("Generate contract", "python cli/main.py generate --type escrow --jurisdiction india"),
        ("Generate from file", "python cli/main.py generate --file examples/escrow_india.yaml"),
        ("Interactive mode", "python cli/main.py generate --interactive"),
        ("Validate contract", "python cli/main.py validate --file examples/escrow_india.yaml"),
        ("List types", "python cli/main.py list-types"),
        ("List jurisdictions", "python cli/main.py list-jurisdictions"),
        ("Deploy contract", "python cli/main.py deploy --contract generated_contracts/escrow_india.sol")
    ]
    
    for description, command in commands:
        print(f"  {description}:")
        print(f"    {command}")
    
    print_section("Example Workflow")
    workflow = [
        "1. Define contract in YAML format",
        "2. Validate contract definition",
        "3. Generate jurisdiction-specific Solidity code",
        "4. Review generated contract",
        "5. Deploy to local testnet (Ganache)",
        "6. Test contract functionality",
        "7. Deploy to public testnet (Sepolia)",
        "8. Verify contract on Etherscan"
    ]
    
    for step in workflow:
        print(f"  {step}")


def main():
    """Run the complete demonstration."""
    print("🚀 Jurisdiction-Specific Smart Contract Generator Demo")
    print("This demonstration shows the complete workflow from DSL parsing to contract deployment.")
    
    try:
        # Demo 1: DSL Parsing
        contract_def = demo_dsl_parsing()
        
        # Demo 2: Legal Rules
        demo_legal_rules()
        
        # Demo 3: Contract Generation
        demo_contract_generation(contract_def)
        
        # Demo 4: Jurisdiction Comparison
        demo_jurisdiction_comparison()
        
        # Demo 5: CLI Usage
        demo_cli_usage()
        
        print_header("DEMONSTRATION COMPLETE")
        print("✅ All demonstrations completed successfully!")
        print("\nNext steps:")
        print("1. Run: python cli/main.py generate --interactive")
        print("2. Start Ganache: ganache-cli")
        print("3. Deploy: npx hardhat run generated_contracts/deploy_escrow_india.js")
        print("4. Test: npx hardhat test generated_contracts/test_escrow_india.js")
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 