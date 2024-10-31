import { OCAuthSandbox } from '@opencampus/ocid-connect-js';

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing OCID Connect...');
    
    // Initialize OCID Connect with Sandbox environment
    const ocidLoginBtn = document.getElementById('ocidLoginBtn');
    
    if (!ocidLoginBtn) {
        console.error('OCID login button not found! Make sure the button has id="ocidLoginBtn"');
        return;
    }

    try {
        // Initialize OCID Connect with Sandbox environment
        const ocAuth = new OCAuthSandbox({
            redirectUri: window.location.origin + '/callback',
            referralCode: 'PARTNER6'
        });
        console.log('OCID Connect initialized successfully');

        // Add click handler to login button
        ocidLoginBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            console.log('OCID login button clicked');
            
            try {
                console.log('Initiating OCID login redirect...');
                await ocAuth.signInWithRedirect({
                    state: 'opencampus'
                });
            } catch (error) {
                console.error('OCID login redirect error:', error);
                alert('Login failed. Please try again.');
            }
        });

    } catch (error) {
        console.error('Error initializing OCID Connect:', error);
        ocidLoginBtn.disabled = true;
        alert('Failed to initialize login. Please refresh the page and try again.');
    }
});

async function handleCallback(ocAuth) {
    try {
        console.log('Handling callback...');
        const authState = await ocAuth.handleLoginRedirect();
        console.log('Auth state:', authState);
        
        if (authState.idToken) {
            console.log('Login successful, sending auth data to server...');
            // Send the auth data to our server
            const response = await fetch('/callback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    idToken: authState.idToken,
                    accessToken: authState.accessToken,
                    OCId: authState.OCId,
                    ethAddress: authState.ethAddress
                })
            });

            if (response.ok) {
                window.location.href = '/profile';
            } else {
                throw new Error('Server authentication failed');
            }
        } else {
            console.log('Login incomplete');
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error handling callback:', error);
        window.location.href = '/login';
    }
} 