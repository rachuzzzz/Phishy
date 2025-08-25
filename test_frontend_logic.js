// Test the frontend classification logic
function testClassification() {
    const testCases = [
        "hi",
        "hello",
        "what is phishing",
        "show click trend", 
        "show click trends",
        "current analytics",
        "analytics overview",
        "which users clicked most",
        "display metrics",
        "cybersecurity help",
        "tell more about user u2204052",
        "show user activity for u2204052",
        "more about user thomasraisen122@gmail.com"
    ];
    
    console.log("Testing Frontend Classification Logic:");
    console.log("=====================================");
    
    testCases.forEach(message => {
        const lowerMessage = message.toLowerCase();
        let predictedIntent = 'CHAT'; // Default to chat
        
        // Direct analytics detection (same logic as frontend)
        if (lowerMessage.includes('click') && (lowerMessage.includes('trend') || lowerMessage.includes('show') || lowerMessage.includes('current')) ||
            lowerMessage.includes('analytics') || 
            lowerMessage.includes('clicktrend') ||
            (lowerMessage.includes('show') && (lowerMessage.includes('click') || lowerMessage.includes('analytics'))) ||
            lowerMessage.includes('user') && (lowerMessage.includes('clicked') || lowerMessage.includes('most')) ||
            // Specific user queries - check for user IDs or "tell more about user"
            (lowerMessage.includes('user') && (lowerMessage.includes('u2204') || lowerMessage.includes('@') || lowerMessage.includes('tell') || lowerMessage.includes('more about'))) ||
            lowerMessage.includes('metrics') || 
            lowerMessage.includes('statistics') ||
            lowerMessage.includes('dashboard') ||
            lowerMessage.includes('report') && !lowerMessage.includes('what')) {
            predictedIntent = 'REPORT';
        }
        
        console.log(`"${message}" -> ${predictedIntent}`);
    });
}

// Run the test
testClassification();