from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from typing import Dict, List, Optional

class FormFiller:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'LOT AI/1.0'})

    def detect_forms(self, url: str) -> List[Dict]:
        try:
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            forms = []
            
            for form in soup.find_all('form'):
                form_id = form.get('id', form.get('name', 'unnamed_form'))
                action = form.get('action', '')
                method = form.get('method', 'get').upper()
                fields = []
                
                for input_tag in form.find_all(['input', 'textarea', 'select']):
                    name = input_tag.get('name')
                    if not name:
                        continue
                    field_type = input_tag.get('type', 'text') if input_tag.name == 'input' else input_tag.name
                    required = input_tag.get('required') is not None
                    
                    # Try to find associated label
                    label = ""
                    if input_tag.get('id'):
                        label_tag = soup.find('label', {'for': input_tag.get('id')})
                        if label_tag:
                            label = label_tag.get_text(strip=True)
                            
                    fields.append({
                        "name": name,
                        "type": field_type,
                        "required": required,
                        "label": label
                    })
                    
                forms.append({
                    "form_id": form_id,
                    "action": action,
                    "method": method,
                    "fields": fields
                })
            return forms
        except Exception:
            return []

    def fill_form(self, url: str, form_data: Dict, submit: bool = False) -> Dict:
        if not submit:
            return {"success": False, "response_url": "", "errors": ["Submit flag is false"]}
            
        try:
            resp = self.session.post(url, data=form_data, timeout=15)
            if resp.ok:
                return {"success": True, "response_url": resp.url, "errors": []}
            return {"success": False, "response_url": resp.url, "errors": [f"Status code {resp.status_code}"]}
        except Exception as e:
            return {"success": False, "response_url": "", "errors": [str(e)]}

    def login(self, url: str, username: str, password: str, username_selector: str = None, password_selector: str = None) -> Dict:
        try:
            # We would typically parse the page to get CSRF tokens if needed
            resp = self.session.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # This is a naive login attempt, real implementations would need CSRF and action URL handling
            data = {
                username_selector or 'username': username,
                password_selector or 'password': password
            }
            
            login_url = url # Assuming self-posting form
            post_resp = self.session.post(login_url, data=data, timeout=15)
            
            success = post_resp.ok and 'login' not in post_resp.url.lower()
            return {
                "success": success,
                "session_cookies": self.session.cookies.get_dict()
            }
        except Exception:
            return {"success": False, "session_cookies": {}}

    def submit_contact_form(self, url: str, name: str, email: str, message: str) -> Dict:
        forms = self.detect_forms(url)
        if not forms:
            return {"success": False, "confirmation": "No form found"}
            
        # Very naive mapping
        form_data = {
            'name': name,
            'email': email,
            'message': message
        }
        
        target_form = forms[0]
        action_url = urljoin(url, target_form['action']) if target_form['action'] else url
        
        return self.fill_form(action_url, form_data, submit=True)

def inject_form_filler_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[LOT AI Directive]: You have an autonomous Form Filler agent. You can parse pages to detect forms and submit data securely."
