from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import requests
from config import Config
from utils.credentials import CredentialIssuer
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your-secret-key'  # Change this to a secure secret key
app.permanent_session_lifetime = timedelta(days=7)  # Set session lifetime

credential_issuer = CredentialIssuer(
    api_key=app.config['OCID_API_KEY'],
    environment=app.config['OCID_ENVIRONMENT']
)

def get_ocid_user_info(access_token):
    """Fetch user info from OCID using the access token"""
    user_info_url = 'https://api.vc.staging.opencampus.xyz/user/info'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-API-KEY': app.config['OCID_API_KEY']
    }
    print("Fetching user info with headers:", headers)  # Debug log
    
    try:
        response = requests.get(user_info_url, headers=headers)
        print("User info response status:", response.status_code)  # Debug log
        print("User info response:", response.text)  # Debug log
        
        if response.ok:
            return response.json()
        else:
            print(f"Failed to get user info: {response.text}")  # Debug log
            return None
    except Exception as e:
        print(f"Exception in get_ocid_user_info: {str(e)}")  # Debug log
        return None

@app.route('/')
@app.route('/login')
def login():
    try:
        if 'user' in session:
            return redirect(url_for('profile'))
        return render_template('login.html')
    except Exception as e:
        print(f"Error in login route: {str(e)}")
        flash('An error occurred. Please try again.', 'error')
        return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        # Decode the ID token to get user info
        id_token = session['user'].get('id_token')
        user_info = jwt.decode(id_token, options={"verify_signature": False})
        
        print("Decoded user info:", user_info)  # Debug log to see all available fields
        
        # Get the edu_username and format it nicely
        edu_username = user_info.get('edu_username', '')
        eth_address = user_info.get('eth_address', '')
        
        # Update session with user info
        session['user'].update({
            'name': user_info.get('name', edu_username.split('.')[0].title()),
            'eth_address': eth_address,
            'ocid': edu_username,
            'user_id': user_info.get('user_id'),
            'login_type': user_info.get('login_type', 'wallet'),
            'profile_url': f"https://id.staging.opencampus.xyz/profile/{edu_username}",
            'achievements': user_info.get('achievements', []),
            'image': user_info.get('image', 'https://img.freepik.com/premium-vector/blockchain-technology-background-with-gradient-blue-circuit-lines_29971-1143.jpg')  # Add default blockchain-themed image
        })
        
        print("Updated user session:", session['user'])
        return render_template('profile.html', user=session['user'])
        
    except Exception as e:
        print(f"Error decoding token: {str(e)}")
        return render_template('profile.html', user=session['user'])

@app.route('/course-success')
def course_success():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    course_data = {
        'id': 'COURSE-001',
        'name': 'AI Agents for Algorithmic Trading',
        'completion_date': datetime.utcnow().strftime('%Y-%m-%d')
    }
    return render_template('course_success.html', course=course_data)

@app.route('/certification')
def certification():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        credentials = credential_issuer.get_user_credentials(session['user']['ocid'])
        return render_template('certification.html', 
                             credentials=credentials,
                             user=session['user'])  # Pass user data to access eth_address
    except Exception as e:
        flash(f'Failed to fetch credentials: {str(e)}', 'error')
        return render_template('certification.html', 
                             credentials={'data': [], 'profile_url': ''},
                             user=session['user'])

@app.route('/callback', methods=['GET', 'POST'])
def ocid_callback():
    print("Callback route accessed with method:", request.method)  # Debug log
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received auth data:", data)  # Debug log

            # Store user info in session
            session['user'] = {
                'ocid': data.get('OCId'),
                'access_token': data.get('accessToken'),
                'id_token': data.get('idToken'),
                'eth_address': data.get('ethAddress')
            }
            print("User session created:", session['user'])  # Debug log

            return jsonify({'success': True})

        except Exception as e:
            print(f"Error in OCID callback POST: {str(e)}")  # Debug log
            return jsonify({'error': str(e)}), 400
    
    # Handle GET request (initial redirect from OCID)
    print("Rendering callback template with params:", request.args)  # Debug log
    return render_template('callback.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/issue-credential', methods=['POST'])
def issue_credential():
    print("Issue credential route accessed")
    
    if 'user' not in session:
        print("User not authenticated")
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        achievement_data = {
            'id': request.form['achievement_id'],
            'name': request.form['name'],
            'type': request.form['type'],
            'description': 'Successfully completed AI Agents for Algorithmic Trading - A comprehensive course on developing autonomous AI agents for financial markets.',
            'criteria': 'Successfully completed all course modules, implemented trading algorithms, and passed the final assessment with distinction.'
        }
        print("Achievement data:", achievement_data)

        print("Issuing credential to:", session['user']['ocid'])
        result = credential_issuer.issue_credential(
            holder_ocid=session['user']['ocid'],
            achievement_data=achievement_data
        )
        print("Credential issued:", result)

        flash('Credential issued successfully!', 'success')
        return jsonify(result)

    except Exception as e:
        print(f"Error issuing credential: {str(e)}")
        flash(f'Failed to issue credential: {str(e)}', 'error')
        return jsonify({'error': str(e)}), 400

@app.route('/credential/<credential_id>')
def get_credential_details(credential_id):
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    try:
        # Fetch specific credential details from OCID API
        response = requests.get(
            f'{credential_issuer.base_url}/credential/{credential_id}',
            headers={'X-API-KEY': app.config['OCID_API_KEY']}
        )
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/profile/setup', methods=['GET', 'POST'])
def profile_setup():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Update user profile with additional information
            profile_data = {
                'display_name': request.form.get('display_name'),
                'bio': request.form.get('bio'),
                'interests': request.form.getlist('interests'),
                'education': request.form.get('education'),
                'occupation': request.form.get('occupation')
            }
            
            # Store profile data in session
            session['user'].update(profile_data)
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
            
        except Exception as e:
            flash('Failed to update profile', 'error')
            return render_template('profile_setup.html', user=session['user'])
    
    return render_template('profile_setup.html', user=session['user'])

@app.route('/progress')
def learning_progress():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        # Fetch user's learning progress
        progress_data = {
            'completed_modules': [
                {
                    'id': 'MOD001',
                    'name': 'Introduction to AI Trading',
                    'completion_date': '2024-03-15',
                    'score': 95
                }
            ],
            'current_module': {
                'id': 'MOD002',
                'name': 'Advanced Trading Strategies',
                'progress': 65,
                'next_lesson': 'Market Analysis Techniques'
            },
            'achievements': session['user'].get('achievements', []),
            'total_progress': 45  # Percentage of overall course completion
        }
        
        return render_template('progress.html', 
                             progress=progress_data,
                             user=session['user'])
    except Exception as e:
        flash('Failed to load progress data', 'error')
        return redirect(url_for('profile'))

@app.route('/credentials/manage')
def manage_credentials():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        # Fetch all credentials (both claimed and unclaimed)
        all_credentials = credential_issuer.get_user_credentials(session['user']['ocid'])
        
        # Separate credentials by status
        claimed_credentials = [c for c in all_credentials.get('data', []) if c.get('status') == 'claimed']
        pending_credentials = [c for c in all_credentials.get('data', []) if c.get('status') == 'pending']
        
        return render_template('manage_credentials.html',
                             claimed_credentials=claimed_credentials,
                             pending_credentials=pending_credentials,
                             user=session['user'])
    except Exception as e:
        flash('Failed to load credentials', 'error')
        return redirect(url_for('profile'))

@app.route('/credentials/claim/<credential_id>', methods=['POST'])
def claim_credential(credential_id):
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        result = credential_issuer.claim_credential(
            credential_id=credential_id,
            holder_ocid=session['user']['ocid']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 