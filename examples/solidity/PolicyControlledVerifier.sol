// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

/// @notice Intentionally simplified documentation fixture. It is not a proof verifier.
contract PolicyControlledVerifier {
    event NullifierUsed(bytes32 indexed nullifier);

    function submit(bytes32 root, bytes32 nullifier, uint256 amount) external {
        uint256[] memory publicInputs = new uint256[](3);
        publicInputs[0] = uint256(root);
        publicInputs[1] = uint256(nullifier);
        publicInputs[2] = amount;
        // Planned VC102: amount must not be a public input under the sample policy.
        emit NullifierUsed(nullifier);
        // A nullifier may be an allowed linkability surface when policy declares it.
    }
}
