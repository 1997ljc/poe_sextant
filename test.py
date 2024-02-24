import gzip
import base64
import io
import json

with open(r"..\price2.txt", "rb") as price:
    price_date = price.read()

compressed_bytes = base64.b64decode(price_date)
bytes_compressed = gzip.compress(compressed_bytes)
with gzip.GzipFile(fileobj=io.BytesIO(compressed_bytes), mode='rb') as f:
    decompressed_bytes = f.read()
decompressed_json = decompressed_bytes.decode('utf-8')
print(decompressed_json)

#decompressed_data = json.loads(decompressed_json)
