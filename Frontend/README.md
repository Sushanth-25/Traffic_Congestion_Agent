# Traffic AI Assistant Frontend

A responsive web interface for interacting with the Traffic AI Assistant powered by IBM watsonx and Langflow.

## Features

✨ **Modern Chat Interface**
- Clean, intuitive design with IBM branding
- Real-time message updates
- Typing indicators for better UX
- Message timestamps

📱 **Fully Responsive**
- Mobile-first design using Tailwind CSS
- Optimized for phones, tablets, and desktops
- Adaptive layout and font sizes

🚀 **Langflow Integration**
- Seamless API integration with Langflow
- Real-time communication with AI agent
- Error handling and connection status monitoring

⚡ **User Experience**
- Sample queries for quick start
- Auto-resizing text input
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)
- Smooth animations and transitions

## Setup Instructions

### 1. Configure Langflow Connection

Edit the `config.js` file to connect to your Langflow instance:

```javascript
const LANGFLOW_CONFIG = {
    apiUrl: 'http://localhost:7860/api/v1/run',
    flowId: 'your-flow-id-here', // Replace with your actual Flow ID
    tweaks: {} // Add any component tweaks if needed
};
```

### 2. Get Your Flow ID

1. Open Langflow UI in your browser
2. Navigate to your flow
3. Copy the Flow ID from the URL or flow settings
4. Paste it in `config.js`

### 3. Start Langflow Server

Make sure your Langflow server is running:

```bash
# From the project root
langflow run --host 0.0.0.0 --port 7860
```

### 4. Open the Frontend

Simply open `index.html` in your web browser:

- **Option 1**: Double-click `index.html`
- **Option 2**: Use a local server (recommended):

```bash
# Using Python
python -m http.server 8000

# Using Node.js (if you have http-server installed)
npx http-server

# Then open http://localhost:8000 in your browser
```

## File Structure

```
Frontend/
├── index.html      # Main HTML file with chat UI
├── app.js          # JavaScript logic and Langflow API integration
├── config.js       # Langflow configuration
└── README.md       # This file
```

## Customization

### Styling

The interface uses Tailwind CSS. You can customize colors in the `tailwind.config` section of `index.html`:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#0f62fe',
                // Add your custom colors here
            }
        }
    }
}
```

### API Integration

Modify the `callLangflowAPI` function in `app.js` to adjust the API payload structure:

```javascript
const payload = {
    input_value: message,
    output_type: "chat",
    input_type: "chat",
    tweaks: CONFIG.TWEAKS
};
```

### Sample Queries

Update the welcome message buttons in `index.html` to show relevant queries for your use case.

## Troubleshooting

### Connection Issues

If you see "Disconnected" status:

1. Verify Langflow is running: `http://localhost:7860`
2. Check the Flow ID in `config.js`
3. Open browser console (F12) for error details
4. Ensure CORS is enabled on Langflow server

### API Errors

Common issues:

- **404 Error**: Wrong Flow ID or API URL
- **CORS Error**: Langflow not allowing requests from your origin
- **500 Error**: Check Langflow logs for flow execution errors

### Response Format Issues

If messages aren't displaying correctly, check the `extractMessageFromOutput` function in `app.js` and adjust it to match your flow's output format.

## Browser Compatibility

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Internet Explorer (not supported)

## Development

### Adding Features

1. **New UI elements**: Edit `index.html`
2. **New functionality**: Add to `app.js`
3. **Styling**: Use Tailwind classes or add custom CSS

### Testing

Open browser DevTools (F12) to see:
- Console logs for debugging
- Network tab for API requests
- Application tab for storage

## Production Deployment

For production deployment:

1. Update `config.js` with production Langflow URL
2. Consider using environment variables
3. Add authentication if needed
4. Optimize assets and enable caching
5. Use HTTPS for secure connections

## Support

For issues related to:
- **Frontend**: Check browser console and this README
- **Langflow**: Refer to Langflow documentation
- **API**: Check Langflow server logs

## License

Part of the IBM Hackathon Project
