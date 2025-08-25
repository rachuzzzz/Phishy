/**
 * Gmail Extension Debug Script
 * Copy and paste this into Gmail console (F12) to debug Phishy AI extension
 */

console.log('🔧 Starting Phishy AI Gmail Extension Debug...');

// Debug helper functions
const debug = {
    log: (msg, data = '') => console.log(`🐛 DEBUG: ${msg}`, data),
    error: (msg, error) => console.error(`❌ ERROR: ${msg}`, error),
    success: (msg) => console.log(`✅ SUCCESS: ${msg}`),
    
    // Check if extension is loaded
    checkExtension: () => {
        const isLoaded = window.phishyGmail !== undefined;
        debug.log('Extension loaded:', isLoaded);
        if (isLoaded) {
            debug.log('Extension config:', {
                apiBaseUrl: window.phishyGmail.apiBaseUrl,
                userEmail: window.phishyGmail.userEmail,
                isActive: window.phishyGmail.isActive,
                pluginId: window.phishyGmail.pluginId
            });
        }
        return isLoaded;
    },
    
    // Check for flag buttons
    checkFlagButtons: () => {
        const buttons = document.querySelectorAll('.phishy-flag-btn');
        debug.log('Flag buttons found:', buttons.length);
        buttons.forEach((btn, i) => {
            debug.log(`Button ${i + 1}:`, {
                text: btn.textContent,
                visible: btn.offsetParent !== null,
                parent: btn.parentElement?.className
            });
        });
        return buttons;
    },
    
    // Check email content elements
    checkEmailContent: () => {
        const selectors = [
            '.ii.gt',           // Gmail message body
            '.a3s.aiL',         // Gmail email content  
            '.adn.ads',         // Gmail conversation
            '.gs .a3s',         // Gmail thread content
            '[role="listitem"] .a3s', // Gmail inbox messages
            '.Ar.Au .adn'       // Gmail expanded messages
        ];
        
        debug.log('Checking email content selectors...');
        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            debug.log(`${selector}: ${elements.length} elements found`);
            
            elements.forEach((el, i) => {
                if (i < 3) { // Show first 3 elements
                    debug.log(`  Element ${i + 1}:`, {
                        textLength: el.textContent?.length || 0,
                        scanned: el.hasAttribute('data-phishy-scanned'),
                        visible: el.offsetParent !== null
                    });
                }
            });
        });
    },
    
    // Test email scanning manually
    testScan: async () => {
        if (!window.phishyGmail) {
            debug.error('Phishy extension not found');
            return;
        }
        
        const emailContents = document.querySelectorAll('.ii.gt, .a3s.aiL');
        if (emailContents.length === 0) {
            debug.error('No email content found');
            return;
        }
        
        const firstEmail = emailContents[0];
        debug.log('Testing scan on first email found');
        
        try {
            await window.phishyGmail.scanOpenedEmail(firstEmail);
            debug.success('Scan completed');
        } catch (error) {
            debug.error('Scan failed:', error);
        }
    },
    
    // Force trigger scanning
    forceScan: () => {
        if (!window.phishyGmail) {
            debug.error('Phishy extension not found');
            return;
        }
        
        debug.log('Forcing email scan...');
        
        // Remove scan markers to force re-scan
        const scannedElements = document.querySelectorAll('[data-phishy-scanned]');
        scannedElements.forEach(el => el.removeAttribute('data-phishy-scanned'));
        debug.log('Removed scan markers from', scannedElements.length, 'elements');
        
        // Trigger scan
        window.phishyGmail.scanVisibleEmails();
        debug.success('Scan triggered');
    },
    
    // Test flag button functionality
    testFlagButton: () => {
        const buttons = document.querySelectorAll('.phishy-flag-btn');
        if (buttons.length === 0) {
            debug.error('No flag buttons found');
            return;
        }
        
        debug.log('Testing flag button click...');
        buttons[0].click();
        debug.success('Flag button clicked');
    },
    
    // Test configuration
    testConfig: async () => {
        if (!window.phishyGmail?.apiBaseUrl) {
            debug.error('API URL not configured');
            return false;
        }
        
        const apiUrl = window.phishyGmail.apiBaseUrl;
        debug.log('Testing API connection to:', apiUrl);
        
        try {
            const response = await fetch(`${apiUrl}/detector/health`, { timeout: 5000 });
            if (response.ok) {
                const data = await response.json();
                debug.success('API connection successful:', data);
                return true;
            } else {
                debug.error('API returned error:', response.status);
                return false;
            }
        } catch (error) {
            debug.error('API connection failed:', error.message);
            return false;
        }
    },
    
    // Comprehensive diagnosis
    diagnose: async () => {
        console.log('\\n' + '='.repeat(60));
        console.log('🛡️  PHISHY AI GMAIL EXTENSION DIAGNOSIS');
        console.log('='.repeat(60));
        
        // 1. Check extension loading
        console.log('\\n📦 1. Extension Loading');
        const extensionLoaded = debug.checkExtension();
        
        // 2. Check configuration
        console.log('\\n⚙️ 2. Configuration');
        if (extensionLoaded) {
            const apiConnected = await debug.testConfig();
        }
        
        // 3. Check email detection
        console.log('\\n📧 3. Email Content Detection');
        debug.checkEmailContent();
        
        // 4. Check flag buttons
        console.log('\\n🚩 4. Flag Buttons');
        debug.checkFlagButtons();
        
        // 5. Test scanning
        console.log('\\n🔍 5. Email Scanning Test');
        await debug.testScan();
        
        console.log('\\n' + '='.repeat(60));
        console.log('💡 TROUBLESHOOTING TIPS:');
        console.log('• If extension not loaded: Refresh page or reinstall extension');
        console.log('• If API not connected: Check ngrok URL and backend status');
        console.log('• If no email content: Open an email in Gmail');
        console.log('• If no warnings: Try debug.forceScan() on phishing emails');
        console.log('• If duplicate buttons: Extension may have loaded multiple times');
        console.log('='.repeat(60));
    }
};

// Auto-run diagnosis
debug.diagnose();

// Make debug functions available globally
window.phishyDebug = debug;

console.log('\\n🔧 Debug functions available as window.phishyDebug');
console.log('Available functions:');
console.log('• phishyDebug.diagnose() - Run full diagnosis');
console.log('• phishyDebug.forceScan() - Force scan all emails');
console.log('• phishyDebug.testScan() - Test scan single email');
console.log('• phishyDebug.checkFlagButtons() - Check flag buttons');
console.log('• phishyDebug.testConfig() - Test API connection');

// Test for common phishing indicators in visible emails
console.log('\\n🎯 Checking for phishing indicators in visible emails...');
const allText = document.body.innerText.toLowerCase();
const phishingWords = ['urgent', 'verify', 'suspended', 'click here', 'act now', 'phishy', 'training'];
const foundWords = phishingWords.filter(word => allText.includes(word));

if (foundWords.length > 0) {
    console.log('🚨 Phishing indicators found:', foundWords);
    console.log('💡 These should trigger warnings if detection is working');
} else {
    console.log('ℹ️ No obvious phishing indicators found in current view');
}