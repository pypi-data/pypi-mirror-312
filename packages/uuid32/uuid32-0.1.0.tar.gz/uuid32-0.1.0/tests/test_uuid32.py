import unittest
from uuid32 import uuid32

class TestUUID32(unittest.TestCase):
    def test_uuid32_length(self):
        """Test if the generated string has a length of 32 characters."""
        result = uuid32()
        self.assertEqual(len(result), 32, "The length of the UUID should be 32 characters.")

    def test_uuid32_characters(self):
        """Test if the generated string contains only valid characters (digits and lowercase letters)."""
        result = uuid32()
        valid_characters = "abcdefghijklmnopqrstuvwxyz0123456789"
        self.assertTrue(
            all(c in valid_characters for c in result),
            "The UUID contains invalid characters."
        )

    def test_uuid32_uniqueness(self):
        """Test if multiple calls to uuid32 produce unique results."""
        results = {uuid32() for _ in range(1000)}  # Generate 1000 UUIDs
        self.assertEqual(len(results), 1000, "UUIDs are not unique.")

if __name__ == "__main__":
    unittest.main()
