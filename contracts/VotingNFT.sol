// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract VotingNFT is ERC721, Ownable {
    uint256 private _tokenIdCounter;
    
    // Mapping pour vérifier si une adresse a le droit de vote
    mapping(address => bool) public hasVotingRight;
    
    // Événements
    event VotingRightGranted(address indexed to);
    event VotingRightRevoked(address indexed from);
    
    constructor() ERC721("VotingRight", "VOTE") Ownable(msg.sender) {}
    
    /**
     * @dev Mint un NFT de vote pour une adresse
     */
    function grantVotingRight(address to) public onlyOwner {
        require(!hasVotingRight[to], "Address already has voting right");
        
        _tokenIdCounter++;
        uint256 tokenId = _tokenIdCounter;
        _mint(to, tokenId);
        hasVotingRight[to] = true;
        
        emit VotingRightGranted(to);
    }
    
    /**
     * @dev Révoquer le droit de vote (burn le NFT)
     */
    function revokeVotingRight(address from) public onlyOwner {
        require(hasVotingRight[from], "Address has no voting right");
        
        uint256 tokenId = tokenOfOwnerByIndex(from, 0);
        _burn(tokenId);
        hasVotingRight[from] = false;
        
        emit VotingRightRevoked(from);
    }
    
    /**
     * @dev Vérifie si une adresse peut voter
     */
    function canVote(address account) public view returns (bool) {
        return hasVotingRight[account];
    }
    
    /**
     * @dev Override pour démarrer l'ID à 1
     */
    function _startTokenId() internal pure override returns (uint256) {
        return 1;
    }
}
