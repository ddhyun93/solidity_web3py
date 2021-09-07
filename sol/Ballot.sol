//SPDX-License-Identifier: MIT License
pragma solidity >=0.4.22 <0.9.0;

contract BallotV1 {
    // types
    struct Voter {
        // Voter details
        uint weight;
        bool voted;
        uint vote;
    }
    struct Proposal {
        // Proposal details
        uint voteCount;
    }
    address chairperson;
    mapping(address=>Voter) voters; // declare voters ; address: Voter map
    Proposal[] proposals;           // declare proposals ; array of Proposal
    enum Phase {Init, Regs, Vote, Done}    // declare Phase ;

    Phase public state = Phase.Init;     // initialize state valuable to "Init", type of state is "Phase"

    // modifier
    modifier validPhase(Phase reqPhase) {
        require(state == reqPhase);
        _;
    }
    modifier onlyChair() {
        require(msg.sender == chairperson);
        _;
    }

    // vote starts as chairperson deploy this contract !!!!!!!
    constructor (uint numProposals) public {
        chairperson = msg.sender;
        voters[chairperson].weight = 2;     // set chairperson's vote weight to 2
        for (uint prop = 0; prop < numProposals; prop++) {
            proposals.push(Proposal(0));     // append zero count of vote to proposals, length of proposals based on num of candidates
        }
        state = Phase.Regs;                  // change state(type Phase) to RegisterPhase once Initialized
    }

    function changeState(Phase x) public onlyChair {    // executor is not chairperson -> revert
        require(x>state);                               // changed state out of range -> revert
        // if (x < state) revert();
        state = x;
    }

    function register(address voter) public validPhase(Phase.Regs) onlyChair {
        require(!voters[voter].voted);                  // if executor is not chairperson, voter already voted -> revert
        // if (voters[voter].voted) revert();
        require(msg.sender != chairperson);             // chairperson can not register by self
        voters[voter].weight = 1;
        voters[voter].voted = false;
    }

    function vote(uint toProposal) public validPhase(Phase.Vote) {
        Voter memory sender = voters[msg.sender];
        require(!sender.voted);
        require(toProposal<proposals.length);                           // if already voted or vote target is out of range -> revert
        // if (sender.voted || toProposal >= proposals.length) revert();
        voters[msg.sender].voted = true;
        sender.vote = toProposal;
        proposals[toProposal].voteCount += sender.weight;
    }

    function reqWinner() public validPhase(Phase.Done) view returns (uint winningProposal) {
        uint winningVoteCount = 0;
        for (uint prop = 0; prop < proposals.length; prop++) {
            if (proposals[prop].voteCount > winningVoteCount) {         // extract highest voter logic
                winningVoteCount = proposals[prop].voteCount;
                winningProposal = prop;
            }
        }
        assert(winningVoteCount >= 3);      // if count under 3 > not return anything
    }
}
