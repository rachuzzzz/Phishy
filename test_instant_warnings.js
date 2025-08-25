/**
 * Test Script for Instant Gmail Warnings
 * Copy this into Gmail console (F12) to test instant warnings
 */

console.log('🧪 Testing Phishy AI Instant Warnings...');

// Test function to trigger warnings on any visible email
function testInstantWarnings() {
    console.log('⚡ Starting instant warning test...');
    
    // Find any email content
    const emailContent = document.querySelector('.ii.gt, .a3s.aiL, .adn.ads, .gs .a3s');
    
    if (!emailContent) {
        console.error('❌ No email content found. Please open an email first.');
        return;
    }
    
    console.log('📧 Found email content, testing warnings...');
    
    // Create test phishing email data
    const testPhishingData = {
        sender: 'urgent.security@fake-bank.com',
        subject: 'URGENT: Verify Your Account Immediately',
        body: `
            Dear Customer,
            
            Your account has been suspended due to suspicious activity.
            Click here to verify your account: http://fake-bank-verification.com/urgent
            
            Please provide your login credentials and social security number.
            
            Act now or your account will be permanently closed!
            
            This is a phishing simulation training email from Phishy AI.
        `,
        urls: ['http://fake-bank-verification.com/urgent'],
        hasAttachments: false
    };
    
    // Create a fake analysis result that should trigger HIGH warning
    const testAnalysisResult = {
        is_phishing: true,
        confidence_score: 95,
        risk_level: 'CRITICAL',
        analysis_details: {
            risk_factors: [
                'High-risk keywords detected: urgent, verify, suspended, click here, phishing, simulation, training',
                '1 URLs detected',
                'Suspicious tracking/shortened URLs',
                'Personal info requested: login, credentials',
                'Suspicious subject line indicators: 2'
            ],
            analysis_method: 'instant_rules_test',
            total_risk_score: 150
        },
        recommendations: [
            '🚨 DO NOT CLICK any links in this email!',
            '📞 Verify sender through alternative means',
            '🛡️ Report to IT security team immediately'
        ]
    };
    
    // Trigger the warning directly
    if (window.phishyGmail && window.phishyGmail.showSuspiciousEmailWarning) {
        console.log('🚨 Triggering HIGH RISK warning...');
        window.phishyGmail.showSuspiciousEmailWarning(emailContent, testAnalysisResult);
        console.log('✅ Warning displayed!');
    } else {
        console.error('❌ Phishy Gmail extension not found or not loaded');
    }
}

// Test medium risk warning
function testMediumWarning() {
    const emailContent = document.querySelector('.ii.gt, .a3s.aiL, .adn.ads, .gs .a3s');
    
    if (!emailContent) {
        console.error('❌ No email content found');
        return;
    }
    
    const mediumAnalysisResult = {
        is_phishing: false,
        confidence_score: 65,
        risk_level: 'MEDIUM',
        analysis_details: {
            risk_factors: ['Suspicious keywords detected', 'Multiple URLs found'],
            analysis_method: 'instant_rules_test',
            total_risk_score: 40
        },
        recommendations: ['Exercise caution with this email']
    };
    
    if (window.phishyGmail && window.phishyGmail.showCautionWarning) {
        console.log('⚠️ Triggering MEDIUM risk warning...');
        window.phishyGmail.showCautionWarning(emailContent, mediumAnalysisResult);
        console.log('✅ Medium warning displayed!');
    }
}

// Test the instant scanning function
function testInstantScan() {
    console.log('⚡ Testing instant scan function...');
    
    const emailContent = document.querySelector('.ii.gt, .a3s.aiL, .adn.ads, .gs .a3s');
    
    if (!emailContent) {
        console.error('❌ No email content found');
        return;
    }
    
    // Remove existing scan marker to force re-scan
    emailContent.removeAttribute('data-phishy-scanned');
    
    if (window.phishyGmail && window.phishyGmail.scanOpenedEmailImmediate) {
        console.log('🔍 Triggering instant scan...');
        window.phishyGmail.scanOpenedEmailImmediate(emailContent);
        console.log('✅ Instant scan completed!');
    } else {
        console.error('❌ Instant scan function not found');
    }
}

// Force scan all visible emails
function forceInstantScanAll() {
    console.log('⚡ Force scanning ALL visible emails...');
    
    if (window.phishyGmail && window.phishyGmail.scanVisibleEmailsImmediate) {
        // Remove all scan markers first
        document.querySelectorAll('[data-phishy-scanned]').forEach(el => {
            el.removeAttribute('data-phishy-scanned');
        });
        
        window.phishyGmail.scanVisibleEmailsImmediate();
        console.log('✅ All emails scanned!');
    } else {
        console.error('❌ Phishy extension not loaded');
    }
}

// Create test buttons for easy testing
function createTestButtons() {
    // Remove existing test buttons
    const existing = document.querySelector('#phishy-test-buttons');
    if (existing) existing.remove();
    
    const buttonContainer = document.createElement('div');
    buttonContainer.id = 'phishy-test-buttons';
    buttonContainer.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 100000;
        background: rgba(0,0,0,0.9);
        padding: 15px;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    `;
    
    const buttons = [
        { text: '🚨 Test HIGH Risk Warning', func: testInstantWarnings, color: '#dc3545' },
        { text: '⚠️ Test MEDIUM Risk Warning', func: testMediumWarning, color: '#fd7e14' },
        { text: '⚡ Test Instant Scan', func: testInstantScan, color: '#17a2b8' },
        { text: '🔍 Force Scan All', func: forceInstantScanAll, color: '#28a745' },
        { text: '❌ Remove Tests', func: () => buttonContainer.remove(), color: '#6c757d' }
    ];
    
    buttons.forEach(({ text, func, color }) => {
        const btn = document.createElement('button');
        btn.textContent = text;
        btn.style.cssText = `
            background: ${color};
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: bold;
        `;
        btn.onclick = func;
        buttonContainer.appendChild(btn);
    });
    
    document.body.appendChild(buttonContainer);
    console.log('✅ Test buttons added to top-right corner');
}

// Run tests
console.log('🧪 Available test functions:');
console.log('• testInstantWarnings() - Show HIGH risk warning');
console.log('• testMediumWarning() - Show MEDIUM risk warning');
console.log('• testInstantScan() - Test instant scanning');
console.log('• forceInstantScanAll() - Scan all emails immediately');
console.log('• createTestButtons() - Add test buttons to page');

// Auto-create test buttons
createTestButtons();

// Auto-test if we find phishing keywords
const pageText = document.body.innerText.toLowerCase();
if (pageText.includes('urgent') || pageText.includes('verify') || pageText.includes('phishy')) {
    console.log('🎯 Phishing keywords detected on page - running test scan...');
    setTimeout(forceInstantScanAll, 1000);
}

console.log('⚡ Instant warning test setup complete!');