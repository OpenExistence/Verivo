// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract ProposalVoting is Ownable {
    
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
        bool votingOpen;
        mapping(address => bool) voters;
    }
    
    Proposal[] public proposals;
    address public votingNFTContract;
    
    event ProposalCreated(uint256 indexed proposalId, string description);
    event VotingStarted(uint256 indexed proposalId);
    event VoteCast(uint256 indexed proposalId, address indexed voter);
    event ProposalExecuted(uint256 indexed proposalId);
    
    constructor(address _votingNFTContract) Ownable(msg.sender) {
        votingNFTContract = _votingNFTContract;
    }
    
    function createProposal(string calldata description) external onlyOwner {
        Proposal storage proposal = proposals.push();
        proposal.description = description;
        proposal.voteCount = 0;
        proposal.executed = false;
        proposal.votingOpen = false;
        
        emit ProposalCreated(proposals.length - 1, description);
    }
    
    // Allow specific voters for a proposal and start voting
    function startVoting(uint256 proposalId, address[] calldata voters) external onlyOwner {
        require(proposalId < proposals.length, "Proposal does not exist");
        require(!proposals[proposalId].votingOpen, "Voting already open");
        
        Proposal storage proposal = proposals[proposalId];
        proposal.votingOpen = true;
        
        // Call NFT contract to allow voters
        IVotingNFT(votingNFTContract).allowVoters(proposalId, voters);
        
        emit VotingStarted(proposalId);
    }
    
    // Get proposal details
    function getProposal(uint256 proposalId) external view returns (
        string memory description,
        uint256 voteCount,
        bool executed,
        bool votingOpen,
        bool hasVoted
    ) {
        require(proposalId < proposals.length, "Proposal does not exist");
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.description,
            proposal.voteCount,
            proposal.executed,
            proposal.votingOpen,
            proposal.voters[msg.sender]
        );
    }
    
    function getProposalCount() external view returns (uint256) {
        return proposals.length;
    }
    
    // Record vote (called after NFT mint)
    function recordVote(uint256 proposalId, address voter) external {
        require(msg.sender == votingNFTContract, "Only NFT contract");
        require(proposalId < proposals.length, "Proposal does not exist");
        
        Proposal storage proposal = proposals[proposalId];
        require(proposal.votingOpen, "Voting not open");
        require(!proposal.voters[voter], "Already voted");
        
        proposal.voters[voter] = true;
        proposal.voteCount++;
        
        emit VoteCast(proposalId, voter);
    }
    
    function executeProposal(uint256 proposalId) external onlyOwner {
        require(proposalId < proposals.length, "Proposal does not exist");
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Already executed");
        
        proposal.executed = true;
        
        emit ProposalExecuted(proposalId);
    }
}

interface IVotingNFT {
    function allowVoters(uint256 proposalId, address[] calldata voters) external;
}
