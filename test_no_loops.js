/**
 * Test No More Scanning Loops
 * Copy this into Gmail console to verify loops are fixed
 */

console.log('🔄 Testing for Scanning Loops...');

// Monitor API calls to detect loops
let apiCallCount = 0;
let lastApiCall = 0;
const apiCalls = [];

// Intercept fetch to monitor ML API calls
const originalFetch = window.fetch;
window.fetch = function(...args) {
    const url = args[0];
    
    // Check if it's a call to the ML detector
    if (typeof url === 'string' && url.includes('/detector/analyze-email')) {
        const now = Date.now();
        apiCallCount++;
        
        console.log(`🔍 API Call #${apiCallCount} to ML model`);
        console.log(`   ⏰ Time since last: ${now - lastApiCall}ms`);
        
        apiCalls.push({
            callNumber: apiCallCount,
            timestamp: now,
            timeSinceLast: now - lastApiCall
        });
        
        lastApiCall = now;
        
        // Warn if too frequent
        if (apiCallCount > 1 && now - lastApiCall < 1000) {
            console.warn('⚠️ POTENTIAL LOOP DETECTED - API calls too frequent!');
        }
    }
    
    return originalFetch.apply(this, args);
};

// Check extension state
function checkExtensionState() {
    console.log('🔍 Extension State Check:');
    
    if (!window.phishyGmail) {
        console.error('❌ Extension not loaded');
        return;
    }
    
    const state = {
        isActive: window.phishyGmail.isActive,
        apiBaseUrl: window.phishyGmail.apiBaseUrl,
        processingEmails: window.phishyGmail.processingEmails?.size || 0,
        shownWarnings: window.phishyGmail.shownWarnings?.size || 0
    };
    
    console.log('📊 Current State:', state);
    
    // Check for scanned emails
    const scannedEmails = document.querySelectorAll('[data-phishy-scanned]');
    console.log(`📧 Emails already scanned: ${scannedEmails.length}`);
    
    return state;
}

// Monitor console for repeated messages
let logCounts = {};
const originalLog = console.log;
console.log = function(...args) {
    const message = args.join(' ');
    
    // Count repeated ML scanning messages
    if (message.includes('ML SCAN starting') || 
        message.includes('INSTANT scan triggered') ||
        message.includes('ML MODEL RESPONSE')) {
        
        logCounts[message] = (logCounts[message] || 0) + 1;
        
        if (logCounts[message] > 3) {
            console.warn(`🔄 LOOP DETECTED: "${message}" repeated ${logCounts[message]} times!`);
        }
    }
    
    return originalLog.apply(this, args);
};

// Test function
function testForLoops() {
    console.log('🧪 Starting Loop Detection Test...');
    console.log('=' + '='.repeat(40));
    
    // Reset counters
    apiCallCount = 0;
    lastApiCall = 0;
    apiCalls.length = 0;
    logCounts = {};
    
    console.log('1️⃣ Checking initial extension state...');
    checkExtensionState();
    
    console.log('\n2️⃣ Monitoring for 30 seconds...');
    console.log('   👀 Watching for repeated API calls');
    console.log('   👂 Listening for repeated log messages');
    
    // Monitor for 30 seconds
    setTimeout(() => {
        console.log('\n' + '='.repeat(41));
        console.log('📊 LOOP TEST RESULTS:');
        console.log('=' + '='.repeat(40));
        
        console.log(`🔍 Total ML API calls: ${apiCallCount}`);
        
        if (apiCallCount === 0) {
            console.log('✅ GOOD: No API calls detected (no loops)');
        } else if (apiCallCount === 1) {
            console.log('✅ PERFECT: Only 1 API call (expected behavior)');
        } else if (apiCallCount <= 3) {
            console.log('⚠️ ACCEPTABLE: Few API calls (might be legitimate)');
        } else {
            console.warn(`🚨 LOOP DETECTED: ${apiCallCount} API calls in 30 seconds!`);
        }
        
        // Show repeated messages
        const repeatedMessages = Object.entries(logCounts).filter(([msg, count]) => count > 2);
        if (repeatedMessages.length > 0) {
            console.log('\n🔄 Repeated Log Messages:');
            repeatedMessages.forEach(([msg, count]) => {
                console.log(`   ${count}x: ${msg.substring(0, 60)}...`);
            });
        }
        
        // Show API call timeline
        if (apiCalls.length > 1) {
            console.log('\n⏰ API Call Timeline:');
            apiCalls.forEach(call => {
                console.log(`   Call ${call.callNumber}: +${call.timeSinceLast}ms`);
            });
        }
        
        console.log('=' + '='.repeat(41));
        
        // Restore original fetch
        window.fetch = originalFetch;
        console.log = originalLog;
        
    }, 30000);
}

// Quick test - trigger scan manually
function triggerTestScan() {
    console.log('🚀 Manually triggering scan to test...');
    
    if (window.phishyGmail) {
        // Clear previous state
        localStorage.removeItem('phishy_last_scan');
        
        // Trigger scan
        window.phishyGmail.scanVisibleEmailsImmediate();
        
        // Check results after 5 seconds
        setTimeout(() => {
            console.log(`📊 After manual scan: ${apiCallCount} API calls made`);
        }, 5000);
    }
}

// Available functions
console.log('🎯 Available loop test functions:');
console.log('• testForLoops() - Monitor for 30 seconds');
console.log('• triggerTestScan() - Manual scan test');
console.log('• checkExtensionState() - Check current state');

console.log('\n✅ Loop detection monitoring active!');
console.log('🔍 All ML API calls will be logged and counted');
console.log('⚠️ Run testForLoops() for comprehensive test');