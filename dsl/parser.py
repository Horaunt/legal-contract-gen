import yaml
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Party:
    name: str
    role: str
    address: Optional[str] = None
    verification_required: bool = True


@dataclass
class Condition:
    trigger: str
    action: str
    parameters: Optional[Dict[str, Any]] = None
    time_limit: Optional[int] = None


@dataclass
class ContractDefinition:
    contract_type: str
    jurisdiction: str
    parties: List[Party]
    conditions: List[Condition]
    legal_requirements: List[str]
    metadata: Dict[str, Any]


class DSLParser:
    """Parser for the Domain Specific Language used to define smart contracts."""
    
    def __init__(self):
        self.supported_types = ['escrow', 'insurance', 'settlement']
        self.supported_jurisdictions = ['india', 'eu', 'us']
    
    def parse_file(self, file_path: str) -> ContractDefinition:
        """Parse a YAML file containing contract definition."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file)
        return self.parse_content(content)
    
    def parse_content(self, content: Dict[str, Any]) -> ContractDefinition:
        """Parse contract definition from dictionary content."""
        if 'contract' not in content:
            raise ValueError("Contract definition must contain 'contract' key")
        
        contract_data = content['contract']
        
        # Validate contract type
        contract_type = contract_data.get('type', '').lower()
        if contract_type not in self.supported_types:
            raise ValueError(f"Unsupported contract type: {contract_type}")
        
        # Validate jurisdiction
        jurisdiction = contract_data.get('jurisdiction', '').lower()
        if jurisdiction not in self.supported_jurisdictions:
            raise ValueError(f"Unsupported jurisdiction: {jurisdiction}")
        
        # Parse parties
        parties = []
        for party_data in contract_data.get('parties', []):
            party = Party(
                name=party_data['name'],
                role=party_data['role'],
                address=party_data.get('address'),
                verification_required=party_data.get('verification_required', True)
            )
            parties.append(party)
        
        # Parse conditions
        conditions = []
        for condition_data in contract_data.get('conditions', []):
            condition = Condition(
                trigger=condition_data['trigger'],
                action=condition_data['action'],
                parameters=condition_data.get('parameters'),
                time_limit=condition_data.get('time_limit')
            )
            conditions.append(condition)
        
        # Get legal requirements
        legal_requirements = contract_data.get('legal_requirements', [])
        
        # Get metadata
        metadata = contract_data.get('metadata', {})
        
        return ContractDefinition(
            contract_type=contract_type,
            jurisdiction=jurisdiction,
            parties=parties,
            conditions=conditions,
            legal_requirements=legal_requirements,
            metadata=metadata
        )
    
    def validate_contract(self, contract_def: ContractDefinition) -> List[str]:
        """Validate contract definition and return list of errors."""
        errors = []
        
        # Check if contract has at least two parties
        if len(contract_def.parties) < 2:
            errors.append("Contract must have at least two parties")
        
        # Check if contract has at least one condition
        if len(contract_def.conditions) == 0:
            errors.append("Contract must have at least one condition")
        
        # Validate party roles based on contract type
        if contract_def.contract_type == 'escrow':
            roles = [party.role for party in contract_def.parties]
            if 'payer' not in roles or 'payee' not in roles:
                errors.append("Escrow contract must have 'payer' and 'payee' roles")
        
        elif contract_def.contract_type == 'insurance':
            roles = [party.role for party in contract_def.parties]
            if 'insurer' not in roles or 'insured' not in roles:
                errors.append("Insurance contract must have 'insurer' and 'insured' roles")
        
        elif contract_def.contract_type == 'settlement':
            roles = [party.role for party in contract_def.parties]
            if 'plaintiff' not in roles or 'defendant' not in roles:
                errors.append("Settlement contract must have 'plaintiff' and 'defendant' roles")
        
        return errors
    
    def to_json(self, contract_def: ContractDefinition) -> str:
        """Convert contract definition to JSON format."""
        data = {
            'contract_type': contract_def.contract_type,
            'jurisdiction': contract_def.jurisdiction,
            'parties': [
                {
                    'name': party.name,
                    'role': party.role,
                    'address': party.address,
                    'verification_required': party.verification_required
                }
                for party in contract_def.parties
            ],
            'conditions': [
                {
                    'trigger': condition.trigger,
                    'action': condition.action,
                    'parameters': condition.parameters,
                    'time_limit': condition.time_limit
                }
                for condition in contract_def.conditions
            ],
            'legal_requirements': contract_def.legal_requirements,
            'metadata': contract_def.metadata
        }
        return json.dumps(data, indent=2)


def load_legal_rules(jurisdiction: str) -> Dict[str, Any]:
    """Load legal rules for a specific jurisdiction."""
    rules_file = Path(__file__).parent.parent / 'legal_rules' / 'jurisdictions.yaml'
    with open(rules_file, 'r', encoding='utf-8') as file:
        rules = yaml.safe_load(file)
    
    if jurisdiction not in rules['jurisdictions']:
        raise ValueError(f"Jurisdiction {jurisdiction} not found in legal rules")
    
    return rules['jurisdictions'][jurisdiction] 