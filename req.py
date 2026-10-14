import requests
import os 

sec_key=os.getenv("JWT_SECRET_KEY")
header={"Authorization":sec_key}

r=requests.get("http://localhost:5000/protected", headers=header)
print(r.json())