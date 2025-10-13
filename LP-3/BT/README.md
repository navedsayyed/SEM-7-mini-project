# 🚀 Energy Trading Platform - Complete Deployment Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Smart Contract Deployment](#smart-contract-deployment)
3. [Frontend Setup](#frontend-setup)
4. [Testing the Application](#testing-the-application)
5. [Project Features](#project-features)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Required Tools:
- **MetaMask Wallet**: Browser extension for Ethereum interactions
- **Remix IDE**: Online Solidity IDE (https://remix.ethereum.org)
- **Test ETH**: Free test Ethereum for Sepolia testnet

### Getting Started:

1. **Install MetaMask**
   - Visit: https://metamask.io
   - Add to your browser (Chrome/Firefox/Edge)
   - Create a new wallet and save your seed phrase securely

2. **Get Test ETH**
   - Switch MetaMask to Sepolia Test Network
   - Get free test ETH from: https://sepoliafaucet.com
   - You'll need this for deploying and testing

---

## 🔷 Smart Contract Deployment

### Step 1: Open Remix IDE
1. Go to https://remix.ethereum.org
2. You'll see the default workspace

### Step 2: Create Contract File
1. In the File Explorer (left sidebar), click the "+" icon
2. Name it: `EnergyTrading.sol`
3. Copy the complete Solidity code from the artifact above
4. Paste it into the file

### Step 3: Compile Contract
1. Click on the "Solidity Compiler" tab (left sidebar)
2. Select compiler version: `0.8.0` or higher
3. Click "Compile EnergyTrading.sol"
4. Wait for green checkmark ✓

### Step 4: Deploy Contract
1. Click "Deploy & Run Transactions" tab (left sidebar)
2. Change ENVIRONMENT to: **"Injected Provider - MetaMask"**
3. MetaMask will pop up - connect your account
4. Ensure you're on **Sepolia Test Network**
5. Click **"Deploy"** button
6. Confirm transaction in MetaMask
7. Wait for deployment (10-30 seconds)

### Step 5: Save Contract Address
1. After deployment, expand the deployed contract
2. Copy the contract address (looks like: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`)
3. **SAVE THIS ADDRESS** - you'll need it for the frontend!

---

## 🌐 Frontend Setup

### Step 1: Download HTML File
1. Copy the complete HTML code from the "Energy Trading Platform - Web Interface" artifact
2. Save it as `index.html` on your computer

### Step 2: Update Contract Address
1. Open `index.html` in a text editor (Notepad++, VS Code, etc.)
2. Find this line (around line 395):
   ```javascript
   const CONTRACT_ADDRESS = "YOUR_CONTRACT_ADDRESS_HERE";
   ```
3. Replace `YOUR_CONTRACT_ADDRESS_HERE` with your deployed contract address
4. Save the file

### Step 3: Run the Application
1. Double-click `index.html` to open in your browser
2. Or right-click → Open with → Your preferred browser

---

## 🧪 Testing the Application

### Test Scenario 1: Connect Wallet
1. Click **"Connect Wallet"** button
2. MetaMask will ask for permission - click "Connect"
3. You should see your account address displayed
4. Stats should show 0 tokens, 0 energy, etc.

### Test Scenario 2: Get Initial Tokens
1. Click **"Get Initial Tokens (1000 ETG)"** button
2. MetaMask will pop up - confirm the transaction
3. Wait 10-20 seconds for confirmation
4. Your token balance should update to 1000 ETG

### Test Scenario 3: List Energy (Producer Role)
1. Go to **"List Energy"** tab
2. Enter:
   - Energy Amount: `100` (kWh)
   - Price per kWh: `5` (ETG tokens)
3. Click **"List Energy for Sale"**
4. Confirm transaction in MetaMask
5. Check your stats - "Listings Created" should increase

### Test Scenario 4: Buy Energy (Consumer Role)
**Note**: You need a second MetaMask account for this
1. Add a second account in MetaMask
2. Send some test ETH to this account
3. Connect with the second account
4. Get initial tokens for this account
5. Go to **"Marketplace"** tab
6. Click **"Buy Energy"** on a listing
7. Enter amount to buy (e.g., `50` kWh)
8. Confirm transaction
9. Check stats - tokens decrease, energy increases

### Test Scenario 5: View Transactions
1. Go to **"My Transactions"** tab
2. You'll see all your purchases and sales
3. Details include: energy amount, price, date, parties involved

---

## ⚡ Project Features

### Smart Contract Features:
- ✅ **Energy Listing**: Producers can list energy with custom pricing
- ✅ **Token-Based Trading**: Uses platform tokens (ETG) for transactions
- ✅ **Purchase System**: Consumers buy energy with tokens
- ✅ **Balance Tracking**: Tracks both token and energy balances
- ✅ **Transaction History**: Complete record of all trades
- ✅ **Listing Management**: Producers can cancel their listings
- ✅ **Active Listing Filter**: Only shows available energy
- ✅ **User Statistics**: Detailed stats for each user

### Frontend Features:
- 🎨 **Modern UI**: Beautiful gradient design with smooth animations
- 🔗 **MetaMask Integration**: Easy wallet connection
- 📊 **Real-Time Stats**: Live updates of balances and activity
- 🔄 **Auto-Refresh**: Updates data after transactions
- 📱 **Responsive Design**: Works on desktop and mobile
- 🛡️ **Error Handling**: User-friendly error messages
- 🎯 **Role-Based Actions**: Different views for producers/consumers

---

## 🐛 Troubleshooting

### Issue: "Contract not deployed" error
**Solution**: 
- Make sure you updated `CONTRACT_ADDRESS` in the HTML file
- Verify you're on Sepolia network in MetaMask
- Check if contract deployment was successful in Remix

### Issue: "Insufficient funds" error
**Solution**:
- Get more test ETH from Sepolia faucet
- Transactions require small gas fees

### Issue: "Tokens already received" error
**Solution**:
- You can only claim initial tokens once per address
- Use a different address if you need more tokens

### Issue: MetaMask not connecting
**Solution**:
- Refresh the page
- Disconnect and reconnect MetaMask
- Try a different browser

### Issue: Transactions not appearing
**Solution**:
- Click the "Refresh" buttons
- Wait 30 seconds for blockchain confirmation
- Check your network connection

### Issue: Can't buy own energy
**Solution**:
- This is intentional - use a second MetaMask account
- Switch accounts in MetaMask to test buying

---

## 📊 Understanding the Platform

### Token System (ETG):
- Initial allocation: 1000 ETG per user
- Used for buying/selling energy
- Transferred between users during trades

### Energy Units:
- Measured in kWh (kilowatt-hours)
- Set your own price per kWh
- Track total energy owned

### Transaction Flow:
```
Producer → Lists Energy → Marketplace
Consumer → Buys Energy → Tokens Transfer
Producer → Receives Tokens
Consumer → Receives Energy
Blockchain → Records Transaction
```

---

## 🎓 Learning Outcomes

After completing this project, you'll understand:
- ✅ Smart contract development with Solidity
- ✅ Blockchain deployment on Ethereum testnet
- ✅ Web3.js integration for dApp frontends
- ✅ MetaMask wallet interaction
- ✅ Decentralized marketplace concepts
- ✅ Token-based trading systems
- ✅ Transaction management on blockchain

---

## 🚀 Next Steps

### Enhancements you can add:
1. **Dynamic Pricing**: Implement time-based pricing
2. **Energy Types**: Solar, wind, hydro classifications
3. **Ratings System**: Rate producers/consumers
4. **Automated Matching**: Auto-match buyers with sellers
5. **Analytics Dashboard**: Charts and graphs for trading data
6. **Multi-Token Support**: Accept different cryptocurrencies
7. **Mobile App**: Create React Native mobile version

---

## 📝 Submission Checklist

For your mini project submission, include:
- ☑️ Smart contract code (EnergyTrading.sol)
- ☑️ Deployed contract address on Sepolia
- ☑️ Frontend HTML file
- ☑️ Screenshots of:
  - Deployed contract in Remix
  - Connected wallet
  - Listing creation
  - Energy purchase
  - Transaction history
- ☑️ This documentation
- ☑️ Brief explanation of blockchain concepts used

---

## 🎉 Congratulations!

You've successfully built a blockchain-based P2P energy trading platform! This demonstrates understanding of:
- Smart contracts
- Decentralized applications
- Token economics
- Peer-to-peer marketplaces

**Need help?** Review the troubleshooting section or check Ethereum documentation at https://ethereum.org/en/developers/docs/

---

## 📚 Additional Resources

- **Solidity Docs**: https://docs.soliditylang.org
- **Web3.js Docs**: https://web3js.readthedocs.io
- **Ethereum Dev**: https://ethereum.org/en/developers
- **MetaMask**: https://metamask.io

---

**Project Version**: 1.0  
**Last Updated**: October 2025  
**License**: MIT