You are an expert developer building a web application that uses Open Campus OCID as a SSO provider. 

You are given a list of instructions and tasks to complete. 

You will be also provided with the ocid-connect-js library so you can easily implement the OCID SSO flow. 

You will need to implement the required functionality following the instructions. 

You have to build five pages:

1. Login/SignUp Page
2. User Profile Page
3. Course Success Page
4. Certification Page

Follow these steps for successful integration:

1. **Staging Environment Integration**:
    - Implement the OC-ID SDK in your development environment
    - Test all functionalities thoroughly
2. **Testnet Credential Issuance**:
    - Issue test credentials on the EDU chain testnet
    - Verify the issuance process and credential data accuracy
3. **Production Environment Integration**:
    - Deploy the OC-ID SDK integration to your production environment
    - Conduct rigorous testing to ensure stability
4. **Production Credential Issuance**:
    - Begin issuing live credentials on the EDU chain mainnet
    - Monitor the process closely and address any issues promptly

First of all, you have to build basic webpages, ensure that all the pages are working properly and then start integrating the OCID SSO flow.

OC Credentials are digital, verifiable credentials that adhere to the [Open Badges](https://www.imsglobal.org/spec/ob/v3p0) standard. They allow organizations to issue, manage, and display achievements and certifications on the Open Campus ID platform. 

The credentials are encrypted and stored on decentralized storage (via our partner Terminal3) and also as NFTs on the blockchain. This ensures transparency, security, and immutability.

Download it via npm here: https://www.npmjs.com/package/@opencampus/ocid-connect-js

Github documentation is here: https://github.com/opencampus-xyz/ocid-connect-js

Why do I need this?

- To integrate the product with the OpenCampus ecosystem, you need to retrieve and associate the OCIDs of your users within your system.
- The "Connect with OCID" functionality works similarly to "Login with Twitter" or "Login with Google."

How does it work?

- OCID product suite provides a JavaScript SDK that you can integrate into our site, enabling users to log into OCID with a simple button click. This SDK provides an OAuth interface to facilitate integration for our partners.
- **JavaScript-based SDK**
    - The SDK includes a JavaScript wrapper for our authentication APIs.
    - It also provides a set of React components for seamless integration into React applications.
    - Integration instructions are available in the package README on the public npm site.

Development

- A Sandbox environment is available and can be easily activated in the SDK for development purposes.
- The Sandbox environment does not require redirect_uri whitelisting, enabling you to test our integrations before going live


### **VC Issuance API**

- **Issuing Credentials:** Companies can issue credentials using the REST API provided by Open Campus. This API supports the issuance, encryption, and minting of verifiable credentials, which are then added to the recipient's OC ID.
- **API Endpoint:** The primary endpoint for issuing credentials is 

`POST https://api.vc.opencampus.xyz/issuer/vc` 

The API requires an API key for authorization and expects the credential details in JSON format.

### **OC ID Dashboard**

- **Credential Management:** The OC ID Dashboard allows users to manage and display their credentials. It includes features like filtering by credential type, toggling visibility of credentials on the public profile, and accessing detailed views of individual credentials.
- **Public Profile:** A public profile page is generated for each OC ID holder, displaying their credentials. The URL follows the format: `https://id.opencampus.xyz/profile/<OC_ID>`.

![(Desktop) OC  Credentials.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/536bfccb-fddf-4275-bd45-c273998b4130/91d7ec28-5acc-4d7e-9be6-6d5802c86f21/(Desktop)_OC__Credentials.png)

![(Desktop) Credential Details.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/536bfccb-fddf-4275-bd45-c273998b4130/b6f41647-be52-4f17-8673-ae2906b7c4ba/(Desktop)_Credential_Details.png)

# **Workflow for Integrating OC Credentials**

### **Preparation**

| **Dependency** | **Who can help you** |
| --- | --- |
| OC ID Creation: The organization must create an OC ID, which will be used as the issuer ID when generating credentials.
| OC ID Connect: You must implement OC ID Connect on your client, which will enable your users to share with you their OC ID handles / identitiers. You will need the user’s OC ID name to issue VCs to them. 
| API Key Request: Apply to get whitelisted on OC ID and obtain an API key for production access.

### **Credential Issuance Flow**

- **Step 1:** Developers test the VC issuance process on EDU Chain Testnet.
- **Step 2:** Once satisfied, they integrate the issuance API into their production environment.
- **Step 3:** Credentials are issued by sending a POST request to the VC issuance endpoint with the required data.
- **Step 4**: The resulting VC is stored on off-chain decentralized storage (IPFS) and an on-chain representation is minted on EDU Chain as an NFT

# **[Seeking Comments] VC Schema Definition**

The VC Schema defines the structure of the credentials issued by Open Campus, ensuring they are compliant with the Open Badges standard while being optimized for blockchain storage.

- **@context:** Specifies the JSON-LD context (e.g., `https://www.w3.org/2018/credentials/v1`).
    - **Type**: URI
- **ID:** A unique identifier for the credential.
    - **Type**: URI
- **Issuer:** Information about the issuing organization, including its OC ID.
    - **ID**: `<OC_ID_OF_ISSUER>`
    - **Type**: `"Organization"`
    - **Name**: `"Open Campus ID"`
- Image: URL of the image associated with the credential, e.g. `<https://example.com/profiles/johndoe.png>`
    - **Type**: URI
- **Awarded Date, Valid From, Valid To:** The date the credential was awarded, e.g., `"2024-01-01"`
    - **Type**: Date
- **Credential Subject:** Details of the recipient, including their OC ID and achievement information.

- 
    - **ID**: `<OC_ID_OF_HOLDER>`
    - **Type**: `"Person"`
    - **Name**: `"John Doe"`
    - **Email**: `"johndoe@example.com"`
    - **Profile URL**: `"<https://example.com/profiles/johndoe>"`
    - **Achievement:**
        - **ID**: `<OC_ID_OF_ISSUER:ACHIEVEMENT_ID>`
        - **Type**: `"Achievement"`
        - **Achievement Type**: `"Certification"` (ENUM: Open Badges Achievement Types)
        - **Name**: `"Blockchain Certification"`
        - **Description**: `"Completed a comprehensive blockchain certification program."`
    - **Custom Fields:**
        - Description: Custom fields that are not captured in the schema above can be inserted here. These will not be included in the NFT made available on EDU Chain.
        - Example:
            - **custom:key1**: `"custom value 1"`
            - **custom:key2**: `"custom value 2"`

### Example JSON Structure

{
  "@context": "https://www.w3.org/2018/credentials/v1",
  "id": "<VC_ID>",
  "type": ["VerifiableCredential", "OpenBadgeCredential"],
  "issuer": {
    "id": "<OC_ID_OF_ISSUER>",
    "type": "Organization",
    "name": "Open Campus ID"
  },
  "awardedDate": "2024-01-01", 
  "validFrom": "2024-01-01",
  "validTo":"2024-01-01",
  "image": "https://example.com/profiles/johndoe.png"
  "description": "Lorem Ipsum", 
  "proof": {
    "type": "<SIGNATURE_TYPE>",
    "created": "<ISOSTRONG>",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "<did:web:network.learncard.com#owner>",
    "@context": [
      "https://w3id.org/security/suites/ed25519-2020/v1"
    ],
    "proofValue": "<PROOF, e.g. 'z2gFQq6xQq7viS6r95AF5WGSysG8SMvUAUH3CPNmNFZNGBkhaZty9i2hrb5Di4CohH6DnPChuyvnLMNExjJwDxbkg'>"
  },
  "credentialSubject": {
    "id": "<OC_ID_OF_HOLDER>",
    "type": "Person",
    "name": "John Doe",
    "email": "johndoe@example.com",
    "profileUrl": "https://id.opencampus.com/profiles/johndoe.edu",
    "achievement": {
      "id": "<OC_ID_OF_ISSUER:ACHIEVEMENT_ID>",
      "type": "Achievement",
      "achievementType": "<ENUM_TYPE> or <CUSTOM_TYPE, e.g. 'ext:OC_CUSTOM:Achievement:Custom_Achievement_Type'>",
      "image": "<IMAGE_URL_OF_CREDENTIAL>",
      "name": "Blockchain Certification",
      "description": "Completed a comprehensive blockchain certification program.",
      "criteria": {
	      "narrative": "<HOW_TO_EARN_THIS_CREDENTIAL>, e.g. 'Students of Rise In are awarded this after they complete the Blockchain Fundamentals course.'"
      },
      "attachments": [ // for any generic attachments related to the achievement, like an image of the certificate
		    {
	        "url": "<URL_OF_ATTACHMENT>",
	        "type": "<ENUM_ATTACHMENT_TYPE>",
	        "title": "<NAME_OF_ATTACHMENT>"
	      }
	    ]    
    },
    "ext:OC_CUSTOM:custom": {
	    "ext:OC_CUSTOM:<OC_ID_OF_ISSUER>:key1": "custom value 1",
		  "ext:OC_CUSTOM:<OC_ID_OF_ISSUER>:key2": "custom value 2" 
	  } 
  }
}

API Technical Spec
For pre-release private beta, use our staging integration endpoint
POST https://api.vc.staging.opencampus.xyz/issuer/vc
Authorization
Once your obtained an API Key from our team, you will use your API Key in the HTTP POST header for authorization:
Header: {  X-API-KEY: <your api key> }
Secure your API Key safely, your API Key is tied to your issuer identity and losing your API Key means allowing others to issue VCs on your behalf.
Body Params (JSON)
Sample Body (raw JSON):
{
	"credentialPayload": { ... },
	"holderOcId": "bob.edu"
}
​
name
type
example
credentialPayload
object
{
    "validFrom": "2023-12-10T16:00:00.000Z",
    "awardedDate": "2023-12-10T16:00:00.000Z",
    "description": "An achievement for achieving outstanding results in mathematics course",
    "credentialSubject": {
        "id": "did:ethr:0xdc3c9e61d5dab754bf9ca2e3f5692fa10fe18fda",
        "name": "John Doe",
        "type": "Person",
        "email": "johndoe@something.edu",
        "image": "https://img.freepik.com/premium-vector/gold-medal-with-gold-ribbon-that-says-gold_1134661-43944.jpg",
        "profileUrl": "https://mycourse.xyz/profile/johndoe",
        "achievement": {
            "name": "Gold Medal Achievements",
            "identifier": "tt:1111222333",
            "description": "Reached 200 points in the intermediate mathematics",
            "achievementType": "Achievement"
        }
    }
}
holderOcId
string
bob.edu
More on Credential Payload 
Credential Payload is what you would use to represent the credential that you are issuing. We accept the following fields. Some of them are required and some of them are optional. Here we list the specifications for the credential payload based on the OpenBadge standard. 
Please refer to Schema Definition Section for explanation of specific fields. This section is dedicated to technical specification for the properties.
Top Level
Property Name
Data Type
Required
Public
Example
Remark
awardedDate
string
Y
Y
2023-09-08T16:00:00.000Z
ISO 8601 Date Format
description
string
Y
Y
my school certification
validFrom
string
Y
Y
2023-09-08T16:00:00.000Z
ISO 8601 Date Format
validUntil
string
N
Y
2023-09-08T16:00:00.000Z
ISO 8601 Date Format
image
string
N
Y
https://image.com/img/11111.jpg
Valid http uri
credentialSubject
object
Y
Y
{ … }
see below details
credentialSubject
Property Name
Data Type
Required
Public
Example
Remark
achievement
object
Y
Y
{ … }
see below details
name
string
N
N
Bob
stored but not exposed to public
email
string
N
N
bob@mycompany.xyz
stored but not exposed to public
profileUrl
string
N
Y
https://mycompany.xyz/profiles/public/11223344
this should be users public profile
image
string
N
Y
https://image.com/img/11111.jpg
Valid http uri
ext:OC_CUSTOM:custom
object
N
Y
{ … }
unspecified blob of custom data
achievement
Property Name
Data Type
Required
Public
Example
Remark
identifier
string
Y
Y
a8505caa-8e3a-4c07-aae2-94944c6b52fc
stored on-chain maxLength 50 characters
achievementType
string
Y
Y
Certificate
see appendix for valid achievement types
name
string
Y
Y
Blockchain Certification
description
string
Y
Y
An introductory blockchain bootcamp class
attachments
array
N
Y
[ { pdf: “….” , png: “….“ }, { … } ]
no standard for internal objects
Appendix: Guideline on Images
Images are essential in both giving your VC a recognizable branding as well as a vibrant display of the holder’s achievements. 
We support images at 2 levels as elaborated above:
At the Top Level of the credential payload
At the Credential Subject level 
At the Top Level
This would be an image of the logo for your institute. We recommend a square aspect ratio with no less than 1300px * 1300px in resolution for best visual presentation. 
At the Credential Subject Level
This would be an image that best represents the specific achievement represented by this credential. It can be a badge, a trophy, a certificate, a mascot … you name it. But please make sure the image DOES NOT:
Contain personal identification information that was not intended to go public.
Contain visual intellectual properties that you are not legally allowed to use or distribute.
We understand your need to have flexibility to best represent the kind of achievement specific to your program. Our guideline is follow an aspect ratio of 4:3 (for landscape) or 3:4 (for portrait) images as close as possible for the best visual result.

Appendix: Valid Achievement Types
The following list of valid achievement types is taken from OpenBadge 3.0 Standard for Achievement Types.
Achievement
ApprenticeshipCertificate
Assessment
Assignment
AssociateDegree
Award
Badge
BachelorDegree
Certificate
CertificateOfCompletion
Certification
CommunityService
Competency
Course
CoCurricular
Degree
Diploma
DoctoralDegree
Fieldwork
GeneralEducationDevelopment
JourneymanCertificate
LearningProgram
License
Membership
ProfessionalDoctorate
QualityAssuranceCredential
MasterCertificate
MasterDegree
MicroCredential
ResearchDoctorate
SecondarySchoolDiploma
​
### Next Steps


Follow these steps for successful integration:

1. **Staging Environment Integration**:
    - Implement the OC-ID SDK in your development environment
    - Test all functionalities thoroughly
2. **Testnet Credential Issuance**:
    - Issue test credentials on the EDU chain testnet
    - Verify the issuance process and credential data accuracy
3. **Production Environment Integration**:
    - Deploy the OC-ID SDK integration to your production environment
    - Conduct rigorous testing to ensure stability
4. **Production Credential Issuance**:
    - Begin issuing live credentials on the EDU chain mainnet
    - Monitor the process closely and address any issues promptly



    // Staging API key for jeezai.edu
{
    "apiKey": "e614339a-1f74-46b7-8739-f3e189f035db",
    "did": "did:key:zUC72SuYHvSa7YE6htxvyEoK9iX9M5qT3GNqvGEJmrStxXWx3h4JbgpZbFavotQ9BLyzdhT1aLHbMBrLKSPT35rTqo26UqfuCwtxAWWQWSpBNriPJ1Zk2WcLi6wcLRGJYuZwUgK",
    "ethAddress": "0xAF605EeE264506D25407E490E2858165018b929E"
}



----



@opencampus/ocid-connect-js
1.2.2 • Public • Published 13 days ago
Table of Contents
Setup
React Integration
Next.js 13+ Integration
Javascript Integration
License
Setup
yarn

Install dependencies

yarn install
Compile & build project

yarn build
Keep in mind that, if you are test OCID with localhost, it might not be able to run on Mobile Safari due to this limitation: https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto

React Integration
Properties that can be overriden

Setup Context to hook up state variables and override configuration

import { OCConnect } from '@opencampus/ocid-connect-js';

const opts = {
    redirectUri: 'http://localhost:3001/redirect',
    referralCode: 'PARTNER6'
}

return (
    <div id='app-root'>
        <OCConnect opts={opts} sandboxMode={true}>
            <RouterProvider router={ router } />
        </OCConnect>
    </div>
)
OCConnect Property

Property	Description
opts	Authentication's properties that can be overriden
sandboxMode	Connect to sandbox if it is set, default to live mode
Opts Property

Property	Description
redirectUri	URL to return after the login process is completed
referralCode	Unique identifiers assigned to partners for tracking during OCID account's registration.
Setup LoginCallBack to handle flow's result

import { LoginCallBack } from '@opencampus/ocid-connect-js';

const loginSuccess = () => {}
const loginError = () => {}

<Route path="/redirect"
    element={ <LoginCallBack errorCallback={loginError} successCallback={loginSuccess}  /> }
/>
It is possible to customize Loading & Error Page

import { LoginCallBack, useOCAuth } from '@opencampus/ocid-connect-js';

export default function CustomErrorComponent ()
{
    const { authState, ocAuth } = useOCAuth();

    return (
        <div>Error Logging in: { authState.error.message }</div>
    );
}

export default function CustomLoadingComponent ()
{
    return (
        <div>Loading....</div>
    );
}

<Route path="/redirect"
    element={
        <LoginCallBack
            customErrorComponent={CustomErrorComponent}
            customLoadingComponent={CustomLoadingComponent}
            successCallback={loginSuccess} />
    }
/>
Use useOCAuth hook to read credentials info

import { useOCAuth } from '@opencampus/ocid-connect-js';

const UserTokenPage = (props) => {
    const { authState, ocAuth, OCId, ethAddress } = useOCAuth();

    if (authState.error !== undefined) {
        return <div>Error: {authState.error.message}</div>;
    } else {
        return (
            <div>
                <h4>User Info</h4>
                <pre>
                { JSON.stringify(ocAuth.getAuthState(), null, 2) }
                </pre>
                <pre>{OCId}</pre>
                <pre>{ethAddress}</pre>
            </div>
        );
    }
};
Next Js 13+ Integration
Install dependencies

npm install @opencampus/ocid-connect-js
or

yarn add @opencampus/ocid-connect-js
1. Create a wrapper component
components/OCConnectWrapper.jsx
'use client'

import { ReactNode } from 'react';
import { OCConnect, OCConnectProps } from '@opencampus/ocid-connect-js';



export default function OCConnectWrapper({ children, opts, sandboxMode }) {
  return (
    <OCConnect opts={opts} sandboxMode={sandboxMode}>
      {children}
    </OCConnect>
  );
}
2. Update the root layout
app/layout.jsx
import OCConnectWrapper from '../components/OCConnectWrapper';

export default function RootLayout({
  children,
}) {
  const opts = {
    redirectUri: 'http://localhost:3000/redirect', // Adjust this URL
    referralCode: 'PARTNER6', // Assign partner code
  };

  return (
    <html lang="en">
      <body>
        <OCConnectWrapper opts={opts} sandboxMode={true}>
          {children}
        </OCConnectWrapper>
      </body>
    </html>
  );
}
3. Create a redirect page
app/redirect/page.jsx
'use client'

import { LoginCallBack } from '@opencampus/ocid-connect-js';
import { useRouter } from 'next/navigation';

export default function RedirectPage() {
  const router = useRouter();

  const loginSuccess = () => {
    router.push('/'); // Redirect after successful login
  };

  const loginError = (error) => {
    console.error('Login error:', error);
  };

  function CustomErrorComponent() {
  const { authState } = useOCAuth();
  return <div>Error Logging in: {authState.error?.message}</div>;
  }

  function CustomLoadingComponent() {
  return <div>Loading....</div>;
  }

  return (
    <LoginCallBack 
      errorCallback={loginError} 
      successCallback={loginSuccess}
      customErrorComponent={<CustomErrorComponent />}
      customLoadingComponent={<CustomLoadingComponent />} 
    />
  );
}
4. Create a LoginButton Component
components/LoginButton.jsx
'use client'

import { useOCAuth } from '@opencampus/ocid-connect-js';

export default function LoginButton() {
  const { ocAuth } = useOCAuth();

  const handleLogin = async () => {
    try {
      await ocAuth.signInWithRedirect({ state: 'opencampus' });
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return <button onClick={handleLogin}>Login</button>;
}
5. Use Components in Your Page
app/page.jsx
'use client';

import { useEffect } from 'react';
import LoginButton from '../components/LoginButton';
import { useOCAuth } from '@opencampus/ocid-connect-js';

export default function Home() {
  const { authState, ocAuth } = useOCAuth();

  useEffect(() => {
    console.log(authState);
  }, [authState]); // Now it will log whenever authState changes

  if (authState.error) {
    return <div>Error: {authState.error.message}</div>;
  }

  // Add a loading state
  if (authState.isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Welcome to My App</h1>
      {authState.isAuthenticated ? (
        <p>You are logged in! {JSON.stringify(ocAuth.getAuthState())}</p>
        
      ) : (
        <LoginButton />
      )}
    </div>
  );
}

**Download file here:**

[Staging_VC_Admin.postman_collection.json](https://prod-files-secure.s3.us-west-2.amazonaws.com/8ae3633d-b577-44b5-8eec-5f11c53e07fc/66823236-5643-46e7-ab2b-e491b4cc63d7/Staging_VC_Admin.postman_collection.json)

**JSON:**
{
	"info": {
		"_postman_id": "3ec22e3e-8af8-426a-a710-7206128ac0e8",
		"name": "Staging VC External",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "36434430"
	},
	"item": [
		{
			"name": "Issue VC",
			"request": {
				"method": "POST",
				"header": [
					{
						"key": "x-api-key",
						"value": "<your issuer api key>",
						"type": "text"
					},
					{
						"key": "Content-Type",
						"value": "application/json",
						"type": "text"
					}
				],
				"body": {
					"mode": "raw",
					"raw": "{\n   \"credentialPayload\": { \n    \"validFrom\": \"<starting date that this credential being valid ISO format> e.g. 2022-12-10T16:00:00.000Z\",\n    \"validUntil\": \"<ending date that this credential being valid ISO format, *do not include this field* if never expire> e.g. 2022-12-10T16:00:00.000Z\",\n    \"awardedDate\": \"<date that this credential was awarded ISO format> e.g. 2022-12-10T16:00:00.000Z\",\n    \"description\": \"<description for this category of the credential>\",\n    \"image\": \"<Image file for your institution>\",\n    \"credentialSubject\": {\n        \"name\": \"John Doe\", \n        \"type\": \"Person\", \n        \"email\": \"johndoe@something.edu\", \n        \"profileUrl\": \"https://id.staging.opencampus.xyz/public/credentials?username=johndoe.edu\",\n        \"image\": \"<image file link to any image relevant to this particular credential>\",\n        \"achievement\": {\n            \"identifier\": \"<an identifier for this achievement, other can take this to validate with you, max 50 characters>\",\n            \"achievementType\": \"<valid achievement type based on integration guide, e.g. Course>\",\n            \"name\": \"<name of the achievement>\",\n            \"description\": \"<description specific to this achievement>\"\n        }\n     }\n    },\n    \"holderOcId\": \"<holder's valid OCID>\"\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "https://api.vc.staging.opencampus.xyz/issuer/vc",
					"protocol": "https",
					"host": [
						"api",
						"vc",
						"staging",
						"opencampus",
						"xyz"
					],
					"path": [
						"issuer",
						"vc"
					]
				}
			},
			"response": []
		}
	]
}