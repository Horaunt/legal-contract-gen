#!/usr/bin/env python3
"""
Command Line Interface for Jurisdiction-Specific Smart Contract Generator
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

from dsl.parser import DSLParser, ContractDefinition, Party, Condition
from generators.code_generator import CodeGenerator
import yaml


class ContractGeneratorCLI:
    """Command Line Interface for generating jurisdiction-specific smart contracts."""
    
    def __init__(self):
        self.parser = DSLParser()
        self.generator = CodeGenerator()
        self.supported_types = ['escrow', 'insurance', 'settlement']
        self.supported_jurisdictions = ['india', 'eu', 'us']
    
    def run(self):
        """Main CLI entry point."""
        parser = argparse.ArgumentParser(
            description='Generate jurisdiction-specific smart contracts',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s generate --type escrow --jurisdiction india --output contracts/
  %(prog)s generate --file contract.yaml --output contracts/
  %(prog)s list-types
  %(prog)s list-jurisdictions
  %(prog)s validate --file contract.yaml
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Generate command
        generate_parser = subparsers.add_parser('generate', help='Generate a smart contract')
        generate_parser.add_argument('--type', choices=self.supported_types, help='Contract type')
        generate_parser.add_argument('--jurisdiction', choices=self.supported_jurisdictions, help='Jurisdiction')
        generate_parser.add_argument('--file', help='YAML contract definition file')
        generate_parser.add_argument('--output', default='contracts/', help='Output directory')
        generate_parser.add_argument('--interactive', action='store_true', help='Interactive mode')
        
        # List commands
        subparsers.add_parser('list-types', help='List supported contract types')
        subparsers.add_parser('list-jurisdictions', help='List supported jurisdictions')
        
        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate contract definition')
        validate_parser.add_argument('--file', required=True, help='YAML contract definition file')
        
        # Deploy command
        deploy_parser = subparsers.add_parser('deploy', help='Deploy generated contract')
        deploy_parser.add_argument('--contract', required=True, help='Contract file to deploy')
        deploy_parser.add_argument('--network', default='localhost:8545', help='Ethereum network')
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        try:
            if args.command == 'generate':
                self.handle_generate(args)
            elif args.command == 'list-types':
                self.list_types()
            elif args.command == 'list-jurisdictions':
                self.list_jurisdictions()
            elif args.command == 'validate':
                self.validate_contract(args.file)
            elif args.command == 'deploy':
                self.deploy_contract(args.contract, args.network)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def handle_generate(self, args):
        """Handle contract generation."""
        if args.interactive:
            contract_def = self.interactive_contract_definition()
        elif args.file:
            contract_def = self.parser.parse_file(args.file)
        elif args.type and args.jurisdiction:
            contract_def = self.create_basic_contract(args.type, args.jurisdiction)
        else:
            print("Error: Must specify either --file, --type+--jurisdiction, or --interactive")
            return
        
        # Validate contract
        errors = self.parser.validate_contract(contract_def)
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"  - {error}")
            return
        
        # Generate contract
        print(f"Generating {contract_def.contract_type} contract for {contract_def.jurisdiction}...")
        
        contract_code = self.generator.generate_contract(contract_def)
        output_path = self.generator.save_contract(contract_code, contract_def)
        
        print(f"Contract generated successfully: {output_path}")
        
        # Generate additional files
        deployment_script = self.generator.create_deployment_script(contract_def)
        test_script = self.generator.create_test_script(contract_def)
        
        print(f"Deployment script: {deployment_script}")
        print(f"Test script: {test_script}")
    
    def interactive_contract_definition(self) -> ContractDefinition:
        """Interactive contract definition creation."""
        print("=== Interactive Contract Definition ===")
        
        # Contract type
        print("\nAvailable contract types:")
        for i, contract_type in enumerate(self.supported_types, 1):
            print(f"  {i}. {contract_type}")
        
        while True:
            try:
                choice = int(input(f"\nSelect contract type (1-{len(self.supported_types)}): ")) - 1
                if 0 <= choice < len(self.supported_types):
                    contract_type = self.supported_types[choice]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
        
        # Jurisdiction
        print("\nAvailable jurisdictions:")
        for i, jurisdiction in enumerate(self.supported_jurisdictions, 1):
            print(f"  {i}. {jurisdiction}")
        
        while True:
            try:
                choice = int(input(f"\nSelect jurisdiction (1-{len(self.supported_jurisdictions)}): ")) - 1
                if 0 <= choice < len(self.supported_jurisdictions):
                    jurisdiction = self.supported_jurisdictions[choice]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
        
        # Parties
        parties = []
        print(f"\nDefine parties for {contract_type} contract:")
        
        if contract_type == 'escrow':
            party_roles = ['payer', 'payee']
        elif contract_type == 'insurance':
            party_roles = ['insurer', 'insured']
        elif contract_type == 'settlement':
            party_roles = ['plaintiff', 'defendant']
        
        for role in party_roles:
            name = input(f"Enter {role} name: ")
            address = input(f"Enter {role} address (optional): ") or None
            parties.append(Party(name=name, role=role, address=address))
        
        # Conditions
        conditions = []
        print(f"\nDefine conditions for {contract_type} contract:")
        
        while True:
            add_condition = input("Add a condition? (y/n): ").lower()
            if add_condition != 'y':
                break
            
            trigger = input("Enter trigger event: ")
            action = input("Enter action: ")
            time_limit = input("Enter time limit in days (optional): ")
            
            condition = Condition(
                trigger=trigger,
                action=action,
                time_limit=int(time_limit) if time_limit else None
            )
            conditions.append(condition)
        
        # Legal requirements
        legal_requirements = []
        print(f"\nLegal requirements for {jurisdiction}:")
        
        # Load legal rules to show available requirements
        from dsl.parser import load_legal_rules
        legal_rules = load_legal_rules(jurisdiction)
        contract_rules = legal_rules['contract_types'].get(contract_type, {})
        available_requirements = contract_rules.get('legal_requirements', [])
        
        print("Available legal requirements:")
        for req in available_requirements:
            print(f"  - {req}")
        
        while True:
            requirement = input("Add legal requirement (or press Enter to finish): ")
            if not requirement:
                break
            if requirement in available_requirements:
                legal_requirements.append(requirement)
            else:
                print("Invalid requirement. Please choose from the list above.")
        
        return ContractDefinition(
            contract_type=contract_type,
            jurisdiction=jurisdiction,
            parties=parties,
            conditions=conditions,
            legal_requirements=legal_requirements,
            metadata={}
        )
    
    def create_basic_contract(self, contract_type: str, jurisdiction: str) -> ContractDefinition:
        """Create a basic contract definition."""
        if contract_type == 'escrow':
            parties = [
                Party(name="Buyer", role="payer"),
                Party(name="Seller", role="payee")
            ]
            conditions = [
                Condition(trigger="delivery_confirmed", action="release_funds")
            ]
        elif contract_type == 'insurance':
            parties = [
                Party(name="Insurance Company", role="insurer"),
                Party(name="Policy Holder", role="insured")
            ]
            conditions = [
                Condition(trigger="claim_submitted", action="process_claim")
            ]
        elif contract_type == 'settlement':
            parties = [
                Party(name="Plaintiff", role="plaintiff"),
                Party(name="Defendant", role="defendant")
            ]
            conditions = [
                Condition(trigger="agreement_reached", action="execute_settlement")
            ]
        
        return ContractDefinition(
            contract_type=contract_type,
            jurisdiction=jurisdiction,
            parties=parties,
            conditions=conditions,
            legal_requirements=[],
            metadata={}
        )
    
    def list_types(self):
        """List supported contract types."""
        print("Supported contract types:")
        for contract_type in self.supported_types:
            print(f"  - {contract_type}")
    
    def list_jurisdictions(self):
        """List supported jurisdictions."""
        print("Supported jurisdictions:")
        for jurisdiction in self.supported_jurisdictions:
            print(f"  - {jurisdiction}")
    
    def validate_contract(self, file_path: str):
        """Validate a contract definition file."""
        try:
            contract_def = self.parser.parse_file(file_path)
            errors = self.parser.validate_contract(contract_def)
            
            if errors:
                print("Validation errors:")
                for error in errors:
                    print(f"  - {error}")
            else:
                print("Contract definition is valid!")
                print(f"Type: {contract_def.contract_type}")
                print(f"Jurisdiction: {contract_def.jurisdiction}")
                print(f"Parties: {len(contract_def.parties)}")
                print(f"Conditions: {len(contract_def.conditions)}")
        
        except Exception as e:
            print(f"Validation failed: {e}")
    
    def deploy_contract(self, contract_file: str, network: str):
        """Deploy a generated contract."""
        print(f"Deploying contract {contract_file} to {network}...")
        
        # This would integrate with a deployment framework like Hardhat or Truffle
        # For now, just show the deployment command
        print(f"To deploy manually, run:")
        print(f"npx hardhat run {contract_file} --network {network}")
        print(f"or")
        print(f"truffle migrate --network {network}")


def main():
    """Main entry point."""
    cli = ContractGeneratorCLI()
    cli.run()


if __name__ == '__main__':
    main() 