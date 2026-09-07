import unittest

from veilcheck.policy import validate_policy


class PolicyValidationTests(unittest.TestCase):
    def test_accepts_minimal_valid_policy(self) -> None:
        policy = {
            "schema": "veilcheck/v1",
            "assets": [
                {
                    "id": "order.amount",
                    "class": "confidential",
                    "selectors": ["contracts/Order.sol::Order.amount"],
                    "forbidden_surfaces": ["event", "transaction_calldata"],
                    "allowed_disclosures": [{"surface": "commitment", "transform": "commitment_with_secret_blinder"}],
                }
            ],
        }
        self.assertTrue(validate_policy(policy).valid)

    def test_rejects_duplicate_asset_ids(self) -> None:
        policy = {
            "schema": "veilcheck/v1",
            "assets": [
                {"id": "amount", "class": "secret", "selectors": ["A::x"]},
                {"id": "amount", "class": "public", "selectors": ["A::y"]},
            ],
        }
        errors = validate_policy(policy).errors
        self.assertTrue(any("duplicates" in error for error in errors))

    def test_rejects_unknown_surface(self) -> None:
        policy = {
            "schema": "veilcheck/v1",
            "assets": [
                {"id": "amount", "class": "secret", "selectors": ["A::x"], "forbidden_surfaces": ["magic"]}
            ],
        }
        self.assertFalse(validate_policy(policy).valid)
