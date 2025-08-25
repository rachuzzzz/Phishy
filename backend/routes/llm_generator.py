from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
import httpx
import logging
from typing import Optional, Dict, Any, List
import json
import asyncio
from pathlib import Path
import re
import base64

router = APIRouter()
logger = logging.getLogger(__name__)

class OllamaClient:
    """Enhanced client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "phi3:mini"
        self.timeout = 120.0
        
    async def check_service(self) -> Dict[str, Any]:
        """Check if Ollama service is available and get model info"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                
                tags_data = response.json()
                models = tags_data.get("models", [])
                
                phi3_available = any("phi3" in model.get("name", "") for model in models)
                
                return {
                    "service_available": True,
                    "models_available": [model.get("name") for model in models],
                    "phi3_available": phi3_available,
                    "recommended_model": self.model if phi3_available else models[0].get("name") if models else None
                }
                
        except Exception as e:
            logger.warning(f"Ollama service check failed: {e}")
            return {
                "service_available": False,
                "error": str(e),
                "models_available": [],
                "phi3_available": False
            }
    
    async def generate_completion(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Generate completion using Phi-3 Mini via Ollama"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                        "top_p": 0.9,
                        "stop": ["```", "---END---", "\n\n\n"]  # Stop tokens to prevent overly long responses
                    }
                }
                
                logger.info(f"Sending request to Ollama: {self.model}")
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                generated_text = result.get("response", "").strip()
                
                logger.info(f"Generated text length: {len(generated_text)} characters")
                return generated_text
                
        except httpx.TimeoutException:
            logger.error("Ollama API timeout")
            raise HTTPException(status_code=504, detail="LLM service timeout - try reducing complexity or wait for service to respond")
        except httpx.RequestError as e:
            logger.error(f"Ollama API connection error: {e}")
            raise HTTPException(status_code=503, detail="LLM service unavailable - ensure Ollama is running")
        except Exception as e:
            logger.error(f"Unexpected error in LLM generation: {e}")
            raise HTTPException(status_code=500, detail=f"Internal LLM error: {str(e)}")

# Initialize Ollama client
ollama_client = OllamaClient()

# Phishing email scenarios
PHISHING_SCENARIOS = {
    "account_security": {
        "context": "urgent account security notification requiring immediate verification",
        "urgency": "suspicious login detected - immediate action required",
        "threat": "account will be locked if not verified within 24 hours",
        "subject_templates": [
            "Urgent: Suspicious Activity Detected",
            "Security Alert: Verify Your Account",
            "Action Required: Account Security Issue"
        ]
    },
    "payment_issue": {
        "context": "payment processing problem requiring user intervention", 
        "urgency": "payment failure needs immediate resolution",
        "threat": "services may be suspended if payment issue not resolved",
        "subject_templates": [
            "Payment Failed - Action Required",
            "Billing Issue: Update Payment Method",
            "Account Suspension Notice"
        ]
    },
    "system_update": {
        "context": "mandatory system update or policy change",
        "urgency": "compliance deadline approaching",
        "threat": "service disruption if update not completed",
        "subject_templates": [
            "Mandatory System Update Required",
            "Policy Update: Action Required",
            "System Maintenance - Verify Account"
        ]
    },
    "reward_notification": {
        "context": "special offer or reward that expires soon",
        "urgency": "limited time offer expires today",
        "threat": "miss out on exclusive opportunity",
        "subject_templates": [
            "Congratulations! You've Won",
            "Exclusive Offer - Expires Today",
            "Claim Your Reward Now"
        ]
    },
    "it_support": {
        "context": "IT department requesting user action",
        "urgency": "security patch requires immediate installation",
        "threat": "system vulnerability if not patched",
        "subject_templates": [
            "IT Security: Action Required",
            "Critical Security Update",
            "System Patch - Install Now"
        ]
    }
}

def create_phishing_prompt(user_email: str, scenario_type: str = "account_security", custom_topic: Optional[str] = None) -> str:
    """Create a structured prompt for generating phishing emails"""
    
    user_name = user_email.split('@')[0].title()
    domain = user_email.split('@')[1] if '@' in user_email else "company.com"
    
    # Use custom topic if provided, otherwise use predefined scenario
    if custom_topic:
        prompt = f"""Generate a realistic, professional phishing email for cybersecurity training purposes.

IMPORTANT: This is for employee security awareness training - NOT for malicious use.

CUSTOM TOPIC: {custom_topic}

TARGET DETAILS:
- Target Email: {user_email}
- User Name: {user_name}
- Domain: {domain}

ENHANCED REQUIREMENTS:
1. PROFESSIONAL CORPORATE TONE - Use formal business language appropriate for {domain}
2. STRUCTURED PARAGRAPHS - Write in clear, well-separated paragraphs (3-4 paragraphs)
3. DETAILED CONTEXT - Provide specific background information and context
4. COMPELLING NARRATIVE - Create a believable story with specific details
5. PROFESSIONAL FORMATTING - Use proper email structure with clear sections
6. PSYCHOLOGICAL TECHNIQUES - Use authority, urgency, social proof, and specificity
7. REALISTIC DETAILS - Include specific names, dates, policies, or procedures
8. CLEAR CALL-TO-ACTION - Include [CLICK_HERE] placeholder for the action link
9. LONGER CONTENT - Write 200-300 words for more detailed, professional emails
10. HTML-READY - Structure for professional email formatting

ENHANCED WRITING STYLE:
- Use industry-specific terminology and jargon
- Include specific policy numbers, dates, or reference codes
- Mention real-sounding departments, systems, or contacts
- Create urgency with specific deadlines and consequences
- Add credibility with technical details and processes

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
Subject: [Write a compelling, professional subject line related to {custom_topic}]

Dear {user_name},

[PARAGRAPH 1: Professional greeting and context introduction with specific background]

[PARAGRAPH 2: Detailed explanation of the situation with specific information and urgency]

[PARAGRAPH 3: Clear consequences and action required with specific timeline]

[PARAGRAPH 4: Call-to-action with [CLICK_HERE] and additional instructions or reassurance]

Best regards,
[Professional signature with title, department, and contact information]

GENERATE THE ENHANCED PHISHING EMAIL NOW:"""
        return prompt
    
    # Use predefined scenario
    scenario = PHISHING_SCENARIOS.get(scenario_type, PHISHING_SCENARIOS["account_security"])
    
    prompt = f"""Generate a realistic phishing email for cybersecurity training purposes.

IMPORTANT: This is for employee security awareness training - NOT for malicious use.

SCENARIO DETAILS:
- Type: {scenario_type.replace('_', ' ').title()}
- Context: {scenario['context']}
- Target: {user_email}
- User Name: {user_name}
- Domain: {domain}
- Urgency Factor: {scenario['urgency']}
- Threat Element: {scenario['threat']}

REQUIREMENTS:
1. Professional business tone appropriate for {domain}
2. Create urgency without being obviously suspicious
3. Include a clear call-to-action with [CLICK_HERE] as the placeholder for the verification link
4. Use psychological manipulation techniques (authority, urgency, fear)
5. Make it believable but educational
6. Keep the email body under 150 words
7. Include a realistic subject line
8. Use proper email formatting

PSYCHOLOGICAL TECHNIQUES TO INCLUDE:
- Authority: Reference legitimate-sounding departments or systems
- Urgency: Create time pressure
- Social proof: Mention that others have already taken action
- Fear: Mention consequences of inaction

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
Subject: [Write a compelling subject line here]

Dear {user_name},

[Write the email body here. Include [CLICK_HERE] where the verification link should go]

[Professional signature]

GENERATE THE PHISHING EMAIL NOW:"""

    return prompt

def generate_fallback_email(user_email: str, action_id: str, link: str, scenario_type: str = "account_security") -> str:
    """Enhanced fallback template when LLM is unavailable"""
    
    scenario = PHISHING_SCENARIOS.get(scenario_type, PHISHING_SCENARIOS["account_security"])
    user_name = user_email.split('@')[0].title()
    domain = user_email.split('@')[1] if '@' in user_email else "company.com"
    
    templates = {
        "account_security": f"""Subject: [URGENT] Security Verification Required - Account Access Suspended

Dear {user_name},

I hope this message finds you well. I am writing to inform you of a critical security matter that requires your immediate attention regarding your {domain} account.

Our advanced threat detection systems have identified multiple unauthorized access attempts on your account from suspicious IP addresses across different geographic locations. These attempts occurred between 2:15 AM and 4:30 AM today, which is outside your typical usage patterns. As part of our enhanced security protocols implemented under Policy SEC-2024-11, we have temporarily restricted certain account functions to protect your sensitive information and prevent potential data breaches.

The security analysis indicates that malicious actors may have obtained partial credential information, possibly through recent phishing campaigns targeting our user base. To ensure the integrity of your account and prevent unauthorized access to your personal data, financial information, and connected services, you must complete our enhanced verification process within the next 24 hours. Failure to complete this verification will result in a full account suspension until identity can be confirmed through our manual review process, which typically takes 5-7 business days.

Please complete the security verification immediately by clicking here: {link}

This secure verification portal will guide you through a brief identity confirmation process and help us restore full access to your account. The process takes approximately 3-5 minutes and includes verification of your contact information and recent account activity. For your security, this link will expire in 24 hours.

Best regards,
Sarah Mitchell
Senior Security Analyst
{domain.split('.')[0].title()} Cybersecurity Operations Center
Phone: +1-800-{domain.split('.')[0].upper()}-SEC
Reference: SEC-{action_id}""",

        "payment_issue": f"""Subject: [ACTION REQUIRED] Payment Processing Failure - Service Interruption Notice

Dear {user_name},

Thank you for being a valued {domain} customer. I am contacting you regarding an urgent billing matter that requires your immediate attention to prevent service disruption.

Our payment processing system attempted to charge your registered payment method for your monthly subscription on {action_id[:8]} but encountered a processing failure. This may be due to an expired card, insufficient funds, changed billing address, or enhanced fraud protection measures implemented by your financial institution. According to our billing policy BP-2024-07, services will be automatically suspended if payment issues are not resolved within 48 hours of initial notification.

Your current subscription includes premium features and cloud storage that will be immediately affected by any service suspension. Additionally, any automated backup processes, scheduled reports, and team collaboration features will be discontinued until payment is successfully processed. Please note that suspended accounts may lose access to certain data recovery options after 72 hours.

To prevent service interruption and maintain access to your account, please update your payment information immediately by visiting our secure billing portal: {link}

Our secure payment system accepts all major credit cards, PayPal, and direct bank transfers. The update process is protected by 256-bit SSL encryption and typically takes 2-3 minutes to complete. Once updated, your services will be automatically restored within 15 minutes.

If you have any questions or need assistance, please contact our billing support team at billing@{domain} or call 1-800-{domain.split('.')[0].upper()}-BILL.

Best regards,
Michael Rodriguez
Senior Billing Specialist
{domain.split('.')[0].title()} Customer Success Team
Billing Reference: BP-{action_id}""",

        "system_update": f"""Subject: {scenario['subject_templates'][0]}

Dear {user_name},

A critical system update requires your immediate attention. All {domain} users must complete this security update by end of day.

Complete the update here: {link}

Failure to complete this update may result in service interruption.

IT Department
{domain.split('.')[0].title()}

Update ID: {action_id}""",
        
        "reward_notification": f"""Subject: {scenario['subject_templates'][0]}

Dear {user_name},

Congratulations! You have been selected for an exclusive {domain.split('.')[0].title()} customer reward program.

Your reward includes:
- Exclusive access to premium features
- 50% discount on services
- Priority customer support

Claim your reward before it expires: {link}

This offer is valid for 48 hours only and is non-transferable.

{domain.split('.')[0].title()} Customer Success Team
Reward Code: {action_id}""",

        "it_support": f"""Subject: {scenario['subject_templates'][0]}

Dear {user_name},

Our IT department has identified a critical security vulnerability that requires immediate patching on all {domain} systems.

URGENT: Please install the security patch by clicking here: {link}

This update must be completed within 2 hours to prevent potential security breaches.

IT Security Team
{domain.split('.')[0].title()}

Patch ID: {action_id}"""
    }
    
    return templates.get(scenario_type, templates["account_security"])

def insert_tracking_url(email_content: str, track_url: str) -> str:
    """
    FIXED: Intelligent tracking URL insertion with multiple fallback strategies
    """
    original_content = email_content
    
    # Strategy 1: Replace common placeholder patterns
    placeholder_patterns = [
        "{{TRACKING_LINK}}",
        "{TRACKING_LINK}",
        "[CLICK_HERE]",
        "[TRACKING_LINK]", 
        "TRACKING_LINK",
        "{{tracking_link}}",
        "{tracking_link}",
        "[tracking_link]",
        "[VERIFICATION_LINK]",
        "[ACTION_LINK]"
    ]
    
    for placeholder in placeholder_patterns:
        if placeholder in email_content:
            email_content = email_content.replace(placeholder, track_url)
            logger.info(f"Replaced placeholder '{placeholder}' with tracking URL")
            return email_content
    
    # Strategy 2: Replace "click here" phrases (case insensitive)
    click_patterns = [
        r'\bclick here\b',
        r'\bclick the link\b',
        r'\bfollowing link\b',
        r'\blink below\b',
        r'\bthis link\b'
    ]
    
    for pattern in click_patterns:
        if re.search(pattern, email_content, re.IGNORECASE):
            email_content = re.sub(
                pattern, 
                lambda m: f"{m.group()}: {track_url}",
                email_content, 
                flags=re.IGNORECASE,
                count=1  # Only replace the first occurrence
            )
            logger.info(f"Enhanced 'click here' pattern with tracking URL")
            return email_content
    
    # Strategy 3: Find "verify" or "update" and insert link after
    action_patterns = [
        (r'(verify[^.]*)', f'\\1\n\nVerification Link: {track_url}'),
        (r'(update[^.]*)', f'\\1\n\nUpdate Link: {track_url}'),
        (r'(complete[^.]*)', f'\\1\n\nCompletion Link: {track_url}'),
        (r'(secure[^.]*)', f'\\1\n\nSecure Access: {track_url}'),
        (r'(login[^.]*)', f'\\1\n\nLogin Here: {track_url}')
    ]
    
    for pattern, replacement in action_patterns:
        if re.search(pattern, email_content, re.IGNORECASE):
            email_content = re.sub(
                pattern, 
                replacement,
                email_content, 
                flags=re.IGNORECASE,
                count=1
            )
            logger.info(f"Inserted tracking URL after action word")
            return email_content
    
    # Strategy 4: Insert before signature (look for common signature patterns)
    signature_patterns = [
        r'(Best regards,)',
        r'(Sincerely,)',
        r'(Thank you,)',
        r'(IT Department)',
        r'(Security Team)',
        r'(\w+ Team)'
    ]
    
    for pattern in signature_patterns:
        if re.search(pattern, email_content, re.IGNORECASE):
            email_content = re.sub(
                pattern,
                f'Take Action: {track_url}\n\n\\1',
                email_content,
                flags=re.IGNORECASE,
                count=1
            )
            logger.info(f"Inserted tracking URL before signature")
            return email_content
    
    # Strategy 5: Last resort - append at the end
    if track_url not in email_content:
        email_content += f"\n\nAction Required: {track_url}"
        logger.warning("Used fallback: appended tracking URL at end")
    
    return email_content

def generate_tracking_id():
    """Generate a unique tracking ID"""
    return f"track-{uuid4().hex[:12]}"

def generate_tracking_url(user_email: str, action_id: str, campaign_id: str = None, base_url: str = None):
    """Generate a tracking pixel URL for an email"""
    import os
    # Use environment variable or provided base_url, fallback to localhost
    if base_url is None:
        base_url = os.getenv("BASE_URL", "http://localhost:8080")
    
    tracking_id = generate_tracking_id()
    
    params = [
        f"user_email={user_email}",
        f"action={action_id}"
    ]
    
    if campaign_id:
        params.append(f"campaign={campaign_id}")
    
    return f"{base_url}/email-track/pixel/{tracking_id}?" + "&".join(params)

def convert_to_html_email(email_content: str) -> str:
    """Convert plain text email to professional HTML format"""
    lines = email_content.split('\n')
    html_lines = []
    
    in_body = False
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines in processing but add them as breaks
        if not line:
            if in_body:
                html_lines.append('<br>')
            continue
            
        # Handle subject line
        if line.startswith('Subject:'):
            subject = line.replace('Subject:', '').strip()
            continue
            
        # Handle greeting
        if line.startswith('Dear '):
            in_body = True
            html_lines.append(f'<p style="margin-bottom: 16px;"><strong>{line}</strong></p>')
            continue
            
        # Handle signature/closing
        if any(closing in line.lower() for closing in ['best regards', 'sincerely', 'thank you', 'yours truly']):
            html_lines.append('<br>')
            html_lines.append(f'<p style="margin-top: 20px; margin-bottom: 8px;"><strong>{line}</strong></p>')
            continue
            
        # Handle regular content paragraphs
        if in_body:
            # Check if it's a name/title line (usually short, no punctuation)
            if len(line) < 50 and not line.endswith('.') and not line.startswith('http'):
                html_lines.append(f'<p style="margin-bottom: 4px;"><em>{line}</em></p>')
            else:
                html_lines.append(f'<p style="margin-bottom: 12px; line-height: 1.5;">{line}</p>')
    
    # Wrap in professional HTML structure
    html_email = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #007bff;">
            {''.join(html_lines)}
        </div>
        <div style="margin-top: 20px; padding: 15px; background-color: #f1f3f4; border-radius: 4px; font-size: 12px; color: #666;">
            <p style="margin: 0;"><strong>Security Notice:</strong> This email was sent as part of a cybersecurity awareness training exercise. If you received this email unexpectedly, please report it to your IT security team.</p>
        </div>
    </body>
    </html>
    """
    
    return html_email

def add_tracking_pixel_to_email(email_content: str, tracking_url: str) -> str:
    """Add invisible tracking pixel to email content"""
    # Create tracking pixel HTML
    pixel_html = f'<img src="{tracking_url}" width="1" height="1" style="display:none;" alt="" />'
    
    # Try to insert before closing </body> tag
    if '</body>' in email_content.lower():
        return email_content.replace('</body>', f'{pixel_html}</body>')
    
    # Try to insert before closing </html> tag
    if '</html>' in email_content.lower():
        return email_content.replace('</html>', f'{pixel_html}</html>')
    
    # If no HTML structure, append at the end
    return email_content + pixel_html

class EmailGenRequest(BaseModel):
    user_email: str = Field(..., description="Target user email address")
    scenario_type: Optional[str] = Field("account_security", description="Type of phishing scenario")
    custom_topic: Optional[str] = Field(None, description="Custom topic for flexible email generation - overrides scenario_type")
    use_llm: Optional[bool] = Field(True, description="Whether to use LLM for generation")
    include_tracking_pixel: Optional[bool] = Field(True, description="Whether to include tracking pixel for email opens")
    html_format: Optional[bool] = Field(True, description="Whether to generate HTML formatted email")
    campaign_id: Optional[str] = Field(None, description="Campaign ID for tracking purposes")
    temperature: Optional[float] = Field(0.7, ge=0.1, le=1.0, description="LLM creativity level")
    max_tokens: Optional[int] = Field(300, ge=50, le=500, description="Maximum tokens for LLM generation")

class EmailResponse(BaseModel):
    email: str
    action_id: str
    track_url: str
    tracking_pixel_url: Optional[str] = None
    email_content: str
    email_content_with_pixel: Optional[str] = None
    email_content_html: Optional[str] = None
    email_content_html_with_pixel: Optional[str] = None
    generated_at: str
    generation_method: str
    scenario_type: str
    model_used: Optional[str] = None
    generation_time_ms: Optional[int] = None

# NEW: General Chat Classes and Endpoint
class ChatRequest(BaseModel):
    message: str = Field(..., description="User message for general chat")
    temperature: Optional[float] = Field(0.7, ge=0.1, le=1.0, description="LLM creativity level")
    max_tokens: Optional[int] = Field(500, ge=50, le=1000, description="Maximum tokens for response")

class ChatResponse(BaseModel):
    response: str
    model_used: str
    generation_time_ms: int
    timestamp: str

@router.post("/chat", response_model=ChatResponse)
async def general_chat(request: ChatRequest):
    """
    General chat endpoint for non-phishing conversations
    
    Allows users to have normal conversations with Phi-3 Mini as Phishy.
    """
    start_time = datetime.utcnow()
    
    try:
        # Create a comprehensive educational prompt
        prompt = f"""You are an expert cybersecurity assistant with deep knowledge of phishing, social engineering, and security awareness training. Your role is to provide comprehensive, educational responses that help users understand cybersecurity concepts thoroughly.

When answering questions:
- Provide detailed, educational explanations
- Include specific examples and context when relevant
- Focus on helping users learn and understand concepts deeply
- Use clear, professional language that teaches rather than just informs
- For greetings, respond naturally and ask how you can help with cybersecurity questions
- For technical questions, provide thorough explanations with practical insights

Your expertise covers:
- Phishing techniques and detection methods
- Social engineering tactics and prevention
- Cybersecurity best practices and implementation
- Threat analysis and risk assessment
- Security awareness training and education

User question: {request.message}

Please provide a comprehensive, educational response:"""
        
        # Generate response using Phi-3 Mini via Ollama
        llm_response = await ollama_client.generate_completion(
            prompt, 
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        logger.info(f"Successfully generated chat response using {ollama_client.model}")
        
        return ChatResponse(
            response=llm_response.strip(),
            model_used=ollama_client.model,
            generation_time_ms=generation_time,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (these are already properly formatted)
        raise
    except Exception as e:
        # If LLM fails, provide a helpful fallback response
        logger.warning(f"LLM chat failed: {e}")
        generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        return ChatResponse(
            response=f"Hi! I'm Phishy, your AI cybersecurity assistant. I'm sorry, but I'm having trouble connecting to my AI service right now. However, I can still help you generate phishing emails for training, analyze security data, or provide system information. Please try asking about cybersecurity topics, phishing simulation, or check if Ollama is running properly with Phi-3 Mini.",
            model_used="fallback",
            generation_time_ms=generation_time,
            timestamp=datetime.utcnow().isoformat()
        )

@router.post("/generate-email", response_model=EmailResponse)
async def generate_email(request: EmailGenRequest):
    """
    FIXED: Generate phishing simulation email using Phi-3 Mini or fallback template
    
    Creates realistic phishing emails for security awareness training with various scenarios or custom topics.
    """
    
    start_time = datetime.utcnow()
    user_email = request.user_email
    action_id = f"phish-{uuid4().hex[:8]}"
    
    # Use environment variable for base URL
    import os
    base_url = os.getenv("BASE_URL", "http://localhost:8080")
    track_url = f"{base_url}/track/click?user_email={user_email}&action={action_id}"
    
    generation_method = "fallback"
    email_content = ""
    model_used = None
    
    # Validate scenario type only if no custom topic is provided
    if not request.custom_topic and request.scenario_type not in PHISHING_SCENARIOS:
        available_scenarios = list(PHISHING_SCENARIOS.keys())
        raise HTTPException(
            status_code=400,
            detail=f"Invalid scenario_type. Available options: {available_scenarios}, or provide a custom_topic"
        )
    
    if request.use_llm:
        try:
            # Generate using Phi-3 Mini via Ollama with custom topic support
            prompt = create_phishing_prompt(user_email, request.scenario_type, request.custom_topic)
            llm_response = await ollama_client.generate_completion(
                prompt, 
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            # FIXED: Use the intelligent tracking URL insertion function
            email_content = insert_tracking_url(llm_response, track_url)
            generation_method = "phi3_mini_ollama"
            model_used = ollama_client.model
            
            logger.info(f"Successfully generated email using {model_used} for {user_email}")
            
        except HTTPException:
            # Re-raise HTTP exceptions (these are already properly formatted)
            raise
        except Exception as e:
            # If LLM fails for other reasons, use fallback
            logger.warning(f"LLM generation failed for {user_email}: {e}")
            email_content = generate_fallback_email(user_email, action_id, track_url, request.scenario_type)
            generation_method = "fallback_template"
    else:
        # Explicitly requested fallback
        email_content = generate_fallback_email(user_email, action_id, track_url, request.scenario_type)
        generation_method = "fallback_template"
    
    generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
    
    # Generate HTML versions if requested
    email_content_html = None
    email_content_html_with_pixel = None
    
    if request.html_format:
        try:
            email_content_html = convert_to_html_email(email_content)
            logger.info(f"Generated HTML version for {user_email}")
        except Exception as e:
            logger.error(f"Failed to generate HTML for {user_email}: {e}")
    
    # Generate tracking pixel if requested
    tracking_pixel_url = None
    email_content_with_pixel = None
    
    if request.include_tracking_pixel:
        try:
            tracking_pixel_url = generate_tracking_url(
                user_email, 
                action_id, 
                request.campaign_id
            )
            email_content_with_pixel = add_tracking_pixel_to_email(email_content, tracking_pixel_url)
            
            # Also add pixel to HTML version if available
            if email_content_html:
                email_content_html_with_pixel = add_tracking_pixel_to_email(email_content_html, tracking_pixel_url)
                
            logger.info(f"Added tracking pixel to email for {user_email}")
        except Exception as e:
            logger.warning(f"Failed to add tracking pixel: {e}")
            email_content_with_pixel = email_content
    
    return EmailResponse(
        email=user_email,
        action_id=action_id,
        track_url=track_url,
        tracking_pixel_url=tracking_pixel_url,
        email_content=email_content,
        email_content_with_pixel=email_content_with_pixel,
        email_content_html=email_content_html,
        email_content_html_with_pixel=email_content_html_with_pixel,
        generated_at=datetime.utcnow().isoformat(),
        generation_method=generation_method,
        scenario_type=request.custom_topic or request.scenario_type,
        model_used=model_used,
        generation_time_ms=generation_time
    )

# NEW: Debug endpoint to test tracking URL insertion
@router.post("/debug-tracking")
async def debug_tracking_insertion(
    user_email: str = Query(..., description="Target email address"),
    scenario_type: str = Query("system_update", description="Scenario type"),
    custom_topic: Optional[str] = Query(None, description="Custom topic")
):
    """
    Debug endpoint to test tracking URL insertion specifically
    """
    action_id = f"debug-{uuid4().hex[:8]}"
    track_url = f"http://localhost:8080/track/click?user_email={user_email}&action={action_id}"
    
    debug_info = {
        "input": {
            "user_email": user_email,
            "scenario_type": scenario_type,
            "custom_topic": custom_topic,
            "generated_tracking_url": track_url
        },
        "steps": []
    }
    
    try:
        # Generate with LLM
        prompt = create_phishing_prompt(user_email, scenario_type, custom_topic)
        llm_response = await ollama_client.generate_completion(prompt, max_tokens=300)
        
        debug_info["llm_raw_response"] = llm_response
        debug_info["steps"].append("Generated raw LLM response")
        
        # Test tracking URL insertion
        final_email = insert_tracking_url(llm_response, track_url)
        
        debug_info["final_email"] = final_email
        debug_info["tracking_url_inserted"] = track_url in final_email
        debug_info["insertion_successful"] = final_email != llm_response
        debug_info["steps"].append("Applied tracking URL insertion")
        
        # Show what changed
        if final_email != llm_response:
            debug_info["changes_made"] = "Tracking URL successfully inserted"
        else:
            debug_info["changes_made"] = "No changes - URL insertion may have failed"
            
    except Exception as e:
        debug_info["error"] = str(e)
        debug_info["fallback_test"] = generate_fallback_email(user_email, action_id, track_url, scenario_type)
        debug_info["fallback_has_url"] = track_url in debug_info["fallback_test"]
    
    return debug_info

# NEW: Flexible Email Generation Endpoint
@router.post("/generate-flexible-email")
async def generate_flexible_email(
    user_email: str = Query(..., description="Target email address"),
    topic: str = Query(..., description="Any topic for the phishing email"),
    temperature: float = Query(0.7, description="Creativity level"),
    max_tokens: int = Query(300, description="Maximum response length")
):
    """
    Generate phishing email for ANY topic - completely flexible
    
    Examples:
    - "COVID-19 vaccine appointment"
    - "Free pizza in the break room"
    - "New parking regulations"
    - "Employee satisfaction survey"
    - "Mandatory compliance training"
    - "Company merger announcement"
    """
    
    try:
        request = EmailGenRequest(
            user_email=user_email,
            custom_topic=topic,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return await generate_email(request)
            
    except Exception as e:
        logger.error(f"Flexible email generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.get("/health")
async def check_llm_health():
    """
    Comprehensive health check for LLM service
    """
    try:
        service_status = await ollama_client.check_service()
        
        # Test generation if service is available
        if service_status["service_available"]:
            try:
                test_prompt = "Generate a brief test response saying 'Service OK' and nothing else."
                test_response = await asyncio.wait_for(
                    ollama_client.generate_completion(test_prompt, max_tokens=10),
                    timeout=15.0
                )
                service_status["generation_test"] = {
                    "success": True,
                    "response_preview": test_response[:50] + "..." if len(test_response) > 50 else test_response
                }
            except Exception as e:
                service_status["generation_test"] = {
                    "success": False,
                    "error": str(e)
                }
        
        status_code = 200 if service_status["service_available"] else 503
        
        return JSONResponse(content={
            "status": "healthy" if service_status["service_available"] else "degraded",
            "ollama_service": service_status,
            "fallback_available": True,
            "supported_scenarios": list(PHISHING_SCENARIOS.keys()),
            "custom_topics_supported": True,
            "tracking_url_insertion": "enhanced_with_multiple_strategies",
            "checked_at": datetime.utcnow().isoformat()
        }, status_code=status_code)
        
    except Exception as e:
        return JSONResponse(content={
            "status": "unhealthy",
            "error": str(e),
            "fallback_available": True,
            "checked_at": datetime.utcnow().isoformat()
        }, status_code=500)

@router.get("/scenarios")
def get_available_scenarios():
    """
    Get list of available phishing scenarios
    """
    scenarios_info = {}
    for scenario_name, scenario_data in PHISHING_SCENARIOS.items():
        scenarios_info[scenario_name] = {
            "name": scenario_name.replace('_', ' ').title(),
            "description": scenario_data["context"],
            "urgency_factor": scenario_data["urgency"],
            "threat_element": scenario_data["threat"],
            "sample_subjects": scenario_data["subject_templates"][:2]  # Show first 2 templates
        }
    
    return JSONResponse(content={
        "available_scenarios": scenarios_info,
        "total_scenarios": len(PHISHING_SCENARIOS),
        "usage_tip": "Use the scenario_type parameter in /generate-email to specify which scenario to use, or use custom_topic for unlimited flexibility"
    })

@router.post("/test-generation")
async def test_generation(
    scenario_type: str = Query("account_security", description="Scenario to test"),
    custom_topic: Optional[str] = Query(None, description="Custom topic to test"),
    use_llm: bool = Query(True, description="Test LLM or fallback")
):
    """
    Test email generation without creating tracking links
    
    Useful for testing different scenarios and LLM connectivity.
    """
    if not custom_topic and scenario_type not in PHISHING_SCENARIOS:
        available_scenarios = list(PHISHING_SCENARIOS.keys())
        raise HTTPException(
            status_code=400,
            detail=f"Invalid scenario_type. Available options: {available_scenarios}, or provide custom_topic"
        )
    
    test_email = "test.user@example.com"
    test_action = "test-action-123"
    test_link = "https://example.com/training"
    
    start_time = datetime.utcnow()
    
    if use_llm:
        try:
            prompt = create_phishing_prompt(test_email, scenario_type, custom_topic)
            response = await ollama_client.generate_completion(prompt, max_tokens=300)
            email_content = insert_tracking_url(response, test_link)
            method = "phi3_mini_ollama"
        except Exception as e:
            email_content = generate_fallback_email(test_email, test_action, test_link, scenario_type)
            method = f"fallback_due_to_error: {str(e)}"
    else:
        email_content = generate_fallback_email(test_email, test_action, test_link, scenario_type)
        method = "fallback_template"
    
    generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
    
    return {
        "test_result": "success",
        "scenario_type": custom_topic or scenario_type,
        "generation_method": method,
        "generation_time_ms": generation_time,
        "email_content": email_content,
        "tracking_url_present": test_link in email_content,
        "note": "This is a test generation - no tracking links were created"
    }

class BatchEmailRequest(BaseModel):
    user_emails: List[str] = Field(..., description="List of user emails")
    scenario_type: Optional[str] = Field("account_security", description="Scenario type for all emails")
    custom_topic: Optional[str] = Field(None, description="Custom topic for all emails")
    use_llm: bool = Field(True, description="Whether to use LLM")
    max_concurrent: int = Field(5, ge=1, le=10, description="Maximum concurrent generations")

@router.post("/batch-generate")
async def batch_generate_emails(request: BatchEmailRequest):
    """
    Generate multiple phishing emails at once
    
    Useful for creating campaigns targeting multiple users with the same scenario or custom topic.
    """
    if len(request.user_emails) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 emails per batch")
    
    if not request.custom_topic and request.scenario_type not in PHISHING_SCENARIOS:
        available_scenarios = list(PHISHING_SCENARIOS.keys())
        raise HTTPException(
            status_code=400,
            detail=f"Invalid scenario_type. Available options: {available_scenarios}, or provide custom_topic"
        )
    
    results = []
    semaphore = asyncio.Semaphore(request.max_concurrent)
    
    async def generate_single_email(email: str):
        async with semaphore:
            try:
                email_request = EmailGenRequest(
                    user_email=email,
                    scenario_type=request.scenario_type,
                    custom_topic=request.custom_topic,
                    use_llm=request.use_llm
                )
                response = await generate_email(email_request)
                return {
                    "email": email,
                    "success": True,
                    "result": response.dict()
                }
            except Exception as e:
                return {
                    "email": email,
                    "success": False,
                    "error": str(e)
                }
    
    # Execute batch generation
    tasks = [generate_single_email(email) for email in request.user_emails]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    successful = [r for r in results if isinstance(r, dict) and r.get("success")]
    failed = [r for r in results if isinstance(r, dict) and not r.get("success")]
    
    return {
        "batch_summary": {
            "total_requested": len(request.user_emails),
            "successful": len(successful),
            "failed": len(failed),
            "topic": request.custom_topic or request.scenario_type,
            "used_llm": request.use_llm
        },
        "results": results,
        "generated_at": datetime.utcnow().isoformat()
    }

class CustomScenarioRequest(BaseModel):
    scenario_name: str = Field(..., description="Unique name for the scenario")
    context: str = Field(..., description="Scenario context description")
    urgency: str = Field(..., description="Urgency factor for the scenario")
    threat: str = Field(..., description="Threat element of the scenario")
    subject_templates: List[str] = Field(..., description="List of subject line templates")

@router.post("/customize-scenario")
async def create_custom_scenario(request: CustomScenarioRequest):
    """
    Create a custom phishing scenario
    
    Note: In production, this would save to a database. Currently stores in memory only.
    """
    if len(request.subject_templates) < 1:
        raise HTTPException(status_code=400, detail="At least one subject template is required")
    
    if request.scenario_name in PHISHING_SCENARIOS:
        raise HTTPException(status_code=400, detail=f"Scenario '{request.scenario_name}' already exists")
    
    # Add to scenarios (temporary - would be saved to DB in production)
    PHISHING_SCENARIOS[request.scenario_name] = {
        "context": request.context,
        "urgency": request.urgency,
        "threat": request.threat,
        "subject_templates": request.subject_templates,
        "custom": True,
        "created_at": datetime.utcnow().isoformat()
    }
    
    return {
        "message": f"Custom scenario '{request.scenario_name}' created successfully",
        "scenario": PHISHING_SCENARIOS[request.scenario_name],
        "total_scenarios": len(PHISHING_SCENARIOS),
        "note": "Custom scenarios are stored in memory and will be lost on server restart"
    }

@router.get("/generation-stats")
def get_generation_stats():
    """
    Get statistics about email generation
    
    In production, this would query actual usage data from a database.
    """
    # This is a placeholder - in production you'd track actual usage
    return {
        "available_scenarios": len(PHISHING_SCENARIOS),
        "scenario_types": list(PHISHING_SCENARIOS.keys()),
        "fallback_templates_available": True,
        "custom_topics_supported": True,
        "tracking_url_insertion": "enhanced_with_intelligent_fallbacks",
        "llm_integration": {
            "model": ollama_client.model,
            "base_url": ollama_client.base_url,
            "timeout": ollama_client.timeout
        },
        "features": {
            "batch_generation": True,
            "custom_scenarios": True,
            "health_monitoring": True,
            "fallback_mode": True,
            "general_chat": True,
            "unlimited_topics": True,
            "flexible_generation": True,
            "intelligent_url_insertion": True,
            "debug_endpoints": True
        }
    }