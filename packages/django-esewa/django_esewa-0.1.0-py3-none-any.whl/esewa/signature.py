import hmac
import hashlib
import base64

def generate_signature(total_amount, transaction_uuid, key="8gBm/:&EnhH.1/q", product_code="EPAYTEST"):
    if not total_amount or not transaction_uuid:
        raise ValueError("Both 'total_amount' and 'transaction_uuid' are required.")

    try:
        message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
        key = key.encode('utf-8')
        message = message.encode('utf-8')

        # Generate HMAC-SHA256 digest
        hmac_sha256 = hmac.new(key, message, hashlib.sha256)
        digest = hmac_sha256.digest()

        # Convert to Base64
        signature = base64.b64encode(digest).decode('utf-8')
        return signature
    except Exception as e:
        raise RuntimeError(f"Failed to generate signature: {e}")



if __name__ == "__main__":
    signature = generate_signature(total_amount="1000", transaction_uuid="1234abcd")
    print(f"Generated Signature: {signature}")
