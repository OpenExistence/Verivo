// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract VotingNFT is ERC721, Ownable {
    uint256 private _tokenIdCounter;
    address public proposalContract;
    
    // Mapping: proposalId => allowed voters
    mapping(uint256 => mapping(address => bool)) public allowedVoters;
    // Mapping: proposalId => hasVoted
    mapping(uint256 => mapping(address => bool)) public hasVoted;
    
    event VotingRightGranted(uint256 indexed proposalId, address indexed to);
    event VoteCast(uint256 indexed proposalId, address indexed voter);
    
    constructor() ERC721("VotingRight", "VOTE") Ownable(msg.sender) {}
    
    function setProposalContract(address _proposalContract) external onlyOwner {
        proposalContract = _proposalContract;
    }
    
    // Allow specific addresses to vote on a specific proposal
    function allowVoters(uint256 proposalId, address[] calldata voters) external onlyOwner {
        for (uint i = 0; i < voters.length; i++) {
            allowedVoters[proposalId][voters[i]] = true;
        }
    }
    
    // Mint NFT to voter and record vote in one transaction
    function mintAndVote(uint256 proposalId, string calldata description) external {
        require(allowedVoters[proposalId][msg.sender], "Not allowed to vote");
        require(!hasVoted[proposalId][msg.sender], "Already voted");
        
        // Mint NFT
        _tokenIdCounter++;
        uint256 tokenId = _tokenIdCounter;
        _mint(msg.sender, tokenId);
        
        // Record vote (the description is stored on-chain for this vote)
        hasVoted[proposalId][msg.sender] = true;
        
        emit VotingRightGranted(proposalId, msg.sender);
        emit VoteCast(proposalId, msg.sender);
    }
    
    // Check if address can vote on proposal
    function canVote(uint256 proposalId, address account) external view returns (bool) {
        return allowedVoters[proposalId][account] && !hasVoted[proposalId][account];
    }
    
    // Check if address has already voted
    function hasVotedOn(uint256 proposalId, address account) external view returns (bool) {
        return hasVoted[proposalId][account];
    }
    
    function _startTokenId() internal pure override returns (uint256) {
        return 1;
    }
}
