// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyTrading {
    
    // Energy listing structure
    struct EnergyListing {
        uint256 id;
        address producer;
        uint256 energyAmount; // in kWh
        uint256 pricePerUnit; // in wei per kWh
        bool isActive;
        uint256 timestamp;
    }
    
    // Transaction record structure
    struct Transaction {
        uint256 id;
        uint256 listingId;
        address producer;
        address consumer;
        uint256 energyAmount;
        uint256 totalPrice;
        uint256 timestamp;
    }
    
    // State variables
    mapping(uint256 => EnergyListing) public energyListings;
    mapping(uint256 => Transaction) public transactions;
    mapping(address => uint256) public energyBalance; // Track energy owned
    mapping(address => uint256) public tokenBalance; // Track platform tokens
    
    uint256 public listingCount;
    uint256 public transactionCount;
    uint256 public constant INITIAL_TOKENS = 1000 ether; // Initial tokens for new users
    
    // Events
    event EnergyListed(uint256 indexed listingId, address indexed producer, uint256 amount, uint256 price);
    event EnergyPurchased(uint256 indexed transactionId, uint256 indexed listingId, address indexed consumer, uint256 amount);
    event ListingCancelled(uint256 indexed listingId);
    event TokensReceived(address indexed user, uint256 amount);
    
    // Modifiers
    modifier onlyProducer(uint256 _listingId) {
        require(energyListings[_listingId].producer == msg.sender, "Only producer can perform this action");
        _;
    }
    
    modifier listingExists(uint256 _listingId) {
        require(_listingId < listingCount, "Listing does not exist");
        _;
    }
    
    modifier listingActive(uint256 _listingId) {
        require(energyListings[_listingId].isActive, "Listing is not active");
        _;
    }
    
    // Constructor
    constructor() {
        listingCount = 0;
        transactionCount = 0;
    }
    
    // Function to get initial tokens (simulates token distribution)
    function getInitialTokens() external {
        require(tokenBalance[msg.sender] == 0, "Tokens already received");
        tokenBalance[msg.sender] = INITIAL_TOKENS;
        emit TokensReceived(msg.sender, INITIAL_TOKENS);
    }
    
    // Producer lists energy for sale
    function listEnergy(uint256 _energyAmount, uint256 _pricePerUnit) external {
        require(_energyAmount > 0, "Energy amount must be greater than 0");
        require(_pricePerUnit > 0, "Price must be greater than 0");
        
        energyListings[listingCount] = EnergyListing({
            id: listingCount,
            producer: msg.sender,
            energyAmount: _energyAmount,
            pricePerUnit: _pricePerUnit,
            isActive: true,
            timestamp: block.timestamp
        });
        
        emit EnergyListed(listingCount, msg.sender, _energyAmount, _pricePerUnit);
        listingCount++;
    }
    
    // Consumer buys energy
    function buyEnergy(uint256 _listingId, uint256 _amount) 
        external 
        listingExists(_listingId) 
        listingActive(_listingId) 
    {
        EnergyListing storage listing = energyListings[_listingId];
        
        require(_amount > 0, "Amount must be greater than 0");
        require(_amount <= listing.energyAmount, "Not enough energy available");
        require(msg.sender != listing.producer, "Producer cannot buy own energy");
        
        uint256 totalPrice = _amount * listing.pricePerUnit;
        require(tokenBalance[msg.sender] >= totalPrice, "Insufficient token balance");
        
        // Transfer tokens from consumer to producer
        tokenBalance[msg.sender] -= totalPrice;
        tokenBalance[listing.producer] += totalPrice;
        
        // Update energy balance
        energyBalance[msg.sender] += _amount;
        
        // Update listing
        listing.energyAmount -= _amount;
        if (listing.energyAmount == 0) {
            listing.isActive = false;
        }
        
        // Record transaction
        transactions[transactionCount] = Transaction({
            id: transactionCount,
            listingId: _listingId,
            producer: listing.producer,
            consumer: msg.sender,
            energyAmount: _amount,
            totalPrice: totalPrice,
            timestamp: block.timestamp
        });
        
        emit EnergyPurchased(transactionCount, _listingId, msg.sender, _amount);
        transactionCount++;
    }
    
    // Producer cancels listing
    function cancelListing(uint256 _listingId) 
        external 
        listingExists(_listingId) 
        onlyProducer(_listingId) 
        listingActive(_listingId) 
    {
        energyListings[_listingId].isActive = false;
        emit ListingCancelled(_listingId);
    }
    
    // Get all active listings
    function getActiveListings() external view returns (EnergyListing[] memory) {
        uint256 activeCount = 0;
        
        // Count active listings
        for (uint256 i = 0; i < listingCount; i++) {
            if (energyListings[i].isActive) {
                activeCount++;
            }
        }
        
        // Create array of active listings
        EnergyListing[] memory activeListings = new EnergyListing[](activeCount);
        uint256 index = 0;
        
        for (uint256 i = 0; i < listingCount; i++) {
            if (energyListings[i].isActive) {
                activeListings[index] = energyListings[i];
                index++;
            }
        }
        
        return activeListings;
    }
    
    // Get user's transaction history
    function getUserTransactions(address _user) external view returns (Transaction[] memory) {
        uint256 userTxCount = 0;
        
        // Count user transactions
        for (uint256 i = 0; i < transactionCount; i++) {
            if (transactions[i].producer == _user || transactions[i].consumer == _user) {
                userTxCount++;
            }
        }
        
        // Create array of user transactions
        Transaction[] memory userTransactions = new Transaction[](userTxCount);
        uint256 index = 0;
        
        for (uint256 i = 0; i < transactionCount; i++) {
            if (transactions[i].producer == _user || transactions[i].consumer == _user) {
                userTransactions[index] = transactions[i];
                index++;
            }
        }
        
        return userTransactions;
    }
    
    // Get user stats
    function getUserStats(address _user) external view returns (
        uint256 tokens,
        uint256 energy,
        uint256 listingsCreated,
        uint256 purchasesMade
    ) {
        tokens = tokenBalance[_user];
        energy = energyBalance[_user];
        
        for (uint256 i = 0; i < listingCount; i++) {
            if (energyListings[i].producer == _user) {
                listingsCreated++;
            }
        }
        
        for (uint256 i = 0; i < transactionCount; i++) {
            if (transactions[i].consumer == _user) {
                purchasesMade++;
            }
        }
        
        return (tokens, energy, listingsCreated, purchasesMade);
    }
}