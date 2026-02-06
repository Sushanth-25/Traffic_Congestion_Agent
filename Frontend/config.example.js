// Configuration template for Langflow integration
// Copy this file to config.js and fill in your actual values

const LANGFLOW_CONFIG = {
    // Local Langflow API endpoint (running on port 7860)
    apiUrl: 'http://localhost:7860/api/v1/run',

    // Your Flow ID - Get from LangFlow URL: http://localhost:7860/flow/<FLOW_ID>
    flowId: 'your-flow-id-here',
    
    // Your application token (from LangFlow settings, or leave empty for local without auth)
    applicationToken: '',

    // Organization ID (not needed for local, leave empty)
    organizationId: '',

    // Optional tweaks
    tweaks: {}
};