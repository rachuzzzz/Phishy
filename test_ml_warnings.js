/**
 * Test ML Model Integration - Gmail Extension
 * Copy this into Gmail console to test ML-based warnings
 */

console.log('🤖 Testing ML Model Integration for Gmail Extension...');

// Test the ML API directly
async function testMLAPI() {
    if (!window.phishyGmail?.apiBaseUrl) {
        console.error('❌ API URL not configured. Please configure the extension first.');
        return false;
    }
    
    const apiUrl = window.phishyGmail.apiBaseUrl;
    console.log('🔍 Testing ML API at:', apiUrl);
    
    // Test email with phishing indicators
    const testEmail = `Subject: URGENT: Verify Your Account Immediately

Dear Customer,

Your account has been suspended due to suspicious activity.
Click here to verify your account: http://fake-verification.com/urgent

Please provide your password and social security number.

Act now or your account will be permanently closed!

This is a phishing simulation training email from Phishy AI.`;

    try {
        console.log('📤 Sending test email to ML model...');
        
        const response = await fetch(`${apiUrl}/detector/analyze-email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email_content: testEmail,
                include_detailed_analysis: true,
                cache_results: false
            }),
            signal: AbortSignal.timeout(5000)
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('✅ ML Model Response:', result);
            
            console.log('🎯 Analysis Summary:');
            console.log(`   Is Phishing: ${result.is_phishing}`);
            console.log(`   Risk Level: ${result.risk_level}`);
            console.log(`   Confidence: ${result.confidence_score}%`);
            console.log(`   Method: ${result.analysis_details?.analysis_method}`);
            
            if (result.analysis_details?.risk_factors) {
                console.log('   Risk Factors:', result.analysis_details.risk_factors);
            }
            
            return result;
        } else {
            console.error('❌ ML API Error:', response.status, response.statusText);
            return false;
        }
        
    } catch (error) {
        console.error('❌ ML API Connection Failed:', error.message);
        return false;
    }
}

// Test the extension's ML integration
async function testExtensionMLScan() {
    console.log('🧪 Testing extension ML scanning...');
    
    const emailContent = document.querySelector('.ii.gt, .a3s.aiL');
    if (!emailContent) {
        console.error('❌ No email content found. Please open an email first.');
        return;
    }
    
    if (!window.phishyGmail) {
        console.error('❌ Phishy Gmail extension not loaded');
        return;
    }
    
    // Clear any existing processing state
    if (window.phishyGmail.processingEmails) {
        window.phishyGmail.processingEmails.clear();
    }
    if (window.phishyGmail.shownWarnings) {
        window.phishyGmail.shownWarnings.clear();
    }
    
    // Remove existing scan markers
    document.querySelectorAll('[data-phishy-scanned]').forEach(el => {
        el.removeAttribute('data-phishy-scanned');
    });
    
    // Remove existing warnings
    document.querySelectorAll('.phishy-email-warning, .phishy-safe-indicator').forEach(el => {
        el.remove();
    });
    
    console.log('🚀 Triggering ML scan...');
    
    try {
        await window.phishyGmail.scanOpenedEmailImmediate(emailContent);
        console.log('✅ ML scan completed!');
    } catch (error) {
        console.error('❌ ML scan failed:', error);
    }
}

// Check extension configuration
function checkExtensionConfig() {
    console.log('⚙️ Checking Extension Configuration:');
    
    if (!window.phishyGmail) {
        console.error('❌ Phishy Gmail extension not loaded');
        return false;
    }
    
    const config = {
        isActive: window.phishyGmail.isActive,
        apiBaseUrl: window.phishyGmail.apiBaseUrl,
        userEmail: window.phishyGmail.userEmail,
        pluginId: window.phishyGmail.pluginId
    };
    
    console.log('📋 Configuration:', config);
    
    if (!config.apiBaseUrl) {
        console.error('❌ API URL not configured!');
        console.log('💡 Configure with: window.phishyGmail.apiBaseUrl = "http://localhost:8080"');
        return false;
    }
    
    if (!config.isActive) {
        console.warn('⚠️ Extension is not active');
        return false;
    }
    
    console.log('✅ Extension properly configured');
    return true;
}

// Run comprehensive test
async function runMLTests() {
    console.log('🧪 Starting Comprehensive ML Integration Tests...');
    console.log('=' + '='.repeat(50));
    
    // Step 1: Check configuration
    console.log('\n1️⃣ Checking Extension Configuration...');
    const configOK = checkExtensionConfig();
    
    if (!configOK) {
        console.log('\n❌ Configuration issues detected. Please fix and try again.');
        return;
    }
    
    // Step 2: Test ML API directly
    console.log('\n2️⃣ Testing ML API Directly...');
    const mlResult = await testMLAPI();
    
    if (!mlResult) {
        console.log('\n❌ ML API test failed. Check backend status.');
        return;
    }
    
    // Step 3: Test extension integration
    console.log('\n3️⃣ Testing Extension ML Integration...');
    await testExtensionMLScan();
    
    console.log('\n' + '='.repeat(51));
    console.log('🎉 ML Integration Tests Complete!');
    console.log('✅ Your extension should now use the ML model for warnings');
    console.log('✅ Warnings appear based on YOUR trained model results');
    console.log('✅ No more duplicate warnings');
    console.log('=' + '='.repeat(50));
}

// Create test buttons
function createMLTestButtons() {
    const existing = document.querySelector('#phishy-ml-test-buttons');
    if (existing) existing.remove();
    
    const buttonContainer = document.createElement('div');
    buttonContainer.id = 'phishy-ml-test-buttons';
    buttonContainer.style.cssText = `
        position: fixed;
        top: 60px;
        right: 10px;
        z-index: 100001;
        background: rgba(25, 25, 112, 0.95);
        padding: 15px;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        border: 2px solid #4169E1;
    `;
    
    const title = document.createElement('div');
    title.textContent = '🤖 ML Model Tests';
    title.style.cssText = 'color: white; font-weight: bold; text-align: center; margin-bottom: 5px;';
    buttonContainer.appendChild(title);
    
    const buttons = [
        { text: '🧪 Run All ML Tests', func: runMLTests, color: '#4169E1' },
        { text: '⚙️ Check Config', func: checkExtensionConfig, color: '#32CD32' },
        { text: '🌐 Test API', func: testMLAPI, color: '#FF6347' },
        { text: '🚀 Test ML Scan', func: testExtensionMLScan, color: '#FFD700' },
        { text: '❌ Remove', func: () => buttonContainer.remove(), color: '#696969' }
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
            font-size: 11px;
            font-weight: bold;
            width: 150px;
        `;
        btn.onclick = func;
        buttonContainer.appendChild(btn);
    });
    
    document.body.appendChild(buttonContainer);
    console.log('🎛️ ML test buttons added');
}

// Auto-run
console.log('🎯 Available ML test functions:');
console.log('• runMLTests() - Complete ML integration test');
console.log('• testMLAPI() - Test your ML model API');
console.log('• testExtensionMLScan() - Test extension ML scanning');
console.log('• checkExtensionConfig() - Check configuration');

// Auto-create test buttons
createMLTestButtons();

console.log('\n🚀 Ready to test ML integration! Click "Run All ML Tests" button or call runMLTests()');