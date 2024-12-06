import pyotp

class OTPClient:
    """
    A client for generating and verifying one-time passwords (OTPs) using TOTP.
    """
    def __init__(self, secret):
        """
        Initialize the OTP client with a secret key.

        :param secret: The base32-encoded secret key used to generate OTPs.
        """
        self.secret = secret
        self.totp = pyotp.TOTP(self.secret)  # Create a TOTP instance with the secret

    def get_otp(self):
        """
        Generate a new OTP based on the current time.

        :return: A string representing the generated OTP.
        """
        return self.totp.now()  # Use .now() to generate the OTP based on the current time

if __name__ == '__main__':
    # Example usage
    secret_key = "HIF64ZBKKUGUAFFX"
    otp_client = OTPClient(secret_key)
    otp = otp_client.get_otp()
    print(f"Generated OTP: {otp}")