from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta

# Generate RSA Private Key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Generate a self-signed certificate
subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Example Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, "example.com"),
])

issuer = subject  # Self-signed
certificate = x509.CertificateBuilder().subject_name(subject)
certificate = certificate.issuer_name(issuer)
certificate = certificate.public_key(private_key.public_key())
certificate = certificate.serial_number(x509.random_serial_number())
certificate = certificate.not_valid_before(datetime.utcnow())
certificate = certificate.not_valid_after(datetime.utcnow() + timedelta(days=365))
certificate = certificate.add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName("example.com"),
        x509.DNSName("www.example.com")
    ]),
    critical=False
)
certificate = certificate.sign(private_key, hashes.SHA256())

# Save the private key and certificate to files
with open("key.pem", "wb") as key_file:
    key_file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("cert.pem", "wb") as cert_file:
    cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))

print("Private key saved to 'key.pem' and certificate saved to 'cert.pem'")
