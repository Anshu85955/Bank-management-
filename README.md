# 🏦 Bank Management System

A comprehensive Python-based bank management system with both command-line interface (CLI) and web-based Streamlit GUI. This system allows users to create accounts, manage deposits/withdrawals, and perform various banking operations with secure PIN authentication.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Security Features](#security-features)
- [Data Storage](#data-storage)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Banking Operations
- **Account Creation**: Create new bank accounts with validation
- **Money Deposit**: Deposit funds with daily limits
- **Money Withdrawal**: Withdraw funds with balance verification
- **Account Details**: View complete account information
- **Update Profile**: Modify account details (name, email, PIN)
- **Account Deletion**: Securely delete accounts with confirmation

### Security Features
- **PIN Authentication**: 4-digit PIN protection for all operations
- **Age Verification**: Minimum age requirement (18 years)
- **Account Number Generation**: Random secure account numbers
- **Transaction Limits**: Daily deposit/withdrawal limits
- **Data Persistence**: JSON-based secure data storage

### User Interfaces
- **Command Line Interface**: Traditional CLI for power users
- **Streamlit Web App**: Modern web-based GUI with interactive forms
- **Real-time Validation**: Input validation and error handling

## 📁 Project Structure

```
Bank-management-/
├── README.md                 # Project documentation
├── main.py                  # CLI version of the application
├── bank_app.py             # Streamlit web application
├── chat.py                 # Alternative Streamlit implementation
├── data.json               # Database file (auto-generated)
├── main copy.py            # Backup CLI version
└── main copy 2.py          # Development version
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Required Dependencies
```bash
pip install streamlit
```

### Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Bank-management-
   ```

2. **Install dependencies**:
   ```bash
   pip install streamlit
   ```

3. **Run the application**:
   
   **For Web Interface (Recommended)**:
   ```bash
   streamlit run bank_app.py
   ```
   
   **For Command Line Interface**:
   ```bash
   python main.py
   ```

## 💻 Usage

### Web Interface (Streamlit)

1. **Start the application**:
   ```bash
   streamlit run bank_app.py
   ```

2. **Navigate to**: `http://localhost:8501`

3. **Select operations** from the sidebar:
   - Create Account
   - Deposit Money
   - Withdraw Money
   - Show Details
   - Update Details
   - Delete Account

### Command Line Interface

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Select from menu options**:
   ```
   Press 1 for creating your account
   Press 2 for deposit money in the Bank
   Press 3 for withdrawing your money
   Press 4 for details
   Press 5 for updating the details
   Press 6 for deleting your account
   ```

## 📚 API Documentation

### Bank Class Methods

#### `create_account(name, age, email, mob, pin)`
Creates a new bank account with validation.

**Parameters:**
- `name` (str): Account holder's name
- `age` (int): Account holder's age (must be ≥18)
- `email` (str): Email address
- `mob` (str): Mobile number
- `pin` (int): 4-digit PIN

**Returns:** Success/failure message with account number

#### `deposit(accnumber, pin, amount)`
Deposits money into an account.

**Parameters:**
- `accnumber` (str): Account number
- `pin` (int): Account PIN
- `amount` (int): Deposit amount (1-10000)

**Returns:** Transaction confirmation message

#### `withdraw(accnumber, pin, amount)`
Withdraws money from an account.

**Parameters:**
- `accnumber` (str): Account number
- `pin` (int): Account PIN
- `amount` (int): Withdrawal amount

**Returns:** Transaction confirmation message

#### `show_details(accnumber, pin)`
Retrieves account information.

**Parameters:**
- `accnumber` (str): Account number
- `pin` (int): Account PIN

**Returns:** Account details dictionary or None

#### `update_details(accnumber, pin, new_name, new_email, new_pin)`
Updates account information.

**Parameters:**
- `accnumber` (str): Account number
- `pin` (int): Current PIN
- `new_name` (str, optional): New name
- `new_email` (str, optional): New email
- `new_pin` (str, optional): New PIN

**Returns:** Update confirmation message

#### `delete(accnumber, pin)`
Deletes an account permanently.

**Parameters:**
- `accnumber` (str): Account number
- `pin` (int): Account PIN

**Returns:** Deletion confirmation message

## 🔐 Security Features

### Account Security
- **PIN Protection**: All operations require 4-digit PIN verification
- **Age Verification**: Minimum age requirement of 18 years
- **Secure Account Numbers**: Randomly generated alphanumeric account numbers

### Transaction Security
- **Amount Limits**: Deposit/withdrawal limits (₹1 - ₹10,000)
- **Balance Verification**: Prevents overdrafts
- **Input Validation**: Comprehensive input sanitization

### Data Security
- **JSON Encryption**: Account data stored in structured JSON format
- **Error Handling**: Graceful handling of file I/O operations
- **Data Persistence**: Automatic saving after each transaction

## 💾 Data Storage

### Database Structure
The system uses a JSON file (`data.json`) to store account information:

```json
[
    {
        "name": "John Doe",
        "age": 25,
        "email": "john@example.com",
        "Mob_no": "9876543210",
        "pin": 1234,
        "accountNo": "A1B2C3D4",
        "balance": 5000
    }
]
```

### Data Fields
- **name**: Account holder's full name
- **age**: Account holder's age
- **email**: Contact email address
- **Mob_no**: Mobile phone number
- **pin**: 4-digit security PIN
- **accountNo**: Unique account identifier
- **balance**: Current account balance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Email: [surajk86808@gmail.com]

## 🔄 Version History

- **v1.0.0** - Initial release with CLI interface
- **v2.0.0** - Added Streamlit web interface
- **v2.1.0** - Enhanced security and validation

---

**Note**: This system is designed for educational purposes. For production use, implement proper encryption, database management, and additional security measures.
