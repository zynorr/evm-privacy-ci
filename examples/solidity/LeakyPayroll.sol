// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

/// @notice Intentionally insecure documentation fixture. Do not deploy.
contract LeakyPayroll {
    event SalaryPaid(address indexed employee, uint256 amount);

    mapping(address => uint256) public salaryOf;

    function pay(address employee, uint256 amount) external {
        // Planned VC002: amount appears in public calldata.
        salaryOf[employee] = amount;
        // Planned VC001 / VC004: raw confidential value is stored and getter-exposed.
        emit SalaryPaid(employee, amount);
        // Planned VC003: event data is public.
    }
}
