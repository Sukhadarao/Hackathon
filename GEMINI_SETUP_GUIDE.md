# Google Gemini API Setup Guide

## Setting up your .env file

Your `.env` file should contain authentication credentials for Google Gemini API. Based on your setup method, add the appropriate variables:

### Option 1: Google AI Studio (Recommended for Development)

**Steps:**
1. Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Add these lines to your `.env` file:

```bash
GOOGLE_API_KEY=your_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

### Option 2: Vertex AI with User Credentials

**Steps:**
1. Install gcloud CLI: https://cloud.google.com/sdk/docs/install
2. Run: `gcloud auth application-default login`
3. Add these lines to your `.env` file:

```bash
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

### Option 3: Vertex AI Express Mode

**Steps:**
1. Sign up for Express Mode to get your API key
2. Add these lines to your `.env` file:

```bash
GOOGLE_API_KEY=your_express_mode_api_key
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

### Option 4: Service Account (Production)

**Steps:**
1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Add this line to your `.env` file:

```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/keyfile.json
```

---

## Handling Quota Limits

### Understanding the 429 Error

The error you encountered means:
- **Free tier limit:** 20 requests per day for `gemini-2.5-flash`
- **Error message:** "RESOURCE_EXHAUSTED"

### Solutions

#### 1. **Automatic Retry (Already Configured)**
The agent now has retry configuration:
- Initial delay: 2 seconds
- Max attempts: 3 retries
- Will wait 30+ seconds if quota exceeded, then retry

#### 2. **Increase Your Quota**
- Visit [Google AI Studio Quotas](https://ai.google.dev/pricing)
- Upgrade to a paid tier for higher limits
- Or request quota increase in Google Cloud Console

#### 3. **Use Different Model**
Change the model in `agent.py`:
```python
model='gemini-1.5-flash'  # Try alternative model
```

#### 4. **Wait for Quota Reset**
Free tier quotas reset:
- **Per minute:** Some limits reset every 60 seconds
- **Per day:** Daily quota resets at midnight PST

---

## Testing Your Configuration

After setting up your `.env` file:

1. **Close and reopen your terminal** (or run `adk run my_agent`)
2. **Test the connection:**
   ```bash
   adk run my_agent
   ```
3. **Try a simple query:**
   ```
   list all users
   ```

---

## Security Best Practices

⚠️ **IMPORTANT:**
- Never commit `.env` to version control (already gitignored)
- Never share your API keys publicly
- Rotate keys if accidentally exposed
- Use Secret Manager for production deployments

---

## Current Configuration

Your agent is now configured with:
- ✅ Automatic retry on quota errors (3 attempts, 2s delay)
- ✅ Model: `gemini-2.5-flash`
- ✅ Environment file support enabled in VS Code
- ✅ PostgreSQL database schema embedded

---

## Troubleshooting

### Still getting 429 errors?
- Wait 30-60 seconds between requests
- Check your current usage: https://ai.dev/rate-limit
- Consider upgrading your API tier

### Environment variables not loading?
- Restart your terminal
- Check `.env` file is in project root
- Verify no typos in variable names
- Run: `Get-ChildItem Env:GOOGLE_API_KEY` (PowerShell) to check if loaded

### Model not responding?
- Verify API key is valid
- Check internet connection
- Review logs: `C:\Users\I760880\AppData\Local\Temp\agents_log\`

---

## Useful Links

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Pricing](https://ai.google.dev/pricing)
- [Vertex AI](https://cloud.google.com/vertex-ai)
