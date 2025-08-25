/**
 * Test Dismiss Button Functionality
 * Copy this into Gmail console to test the dismiss button
 */

console.log('🧪 Testing Dismiss Button Functionality...');

// Test dismiss functionality
function testDismissButton() {
    console.log('🔍 Testing dismiss button...');
    
    if (!window.phishyGmail) {
        console.error('❌ Phishy Gmail extension not loaded');
        return;
    }
    
    // Find any email content to create a test warning
    const emailContent = document.querySelector('.ii.gt, .a3s.aiL, .adn.ads, .gs .a3s');
    
    if (!emailContent) {
        console.error('❌ No email content found. Please open an email first.');
        return;
    }
    
    // Create a test warning with dismiss button
    const testWarningId = 'phishy-test-warning-' + Date.now();
    const testWarning = document.createElement('div');
    testWarning.id = testWarningId;
    testWarning.className = 'phishy-email-warning phishy-warning-high';
    testWarning.style.cssText = `
        position: relative;
        z-index: 99999;
        margin: 10px 0;
    `;
    
    testWarning.innerHTML = `
        <div style="background: linear-gradient(135deg, #dc3545, #a71e2a); 
                    color: white; padding: 20px; border-radius: 8px; 
                    border: 3px solid #721c24; box-shadow: 0 8px 25px rgba(220, 53, 69, 0.5);">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <span style="font-size: 32px; margin-right: 15px;">🧪</span>
                <div>
                    <h4 style="margin: 0; font-size: 20px; font-weight: bold;">
                        TEST WARNING - DISMISS BUTTON TEST
                    </h4>
                    <p style="margin: 8px 0 0 0; font-size: 14px;">
                        This is a test warning to verify the dismiss functionality works
                    </p>
                </div>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button class="phishy-btn phishy-btn-dismiss" 
                        style="background: #6c757d !important; color: white !important; font-weight: bold !important; 
                               padding: 12px 20px !important; border-radius: 6px !important; cursor: pointer;"
                        onclick="window.phishyGmail.dismissWarning('${testWarningId}')">
                    ✅ I UNDERSTAND - DISMISS
                </button>
                <button class="phishy-btn" 
                        style="background: #28a745 !important; color: white !important; font-weight: bold !important; 
                               padding: 12px 20px !important; border-radius: 6px !important; cursor: pointer;"
                        onclick="console.log('🧪 Test button clicked!')">
                    🧪 TEST BUTTON
                </button>
            </div>
        </div>
    `;
    
    // Insert the test warning
    emailContent.parentNode.insertBefore(testWarning, emailContent);
    
    console.log('✅ Test warning created with ID:', testWarningId);
    console.log('🎯 Click the "I UNDERSTAND - DISMISS" button to test functionality');
    
    // Auto-test dismiss after 10 seconds if not manually dismissed
    setTimeout(() => {
        if (document.getElementById(testWarningId)) {
            console.log('⏰ Auto-testing dismiss function...');
            window.phishyGmail.dismissWarning(testWarningId);
        }
    }, 10000);
    
    return testWarningId;
}

// Test the dismiss function directly
function testDismissFunction(warningId) {
    console.log('🔧 Testing dismiss function directly...');
    
    if (!window.phishyGmail || !window.phishyGmail.dismissWarning) {
        console.error('❌ Dismiss function not found');
        return false;
    }
    
    if (!warningId) {
        // Find any existing warning
        const existingWarning = document.querySelector('.phishy-email-warning');
        if (existingWarning && existingWarning.id) {
            warningId = existingWarning.id;
        } else {
            console.error('❌ No warning ID provided and no existing warnings found');
            return false;
        }
    }
    
    console.log('🎯 Dismissing warning:', warningId);
    window.phishyGmail.dismissWarning(warningId);
    
    // Check if it was removed
    setTimeout(() => {
        const stillExists = document.getElementById(warningId);
        if (!stillExists) {
            console.log('✅ Dismiss function works correctly!');
            return true;
        } else {
            console.error('❌ Warning still exists after dismiss');
            return false;
        }
    }, 500);
}

// Clean up any existing test warnings
function cleanupTestWarnings() {
    console.log('🧹 Cleaning up test warnings...');
    const testWarnings = document.querySelectorAll('[id*="phishy-test-warning"]');
    testWarnings.forEach(warning => warning.remove());
    console.log(`✅ Removed ${testWarnings.length} test warnings`);
}

// Run comprehensive dismiss test
function runDismissTests() {
    console.log('🧪 Running Comprehensive Dismiss Button Tests...');
    console.log('=' + '='.repeat(45));
    
    // Clean up first
    cleanupTestWarnings();
    
    // Test 1: Check if dismiss function exists
    console.log('\n1️⃣ Checking dismiss function exists...');
    if (window.phishyGmail && window.phishyGmail.dismissWarning) {
        console.log('✅ Dismiss function found');
    } else {
        console.error('❌ Dismiss function not found');
        return;
    }
    
    // Test 2: Create test warning
    console.log('\n2️⃣ Creating test warning...');
    const warningId = testDismissButton();
    
    console.log('\n3️⃣ Instructions:');
    console.log('👆 Click the "I UNDERSTAND - DISMISS" button in the warning above');
    console.log('⏱️  Or wait 10 seconds for auto-test');
    
    console.log('\n🎯 You can also manually test with:');
    console.log(`   testDismissFunction('${warningId}')`);
    
    console.log('\n' + '='.repeat(46));
}

// Create test buttons
function createDismissTestButtons() {
    const existing = document.querySelector('#phishy-dismiss-test-buttons');
    if (existing) existing.remove();
    
    const buttonContainer = document.createElement('div');
    buttonContainer.id = 'phishy-dismiss-test-buttons';
    buttonContainer.style.cssText = `
        position: fixed;
        top: 120px;
        right: 10px;
        z-index: 100002;
        background: rgba(106, 90, 205, 0.95);
        padding: 15px;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        border: 2px solid #9370DB;
    `;
    
    const title = document.createElement('div');
    title.textContent = '✅ Dismiss Button Tests';
    title.style.cssText = 'color: white; font-weight: bold; text-align: center; margin-bottom: 5px; font-size: 12px;';
    buttonContainer.appendChild(title);
    
    const buttons = [
        { text: '🧪 Test Dismiss', func: runDismissTests, color: '#9370DB' },
        { text: '🔧 Create Test Warning', func: testDismissButton, color: '#FF69B4' },
        { text: '🧹 Clean Up Tests', func: cleanupTestWarnings, color: '#32CD32' },
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
            width: 140px;
        `;
        btn.onclick = func;
        buttonContainer.appendChild(btn);
    });
    
    document.body.appendChild(buttonContainer);
    console.log('🎛️ Dismiss test buttons added');
}

// Available functions
console.log('🎯 Available dismiss test functions:');
console.log('• runDismissTests() - Complete dismiss button test');
console.log('• testDismissButton() - Create test warning');
console.log('• testDismissFunction(warningId) - Test dismiss directly');
console.log('• cleanupTestWarnings() - Remove test warnings');

// Auto-create test buttons
createDismissTestButtons();

console.log('\n✅ Dismiss button test ready! Click "Test Dismiss" button to start');
console.log('🎯 The dismiss button should now work properly with fade animation');