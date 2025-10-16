// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyTradingPlatform {
    
    enum EnergyType { SOLAR, WIND, HYDRO, BIOMASS, GEOTHERMAL }
    enum VerificationLevel { UNVERIFIED, BASIC, VERIFIED, CERTIFIED }
    
    struct EnergyListing {
        address producer;
        uint128 energyAmount;
        uint128 pricePerUnit;
        EnergyType energyType;
        uint32 expiryDate;
        uint32 minPurchase;
        uint32 carbonOffset;
        bool isActive;
    }
    
    struct Transaction {
        address producer;
        address consumer;
        uint128 energyAmount;
        uint128 totalPrice;
        uint32 timestamp;
        EnergyType energyType;
        bool isDisputed;
    }
    
    struct UserProfile {
        VerificationLevel verificationLevel;
        uint32 reputationScore;
        uint32 registrationDate;
        uint32 carbonCredits;
        bool isActive;
    }
    
    struct Escrow {
        address buyer;
        address seller;
        uint128 amount;
        uint32 releaseTime;
        bool isReleased;
        bool isRefunded;
    }
    
    mapping(uint256 => EnergyListing) public listings;
    mapping(uint256 => Transaction) public transactions;
    mapping(uint256 => Escrow) public escrows;
    mapping(address => uint256) public tokenBalance;
    mapping(address => uint256) public energyBalance;
    mapping(address => UserProfile) public profiles;
    mapping(address => bool) public blacklisted;
    
    uint256 public listingCount;
    uint256 public txCount;
    uint256 public escrowCount;
    uint256 public platformBalance;
    
    address public owner;
    
    uint256 constant INITIAL_TOKENS = 1000 ether;
    uint256 constant PLATFORM_FEE = 2;
    uint256 constant ESCROW_PERIOD = 7 days;
    uint256 constant LISTING_EXPIRY = 30 days;
    uint256 constant MAX_PRICE = 100 ether;
    uint256 constant MIN_PRICE = 0.001 ether;
    
    event EnergyListed(uint256 indexed id, address indexed producer, uint256 amount, uint256 price, EnergyType energyType);
    event EnergyPurchased(uint256 indexed txId, uint256 indexed listingId, address indexed consumer, uint256 amount);
    event EscrowReleased(uint256 indexed escrowId, address indexed seller, uint256 amount);
    event DisputeRaised(uint256 indexed txId, address indexed raiser);
    event DisputeResolved(uint256 indexed txId, bool refunded);
    event UserRegistered(address indexed user, uint32 timestamp);
    event TokensClaimed(address indexed user, uint256 amount);
    event ListingCancelled(uint256 indexed listingId);
    event PriceUpdated(uint256 indexed listingId, uint128 newPrice);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    modifier notBlacklisted() {
        require(!blacklisted[msg.sender], "User blacklisted");
        _;
    }
    
    modifier registered() {
        require(profiles[msg.sender].registrationDate > 0, "Not registered");
        _;
    }
    
    constructor() {
        owner = msg.sender;
        // Auto-register owner
        profiles[msg.sender] = UserProfile({
            verificationLevel: VerificationLevel.CERTIFIED,
            reputationScore: 100,
            registrationDate: uint32(block.timestamp),
            carbonCredits: 0,
            isActive: true
        });
    }
    
    // User registration
    function register() external {
        require(profiles[msg.sender].registrationDate == 0, "Already registered");
        profiles[msg.sender] = UserProfile({
            verificationLevel: VerificationLevel.UNVERIFIED,
            reputationScore: 50,
            registrationDate: uint32(block.timestamp),
            carbonCredits: 0,
            isActive: true
        });
        emit UserRegistered(msg.sender, uint32(block.timestamp));
    }
    
    // Claim initial tokens (can only be done once)
    function getTokens() external notBlacklisted registered {
        require(tokenBalance[msg.sender] == 0, "Tokens already claimed");
        tokenBalance[msg.sender] = INITIAL_TOKENS;
        emit TokensClaimed(msg.sender, INITIAL_TOKENS);
    }
    
    // List energy for sale
    function listEnergy(
        uint128 _amount,
        uint128 _price,
        EnergyType _type,
        uint32 _minPurchase,
        uint32 _carbonOffset
    ) external notBlacklisted registered {
        require(_amount > 0, "Amount must be positive");
        require(_minPurchase > 0 && _minPurchase <= _amount, "Invalid min purchase");
        require(_price >= MIN_PRICE && _price <= MAX_PRICE, "Price out of range");
        
        listings[listingCount] = EnergyListing({
            producer: msg.sender,
            energyAmount: _amount,
            pricePerUnit: _price,
            energyType: _type,
            expiryDate: uint32(block.timestamp + LISTING_EXPIRY),
            minPurchase: _minPurchase,
            carbonOffset: _carbonOffset,
            isActive: true
        });
        
        emit EnergyListed(listingCount, msg.sender, _amount, _price, _type);
        listingCount++;
    }
    
    // Buy energy from a listing
    function buyEnergy(uint256 _listingId, uint128 _amount) external notBlacklisted registered {
        require(_listingId < listingCount, "Invalid listing ID");
        EnergyListing storage listing = listings[_listingId];
        require(listing.isActive, "Listing not active");
        require(listing.expiryDate > block.timestamp, "Listing expired");
        require(_amount >= listing.minPurchase, "Below minimum purchase");
        require(_amount <= listing.energyAmount, "Insufficient energy available");
        require(msg.sender != listing.producer, "Cannot buy own energy");
        
        uint256 totalPrice = uint256(_amount) * uint256(listing.pricePerUnit);
        uint256 fee = (totalPrice * PLATFORM_FEE) / 100;
        uint256 totalCost = totalPrice + fee;
        
        require(tokenBalance[msg.sender] >= totalCost, "Insufficient tokens");
        
        tokenBalance[msg.sender] -= totalCost;
        platformBalance += fee;
        
        escrows[escrowCount] = Escrow({
            buyer: msg.sender,
            seller: listing.producer,
            amount: uint128(totalPrice),
            releaseTime: uint32(block.timestamp + ESCROW_PERIOD),
            isReleased: false,
            isRefunded: false
        });
        
        energyBalance[msg.sender] += _amount;
        profiles[msg.sender].carbonCredits += uint32((_amount * listing.carbonOffset) / 1000);
        
        listing.energyAmount -= _amount;
        if (listing.energyAmount == 0) listing.isActive = false;
        
        transactions[txCount] = Transaction({
            producer: listing.producer,
            consumer: msg.sender,
            energyAmount: _amount,
            totalPrice: uint128(totalPrice),
            timestamp: uint32(block.timestamp),
            energyType: listing.energyType,
            isDisputed: false
        });
        
        emit EnergyPurchased(txCount, _listingId, msg.sender, _amount);
        
        escrowCount++;
        txCount++;
    }
    
    // Release escrow payment to seller
    function releaseEscrow(uint256 _escrowId) external {
        require(_escrowId < escrowCount, "Invalid escrow ID");
        Escrow storage escrow = escrows[_escrowId];
        require(!escrow.isReleased && !escrow.isRefunded, "Escrow already processed");
        require(
            msg.sender == escrow.buyer || block.timestamp >= escrow.releaseTime,
            "Cannot release yet"
        );
        
        tokenBalance[escrow.seller] += escrow.amount;
        escrow.isReleased = true;
        
        _updateReputation(escrow.seller, true);
        _updateReputation(escrow.buyer, true);
        
        emit EscrowReleased(_escrowId, escrow.seller, escrow.amount);
    }
    
    // Raise a dispute for a transaction
    function raiseDispute(uint256 _txId) external {
        require(_txId < txCount, "Invalid transaction ID");
        Transaction storage txn = transactions[_txId];
        require(
            msg.sender == txn.consumer || msg.sender == txn.producer,
            "Not part of transaction"
        );
        require(!txn.isDisputed, "Already disputed");
        
        txn.isDisputed = true;
        emit DisputeRaised(_txId, msg.sender);
    }
    
    // Resolve dispute (owner only)
    function resolveDispute(uint256 _txId, bool _refund) external onlyOwner {
        require(_txId < txCount, "Invalid transaction ID");
        Transaction storage txn = transactions[_txId];
        require(txn.isDisputed, "No active dispute");
        
        // Find the related escrow
        for (uint256 i = 0; i < escrowCount; i++) {
            Escrow storage escrow = escrows[i];
            if (escrow.buyer == txn.consumer && 
                escrow.seller == txn.producer && 
                !escrow.isReleased && 
                !escrow.isRefunded) {
                
                if (_refund) {
                    tokenBalance[escrow.buyer] += escrow.amount;
                    escrow.isRefunded = true;
                    _updateReputation(escrow.seller, false);
                } else {
                    tokenBalance[escrow.seller] += escrow.amount;
                    escrow.isReleased = true;
                    _updateReputation(escrow.buyer, false);
                }
                txn.isDisputed = false;
                emit DisputeResolved(_txId, _refund);
                break;
            }
        }
    }
    
    // Update user reputation
    function _updateReputation(address _user, bool _positive) internal {
        UserProfile storage profile = profiles[_user];
        if (_positive) {
            if (profile.reputationScore < 100) {
                profile.reputationScore += 5;
                if (profile.reputationScore > 100) profile.reputationScore = 100;
            }
        } else {
            if (profile.reputationScore > 10) {
                profile.reputationScore -= 10;
            } else {
                profile.reputationScore = 0;
            }
        }
    }
    
    // Cancel an active listing
    function cancelListing(uint256 _listingId) external {
        require(_listingId < listingCount, "Invalid listing ID");
        require(listings[_listingId].producer == msg.sender, "Not your listing");
        require(listings[_listingId].isActive, "Listing not active");
        listings[_listingId].isActive = false;
        emit ListingCancelled(_listingId);
    }
    
    // Update listing price
    function updatePrice(uint256 _listingId, uint128 _newPrice) external {
        require(_listingId < listingCount, "Invalid listing ID");
        require(listings[_listingId].producer == msg.sender, "Not your listing");
        require(_newPrice >= MIN_PRICE && _newPrice <= MAX_PRICE, "Price out of range");
        listings[_listingId].pricePerUnit = _newPrice;
        emit PriceUpdated(_listingId, _newPrice);
    }
    
    // Verify user (owner only)
    function verifyUser(address _user, VerificationLevel _level) external onlyOwner {
        require(profiles[_user].registrationDate > 0, "User not registered");
        profiles[_user].verificationLevel = _level;
    }
    
    // Blacklist/unblacklist user (owner only)
    function blacklistUser(address _user, bool _status) external onlyOwner {
        blacklisted[_user] = _status;
    }
    
    // Withdraw platform fees (owner only)
    function withdrawFees() external onlyOwner {
        uint256 amount = platformBalance;
        require(amount > 0, "No fees to withdraw");
        platformBalance = 0;
        tokenBalance[owner] += amount;
    }
    
    // Get all active listings
    function getActiveListings() external view returns (uint256[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < listingCount; i++) {
            if (listings[i].isActive && listings[i].expiryDate > block.timestamp) {
                count++;
            }
        }
        
        uint256[] memory activeIds = new uint256[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < listingCount; i++) {
            if (listings[i].isActive && listings[i].expiryDate > block.timestamp) {
                activeIds[index] = i;
                index++;
            }
        }
        return activeIds;
    }
    
    // Get listings by energy type
    function getListingsByType(EnergyType _type) external view returns (uint256[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < listingCount; i++) {
            if (listings[i].isActive && 
                listings[i].energyType == _type && 
                listings[i].expiryDate > block.timestamp) {
                count++;
            }
        }
        
        uint256[] memory ids = new uint256[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < listingCount; i++) {
            if (listings[i].isActive && 
                listings[i].energyType == _type && 
                listings[i].expiryDate > block.timestamp) {
                ids[index] = i;
                index++;
            }
        }
        return ids;
    }
    
    // Get user statistics
    function getUserStats(address _user) external view returns (
        uint256 tokens,
        uint256 energy,
        uint32 reputation,
        uint32 carbonCredits,
        VerificationLevel level
    ) {
        return (
            tokenBalance[_user],
            energyBalance[_user],
            profiles[_user].reputationScore,
            profiles[_user].carbonCredits,
            profiles[_user].verificationLevel
        );
    }
    
    // Get user's transactions
    function getUserTransactions(address _user) external view returns (uint256[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < txCount; i++) {
            if (transactions[i].producer == _user || transactions[i].consumer == _user) {
                count++;
            }
        }
        
        uint256[] memory txIds = new uint256[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < txCount; i++) {
            if (transactions[i].producer == _user || transactions[i].consumer == _user) {
                txIds[index] = i;
                index++;
            }
        }
        return txIds;
    }
    
    // Get user's escrows
    function getUserEscrows(address _user) external view returns (uint256[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < escrowCount; i++) {
            if (escrows[i].buyer == _user || escrows[i].seller == _user) {
                count++;
            }
        }
        
        uint256[] memory escrowIds = new uint256[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < escrowCount; i++) {
            if (escrows[i].buyer == _user || escrows[i].seller == _user) {
                escrowIds[index] = i;
                index++;
            }
        }
        return escrowIds;
    }
    
    // Get listing details
    function getListingDetails(uint256 _listingId) external view returns (
        address producer,
        uint128 energyAmount,
        uint128 pricePerUnit,
        EnergyType energyType,
        uint32 expiryDate,
        uint32 minPurchase,
        uint32 carbonOffset,
        bool isActive
    ) {
        require(_listingId < listingCount, "Invalid listing ID");
        EnergyListing memory listing = listings[_listingId];
        return (
            listing.producer,
            listing.energyAmount,
            listing.pricePerUnit,
            listing.energyType,
            listing.expiryDate,
            listing.minPurchase,
            listing.carbonOffset,
            listing.isActive
        );
    }
    
    // Get transaction details
    function getTransactionDetails(uint256 _txId) external view returns (
        address producer,
        address consumer,
        uint128 energyAmount,
        uint128 totalPrice,
        uint32 timestamp,
        EnergyType energyType,
        bool isDisputed
    ) {
        require(_txId < txCount, "Invalid transaction ID");
        Transaction memory txn = transactions[_txId];
        return (
            txn.producer,
            txn.consumer,
            txn.energyAmount,
            txn.totalPrice,
            txn.timestamp,
            txn.energyType,
            txn.isDisputed
        );
    }
}
