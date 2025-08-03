# Setup Guide for Jurisdiction-Specific Smart Contract Generator

This guide will help you set up and use the jurisdiction-specific smart contract generator.

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Horaunt/legal-contract-gen
cd jurisdiction-smart-contract-generator
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies

```bash
npm install
```

### 4. Install Ganache CLI (for local testing)

```bash
npm install -g ganache-cli
```

## Project Structure

```
jurisdiction-smart-contract-generator/
├── legal_rules/           # Legal requirements per jurisdiction
│   └── jurisdictions.yaml
├── dsl/                   # Domain Specific Language parser
│   └── parser.py
├── templates/             # Solidity contract templates
│   ├── base_contract.sol
│   └── india_escrow.sol
├── generators/            # Code generation logic
│   └── code_generator.py
├── cli/                   # Command line interface
│   └── main.py
├── tests/                 # Test files
│   ├── test_dsl_parser.py
│   └── test_code_generator.py
├── examples/              # Example contract definitions
│   ├── escrow_india.yaml
│   └── insurance_eu.yaml
├── generated_contracts/   # Generated Solidity contracts
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies
└── README.md
```

## Quick Start

### 1. Generate a Basic Contract

Generate an escrow contract for India:

```bash
python cli/main.py generate --type escrow --jurisdiction india
```

### 2. Generate from YAML Definition

```bash
python cli/main.py generate --file examples/escrow_india.yaml
```

### 3. Interactive Mode

```bash
python cli/main.py generate --interactive
```

### 4. Validate a Contract Definition

```bash
python cli/main.py validate --file examples/escrow_india.yaml
```

## Usage Examples

### Example 1: Generate India Escrow Contract

```bash
# Generate the contract
python cli/main.py generate --type escrow --jurisdiction india

# This will create:
# - generated_contracts/escrow_india.sol
# - generated_contracts/deploy_escrow_india.js
# - generated_contracts/test_escrow_india.js
```

### Example 2: Generate EU Insurance Contract

```bash
# Generate the contract
python cli/main.py generate --type insurance --jurisdiction eu

# This will create:
# - generated_contracts/insurance_eu.sol
# - generated_contracts/deploy_insurance_eu.js
# - generated_contracts/test_insurance_eu.js
```

### Example 3: Generate US Settlement Contract

```bash
# Generate the contract
python cli/main.py generate --type settlement --jurisdiction us

# This will create:
# - generated_contracts/settlement_us.sol
# - generated_contracts/deploy_settlement_us.js
# - generated_contracts/test_settlement_us.js
```

## Testing

### Run Python Tests

```bash
pytest tests/
```

### Run Specific Test Files

```bash
pytest tests/test_dsl_parser.py
pytest tests/test_code_generator.py
```

### Test Contract Generation

```bash
# Test DSL parsing
python cli/main.py validate --file examples/escrow_india.yaml

# Test contract generation
python cli/main.py generate --file examples/escrow_india.yaml
```

## Deployment

### 1. Start Local Ethereum Network

```bash
ganache-cli
```

### 2. Deploy Generated Contract

```bash
# Deploy to local network
npx hardhat run generated_contracts/deploy_escrow_india.js --network localhost

# Deploy to testnet (e.g., Sepolia)
npx hardhat run generated_contracts/deploy_escrow_india.js --network sepolia
```

### 3. Verify Contract on Etherscan

```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

## Configuration

### Legal Rules Configuration

Edit `legal_rules/jurisdictions.yaml` to modify legal requirements:

```yaml
jurisdictions:
  india:
    contract_types:
      escrow:
        legal_requirements:
          - "kyc_verification"
          - "gst_compliance"
        mandatory_clauses:
          - "kyc_verification_clause"
        time_limits:
          dispute_resolution_days: 30
```

### Template Customization

Modify templates in `templates/` directory:

- `base_contract.sol`: Base contract template
- `india_escrow.sol`: India-specific escrow template
- Add new templates for other jurisdictions/contract types

## Supported Jurisdictions

### India
- **Regulatory Bodies**: RBI, SEBI, IRDAI
- **Legal Requirements**: KYC, GST, PAN, Aadhaar
- **Contract Types**: Escrow, Insurance, Settlement

### European Union
- **Regulatory Bodies**: ESMA, EBA, EIOPA
- **Legal Requirements**: GDPR, PSD2, MiCA
- **Contract Types**: Escrow, Insurance, Settlement

### United States
- **Regulatory Bodies**: SEC, CFTC, FINRA
- **Legal Requirements**: SEC registration, AML/KYC, UCC
- **Contract Types**: Escrow, Insurance, Settlement

## Supported Contract Types

### Escrow Contracts
- Secure payment holding with conditional release
- Jurisdiction-specific compliance requirements
- Automated dispute resolution

### Insurance Contracts
- Automated claims processing and payout
- Regulatory compliance verification
- Policy management

### Settlement Contracts
- Dispute resolution and automated settlements
- Court approval requirements
- Jurisdiction-specific legal frameworks

## DSL Syntax

### Basic Contract Definition

```yaml
contract:
  type: escrow
  jurisdiction: india
  parties:
    - name: "Buyer"
      role: "payer"
      address: "0x1234..."
    - name: "Seller"
      role: "payee"
      address: "0x5678..."
  conditions:
    - trigger: "delivery_confirmed"
      action: "release_funds"
      time_limit: 7
  legal_requirements:
    - "kyc_verification"
    - "gst_compliance"
  metadata:
    version: "1.0.0"
    description: "India-compliant escrow contract"
```

### Condition Parameters

```yaml
conditions:
  - trigger: "dispute_raised"
    action: "freeze_funds"
    time_limit: 30
    parameters:
      dispute_resolution_authority: "rbi"
      cooling_off_period: 7
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the project root directory
2. **Template Not Found**: Check that template files exist in `templates/`
3. **Legal Rules Not Found**: Verify `legal_rules/jurisdictions.yaml` exists
4. **Deployment Fails**: Ensure Ganache is running and network is accessible

### Debug Mode

Run with verbose output:

```bash
python cli/main.py generate --type escrow --jurisdiction india --verbose
```

### Log Files

Check generated log files in `logs/` directory for detailed error information.

## Contributing

### Adding New Jurisdictions

1. Add jurisdiction rules to `legal_rules/jurisdictions.yaml`
2. Create jurisdiction-specific template in `templates/`
3. Add jurisdiction-specific code in `generators/code_generator.py`
4. Add tests in `tests/`

### Adding New Contract Types

1. Add contract type rules to legal rules
2. Create contract type template
3. Update DSL parser validation
4. Add tests

### Code Style

```bash
# Format Python code
black .

# Lint Python code
flake8 .

# Type checking
mypy .
```


## Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing issues on GitHub
3. Create a new issue with detailed information
4. Contact the development team

## Roadmap

- [ ] Add more jurisdictions (UK, Singapore, Australia)
- [ ] Support for more contract types (derivatives, bonds)
- [ ] Web UI for contract generation
- [ ] Integration with legal compliance APIs
- [ ] Automated legal compliance verification
- [ ] Multi-language support (Spanish, French, German)
- [ ] Blockchain network support (Polygon, BSC, Arbitrum) 