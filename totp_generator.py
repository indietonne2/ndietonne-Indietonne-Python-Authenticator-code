import pyotp
import datetime
import hashlib
import base64


class TOTP:

    @staticmethod
    def hex_to_base32(hex_key):
        """Convert a hex key to base32 format"""
        return base64.b32encode(bytes.fromhex(hex_key)).decode('utf-8')

    @staticmethod
    def generate_totp(key, time, return_digits, crypto='HmacSHA1'):
        time_int = int(time, 16)
        digest = hashlib.sha1
        if crypto == 'HmacSHA256':
            digest = hashlib.sha256
        elif crypto == 'HmacSHA512':
            digest = hashlib.sha512
        base32_key = TOTP.hex_to_base32(key)
        totp = pyotp.TOTP(base32_key, digits=int(return_digits), digest=digest)
        otp = totp.at(time_int)
        return otp

    @staticmethod
    def main():
        seed = "3132333435363738393031323334353637383930"
        seed32 = ("31323334353637383930313233343536373839303132333435363738393031323334"
                  "313233343536373839303132")
        seed64 = ("31323334353637383930313233343536373839303132333435363738393031323334"
                  "313233343536373839303132333435363738393031323334")
        t0 = 0
        x = 30
        test_times = [59, 1111111109, 1111111111, 1234567890, 2000000000, 20000000000]

        print("+---------------+-----------------------+------------------+--------+--------+")
        print("|  Time(sec)    |   Time (UTC format)   | Value of T(Hex)  |  TOTP  | Mode   |")
        print("+---------------+-----------------------+------------------+--------+--------+")

        for t in test_times:
            time_val = (t - t0) // x
            steps = hex(time_val)[2:].upper().zfill(16)
            fmt_time = str(t).ljust(11)
            utc_time = datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
            print(f"|  {fmt_time}  |  {utc_time}  | {steps} | {TOTP.generate_totp(seed, steps, '8', 'HmacSHA1')} | SHA1   |")
            print(f"|  {fmt_time}  |  {utc_time}  | {steps} | {TOTP.generate_totp(seed32, steps, '8', 'HmacSHA256')} | SHA256 |")
            print(f"|  {fmt_time}  |  {utc_time}  | {steps} | {TOTP.generate_totp(seed64, steps, '8', 'HmacSHA512')} | SHA512 |")
            print("+---------------+-----------------------+------------------+--------+--------+")


if __name__ == "__main__":
    TOTP.main()
