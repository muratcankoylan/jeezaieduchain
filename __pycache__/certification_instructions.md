VC Schema Definition 
The VC Schema defines the structure of the credentials issued by Open Campus, ensuring they are compliant with the Open Badges standard while being optimized for blockchain storage.
@context: Specifies the JSON-LD context (e.g., https://www.w3.org/2018/credentials/v1).
Type: URI
ID: A unique identifier for the credential.
Type: URI
Issuer: Information about the issuing organization, including its OC ID.
ID: <OC_ID_OF_ISSUER>
Type: "Organization"
Name: "Open Campus ID"
Image: URL of the image associated with the credential, e.g. <https://example.com/profiles/johndoe.png>
Type: URI
Awarded Date, Valid From, Valid To: The date the credential was awarded, e.g., "2024-01-01"
Type: Date
Credential Subject: Details of the recipient, including their OC ID and achievement information.
ID: <OC_ID_OF_HOLDER>
Type: "Person"
Name: "John Doe"
Email: "johndoe@example.com"
Profile URL: "<https://example.com/profiles/johndoe>"
Achievement: 
ID: <OC_ID_OF_ISSUER:ACHIEVEMENT_ID>
Type: "Achievement"
Achievement Type: "Certification" (ENUM: Open Badges Achievement Types)
Name: "Blockchain Certification"
Description: "Completed a comprehensive blockchain certification program."
 Custom Fields:
Description: Custom fields that are not captured in the schema above can be inserted here. These will not be included in the NFT made available on EDU Chain. 
Example: 
custom:key1: "custom value 1"
custom:key2: "custom value 2"
Example JSON Structure
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
​
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