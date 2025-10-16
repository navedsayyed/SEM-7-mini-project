# 🧪 Energy Trading Platform - Testing Guide

## 📋 Quick Start Testing Guide

This guide will walk you through testing all features of the Energy Trading Platform smart contract using Remix IDE.

---

## ✅ Prerequisites

Before testing, make sure you have:
- ✅ Deployed the `EnergyTradingPlatform` contract in Remix
- ✅ Contract is visible under "Deployed Contracts" section
- ✅ At least 2 accounts available in Remix (for testing buyer/seller interaction)

---

## 🧪 TEST 1: Register & Get Initial Tokens

### Purpose: Set up your account and get starting tokens (1000 ETG)

**Steps:**

1. **Register Your Account**
   - Find the orange button **`register`**
   - Click it
   - ✅ You're now registered!

2. **Get Your Initial Tokens (Money)**
   - Find the orange button **`getTokens`**
   - Click it
   - ✅ You now have 1000 tokens (1000000000000000000000 wei)

3. **Verify Token Balance**
   - Find the blue button **`tokenBalance`**
   - Click dropdown (▼)
   - Paste your account address (shown at top: `0x5B3...eddC4`)
   - Click **"call"**
   - **Expected Result:** `1000000000000000000000`

---

## 🌞 TEST 2: List Energy for Sale (Producer Role)

### Purpose: Create an energy listing to sell to others

**Steps:**

1. **Create Energy Listing**
   - Find the orange button **`listEnergy`**
   - Click the dropdown arrow (▼)
   - Fill in the following values:

   ```
   _amount: 100              (100 kWh of energy)
   _price: 1000000000000000  (Price per unit in wei)
   _type: 0                  (0=SOLAR, 1=WIND, 2=HYDRO, 3=BIOMASS, 4=GEOTHERMAL)
   _minPurchase: 10          (Minimum 10 kWh per purchase)
   _carbonOffset: 500        (Carbon credits)
   ```

2. Click **"transact"**
3. ✅ Your energy is now listed for sale!

**Verify Listing Created:**

1. Find the blue button **`getActiveListings`**
2. Click **"call"**
3. **Expected Result:** `[0]` (means listing ID 0 exists)

**Check Listing Details:**

1. Find the blue button **`getListingDetails`**
2. Click dropdown (▼)
3. Enter: `_listingId: 0`
4. Click **"call"**
5. You'll see all listing information (producer, amount, price, type, etc.)

---

## 💰 TEST 3: Buy Energy (Consumer Role)

### Purpose: Switch to a different account and purchase energy

**Steps:**

1. **Switch Account**
   - At the very top of Remix, find **"ACCOUNT"** dropdown
   - Select the **2nd account** (different address)
   - ⚠️ Important: You're now a different user!

2. **Register New User**
   - Find the orange button **`register`**
   - Click it
   - ✅ New account registered

3. **Get Tokens for New User**
   - Find the orange button **`getTokens`**
   - Click it
   - ✅ This account now has 1000 tokens

4. **Purchase Energy**
   - Find the orange button **`buyEnergy`**
   - Click dropdown (▼)
   - Fill in:
   ```
   _listingId: 0    (The listing we created earlier)
   _amount: 50      (Buy 50 kWh)
   ```
   - Click **"transact"**
   - ✅ You bought 50 energy units!

**Verify Purchase:**

1. Find the blue button **`energyBalance`**
2. Click dropdown (▼)
3. Paste your **current account address** (Account 2)
4. Click **"call"**
5. **Expected Result:** `50`

**Check Token Balance After Purchase:**

1. Find the blue button **`tokenBalance`**
2. Click dropdown (▼)
3. Paste your current address
4. Click **"call"**
5. **Expected Result:** Less than 1000 (you paid for energy + 2% platform fee)

---

## 📊 TEST 4: Check User Statistics

### Purpose: View comprehensive user statistics

**Steps:**

1. Find the blue button **`getUserStats`**
2. Click dropdown (▼)
3. Paste your current address
4. Click **"call"**

**You'll See:**

| Field | Description |
|-------|-------------|
| `tokens` | Your remaining token balance |
| `energy` | Total energy units you own |
| `reputation` | Your reputation score (0-100) |
| `carbonCredits` | Environmental credits earned |
| `level` | Verification level (0=Unverified, 1=Basic, 2=Verified, 3=Certified) |

---

## 🔓 TEST 5: Release Escrow Payment

### Purpose: Release payment from escrow to seller after successful transaction

**Steps:**

1. Find the orange button **`releaseEscrow`**
2. Click dropdown (▼)
3. Enter: `_escrowId: 0`
4. Click **"transact"**
5. ✅ Seller receives payment!

**Verify Payment Released:**

1. **Switch back to Account 1** (the seller)
2. Find the blue button **`tokenBalance`**
3. Paste Account 1 address
4. Click **"call"**
5. **Expected Result:** Balance increased (original 1000 + payment from sale)

---

## 🔍 TEST 6: View Transactions

### Purpose: See all your transaction history

**Steps:**

1. Find the blue button **`getUserTransactions`**
2. Click dropdown (▼)
3. Paste your address (works for either buyer or seller)
4. Click **"call"**
5. **Expected Result:** `[0]` (transaction ID 0)

**Get Transaction Details:**

1. Find the blue button **`getTransactionDetails`**
2. Click dropdown (▼)
3. Enter: `_txId: 0`
4. Click **"call"**

**You'll See:**
- Producer address
- Consumer address
- Energy amount
- Total price paid
- Timestamp
- Energy type
- Dispute status

---

## 🎯 TEST 7: Advanced Features

### A. Cancel a Listing

1. **Switch to producer account** (Account 1)
2. Find orange button **`cancelListing`**
3. Enter: `_listingId: 0`
4. Click **"transact"**
5. ✅ Listing cancelled!

### B. Update Listing Price

1. Find orange button **`updatePrice`**
2. Fill in:
   ```
   _listingId: 0
   _newPrice: 2000000000000000
   ```
3. Click **"transact"**
4. ✅ Price updated!

### C. Get Listings by Energy Type

1. Find blue button **`getListingsByType`**
2. Enter: `_type: 0` (0=SOLAR)
3. Click **"call"**
4. **Result:** All active solar energy listings

### D. Check User Escrows

1. Find blue button **`getUserEscrows`**
2. Paste your address
3. Click **"call"**
4. **Result:** All your escrow IDs

---

## ⚠️ TEST 8: Error Handling

### Test Error Messages:

1. **Try to get tokens twice:**
   - Click **`getTokens`** again
   - **Expected Error:** "Tokens already claimed"

2. **Try to buy your own energy:**
   - As Account 1, try to **`buyEnergy`** from your own listing
   - **Expected Error:** "Cannot buy own energy"

3. **Try to buy more than available:**
   - Try **`buyEnergy`** with amount > listing amount
   - **Expected Error:** "Insufficient energy available"

4. **Try actions without registering:**
   - Use Account 3 (unregistered)
   - Try **`getTokens`**
   - **Expected Error:** "Not registered"

---

## 🎯 TEST 9: Dispute System (Owner Only)

### Raise a Dispute:

1. Switch to **buyer or seller account**
2. Find orange button **`raiseDispute`**
3. Enter: `_txId: 0`
4. Click **"transact"**
5. ✅ Dispute raised!

### Resolve Dispute (Owner Only):

1. **Switch to contract owner account** (Account that deployed contract)
2. Find orange button **`resolveDispute`**
3. Fill in:
   ```
   _txId: 0
   _refund: true   (true = refund buyer, false = pay seller)
   ```
4. Click **"transact"**
5. ✅ Dispute resolved!

---

## 👑 TEST 10: Owner Functions

### Only contract deployer can do these:

### A. Verify a User

```
verifyUser:
  _user: [user address]
  _level: 2  (0=Unverified, 1=Basic, 2=Verified, 3=Certified)
```

### B. Blacklist a User

```
blacklistUser:
  _user: [user address]
  _status: true  (true = blacklist, false = remove from blacklist)
```

### C. Withdraw Platform Fees

```
withdrawFees:
  (no parameters - just click)
```

---

## 📈 Complete Testing Flow

**Full End-to-End Test:**

```
1. Account 1: register() → getTokens() → listEnergy(100, price, 0, 10, 500)
2. Check: getActiveListings() → [0]
3. Account 2: register() → getTokens()
4. Account 2: buyEnergy(0, 50)
5. Check: energyBalance(Account2) → 50
6. Check: getUserStats(Account2) → see all stats
7. Account 2: releaseEscrow(0)
8. Check: tokenBalance(Account1) → increased
9. Check: getUserTransactions(Account1) → [0]
10. Check: getUserTransactions(Account2) → [0]
```

---

## 🔢 Understanding Wei Values

**Common Conversions:**

| Description | Wei Value | Human Readable |
|-------------|-----------|----------------|
| 1000 tokens | `1000000000000000000000` | 1000 ETG |
| 1 token/kWh | `1000000000000000` | 1 ETG/kWh |
| 0.001 tokens | `1000000000000000` | Min price |
| 100 tokens | `100000000000000000000` | Max price |

---

## 🎯 Energy Type Reference

```
0 = SOLAR
1 = WIND
2 = HYDRO
3 = BIOMASS
4 = GEOTHERMAL
```

---

## ✅ Testing Checklist

- [ ] Register account
- [ ] Get initial tokens (1000 ETG)
- [ ] List energy for sale
- [ ] Verify listing appears in active listings
- [ ] Switch to second account
- [ ] Register second account
- [ ] Get tokens for second account
- [ ] Buy energy from listing
- [ ] Verify energy balance updated
- [ ] Check token balance decreased
- [ ] View user statistics
- [ ] Release escrow payment
- [ ] Verify seller received payment
- [ ] View transaction history
- [ ] Test error cases
- [ ] (Optional) Test dispute system
- [ ] (Optional) Test owner functions

---

## 🐛 Common Issues & Solutions

### Issue: "Transaction failed"
**Solution:** Make sure you have enough test ETH for gas fees

### Issue: "Not registered"
**Solution:** Call `register()` function first

### Issue: "Tokens already claimed"
**Solution:** Each account can only claim tokens once. Use a different account.

### Issue: "Cannot buy own energy"
**Solution:** Switch to a different account to test buying

### Issue: "Insufficient tokens"
**Solution:** Make sure buyer has enough tokens (call `getTokens()` first)

### Issue: Button not showing
**Solution:** 
- Orange buttons = State-changing functions (write)
- Blue buttons = View functions (read)

---

## 📝 Notes

- **Gas Fees:** All transactions require small amount of test ETH for gas
- **Escrow Period:** Payments held in escrow for 7 days (can be released early by buyer)
- **Platform Fee:** 2% fee on all transactions goes to platform
- **Listing Expiry:** Listings expire after 30 days
- **Reputation:** Score increases with successful trades, decreases with disputes

---

## 🎉 Success!

If you completed all tests successfully, you've:
- ✅ Registered users
- ✅ Created energy listings
- ✅ Bought and sold energy
- ✅ Used escrow system
- ✅ Tracked transactions
- ✅ Understood the complete platform workflow

---

**Happy Testing! 🚀**

For full deployment guide, see [README.md](./README.md)
