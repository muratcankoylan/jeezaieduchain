import requests
from datetime import datetime
from flask import session

class CredentialIssuer:
    def __init__(self, api_key, environment='staging'):
        self.api_key = api_key
        self.base_url = 'https://api.vc.opencampus.xyz' if environment == 'production' else 'https://api.vc.staging.opencampus.xyz'
        
    def issue_credential(self, holder_ocid, achievement_data):
        """
        Issue a verifiable credential to a user using the VC Issuance API
        """
        current_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        # Format credential payload according to the sample JSON
        credential_payload = {
            "validFrom": current_date,
            "awardedDate": current_date,
            "description": achievement_data.get('description', ''),
            "credentialSubject": {
                "id": f"did:ethr:{session.get('user', {}).get('eth_address')}",  # Use ETH address from session
                "name": "JEZM Student",
                "type": "Person",
                "email": "student@jeezai.edu",
                "image": "https://via.placeholder.com/300x200",
                "profileUrl": f"https://id.staging.opencampus.xyz/profile/{holder_ocid}",
                "achievement": {
                    "name": achievement_data['name'],
                    "identifier": achievement_data['id'],  # Use achievement_id as identifier
                    "description": achievement_data.get('description', ''),
                    "achievementType": achievement_data.get('type', 'Achievement')
                }
            }
        }

        request_payload = {
            'credentialPayload': credential_payload,
            'holderOcId': holder_ocid
        }

        print("Sending request to:", f'{self.base_url}/issuer/vc')
        print("Headers:", {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        })
        print("Request payload:", request_payload)

        try:
            response = requests.post(
                f'{self.base_url}/issuer/vc',
                headers={
                    'X-API-KEY': self.api_key,
                    'Content-Type': 'application/json'
                },
                json=request_payload
            )
            
            print("Response status:", response.status_code)
            print("Response content:", response.text)
            
            if not response.ok:
                error_message = response.json().get('error', {}).get('message', 'Unknown error')
                print(f"Error message from API: {error_message}")
                raise Exception(error_message)
                
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Error response: {e.response.text}")
            raise Exception(f"Failed to issue credential: {str(e)}")

    def get_user_credentials(self, holder_ocid):
        """
        Return the URL to view credentials on OC-ID
        """
        # Use staging or production URL based on environment
        base_url = 'https://id.staging.opencampus.xyz' if self.base_url.endswith('staging.opencampus.xyz') else 'https://id.opencampus.xyz'
        
        return {
            'data': [],  # Empty list for backward compatibility
            'profile_url': f"{base_url}/profile/{holder_ocid}"
        }