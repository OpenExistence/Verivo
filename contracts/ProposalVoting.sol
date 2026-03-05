// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract ProposalVoting is Ownable {
    
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
        mapping(address => bool) voters;
    }
    
    Proposal[] public proposals;
    
    // Adresse du contrat NFT pour vérifier les droits de vote
    address public votingNFTContract;
    
    event ProposalCreated(uint256 indexed proposalId, string description);
    event VoteCast(uint256 indexed proposalId, address indexed voter);
    event ProposalExecuted(uint256 indexed proposalId);
    
    constructor(address _votingNFTContract) Ownable(msg.sender) {
        votingNFTContract = _votingNFTContract;
    }
    
    /**
     * @dev Créer une nouvelle proposition
     */
    function createProposal(string calldata description) external onlyOwner {
        Proposal storage proposal = proposals.push();
        proposal.description = description;
        proposal.voteCount = 0;
        proposal.executed = false;
        
        emit ProposalCreated(proposals.length - 1, description);
    }
    
    /**
     * @dev Voter pour une proposition (vérifie le NFT)
     */
    function vote(uint256 proposalId) external {
        require(proposalId < proposals.length, "Proposal does not exist");
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Proposal already executed");
        require(!proposal.voters[msg.sender], "Already voted");
        
        // Vérification via interface ERC721
        try IERC721(votingNFTContract).balanceOf(msg.sender) returns (uint256 balance) {
            require(balance > 0, "No voting NFT");
        } catch {
            revert("Voting NFT contract invalid");
        }
        
        proposal.voters[msg.sender] = true;
        proposal.voteCount++;
        
        emit VoteCast(proposalId, msg.sender);
    }
    
    /**
     * @dev Exécuter une proposition
     */
    function executeProposal(uint256 proposalId) external onlyOwner {
        require(proposalId < proposals.length, "Proposal does not exist");
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Already executed");
        
        proposal.executed = true;
        
        emit ProposalExecuted(proposalId);
    }
    
    /**
     * @dev Obtenir le nombre de propositions
     */
    function getProposalCount() external view returns (uint256) {
        return proposals.length;
    }
    
    /**
     * @dev Obtenir les détails d'une proposition
     */
    function getProposal(uint256 proposalId) external view returns (
        string memory description,
        uint256 voteCount,
        bool executed,
        bool hasVoted
    ) {
        require(proposalId < proposals.length, "Proposal does not exist");
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.description,
            proposal.voteCount,
            proposal.executed,
            proposal.voters[msg.sender]
        );
    }
}

// Interface minimale ERC721
interface IERC721 {
    function balanceOf(address owner) external view returns (uint256);
}
