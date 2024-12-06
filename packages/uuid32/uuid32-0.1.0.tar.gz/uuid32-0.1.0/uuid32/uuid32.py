import random
import string
import socket
import hashlib
import time

# A global variable containing the valid characters for the UUID
# Digits (0-9) and lowercase English letters (a-z)
CHARACTERS_UUID32 = string.digits + string.ascii_lowercase


def enhance_random_with_hostname():
    """
    Enhances the random number generator by seeding it with a combination of
    the machine's hostname and the current timestamp.
    """
    try:
        # Get the hostname of the current machine
        hostname = socket.gethostname()

        # Hash the hostname to create a stable, uniform value
        hostname_hash = hashlib.sha256(hostname.encode()).hexdigest()

        # Convert the hash to an integer
        hostname_seed = int(hostname_hash, 16)

        # Get the current time in milliseconds
        time_seed = int(time.time() * 1000)

        # Combine the hostname seed and time seed using XOR for randomness
        combined_seed = hostname_seed ^ time_seed

        # Seed the random number generator with the combined value
        random.seed(combined_seed)
    except Exception as e:
        # Print an error message if the enhancement fails
        print(f"Failed to enhance random: {e}")


def uuid32():
    """
    Generates a random 32-character string using digits (0-9)
    and lowercase English letters (a-z).
    """
    # Generate a random string of 32 characters
    return ''.join(random.choices(CHARACTERS_UUID32, k=32))


# Automatically enhance the random number generator upon module import
enhance_random_with_hostname()
