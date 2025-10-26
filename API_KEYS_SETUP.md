# 🔑 API Keys Setup Guide

## Quick Start (3 Steps)

### 1️⃣ Install Required Package
```bash
pip install python-dotenv openai
```

### 2️⃣ Create Your `.env` File
Copy the example file and add your API keys:

```bash
# Copy the template
copy .env.example .env

# Or on Mac/Linux:
cp .env.example .env
```

### 3️⃣ Add Your API Keys to `.env`
Open `.env` in a text editor and replace the placeholder keys:

```env
# ============================================================
# OPENAI API (Required for ChatGPT features)
# ============================================================
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
OPENAI_MODEL=gpt-4o
```

---

## 📍 Where API Keys Are Used

### **Backend (Python)**

#### ✅ `config.py`
- Loads API keys from `.env` file
- Makes them available to all Python modules
- Usage:
  ```python
  from config import OPENAI_API_KEY, OPENAI_MODEL
  ```

#### ✅ `src/ses_agents.py`
- Uses OpenAI API for AI-powered analysis
- Automatically loads keys from `config.py`
- Fallback to environment variables if config not found

---

## 🔐 How to Get API Keys

### **OpenAI API Key** (For ChatGPT)

1. Go to: https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste it in your `.env` file:
   ```env
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
   ```

### **Anthropic API Key** (Optional - for Claude)

1. Go to: https://console.anthropic.com/
2. Sign in and navigate to API Keys
3. Create a new key
4. Add to `.env`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   ```

---

## ⚠️ Security Best Practices

### ✅ DO:
- ✅ Keep `.env` file **LOCAL ONLY** (already in `.gitignore`)
- ✅ Use different keys for development and production
- ✅ Rotate keys regularly
- ✅ Set spending limits on API provider dashboards
- ✅ Use environment variables for CI/CD

### ❌ DON'T:
- ❌ **NEVER** commit `.env` to Git
- ❌ **NEVER** share your API keys publicly
- ❌ **NEVER** hardcode keys in source code
- ❌ **NEVER** post keys in issues or forums

---

## 🧪 Testing Your Setup

### Test 1: Check if `.env` is loaded
```python
python -c "import config; print('OpenAI Key:', config.OPENAI_API_KEY[:10] + '...')"
```

### Test 2: Verify OpenAI connection
```python
python -c "import openai; import config; openai.api_key = config.OPENAI_API_KEY; print('✓ API key configured')"
```

### Test 3: Run the agent
```bash
python src/ses_agents.py
```

---

## 🌐 Frontend (JavaScript)

### **Option 1: Backend API (Recommended)**
Don't expose API keys in frontend. Instead:
1. Create a backend API endpoint in Python
2. Frontend calls your backend
3. Backend uses the API keys securely

### **Option 2: Environment Variables (Build-time)**
For frameworks like React/Vue:

Create `frontend/.env`:
```env
# Build-time only - still goes to client!
VITE_API_URL=http://localhost:5000
# DO NOT PUT API KEYS HERE
```

Use in JavaScript:
```javascript
const API_URL = import.meta.env.VITE_API_URL;
```

⚠️ **Never put API keys in frontend `.env` files!**

---

## 📁 File Structure

```
Bite-Piper/
├── .env                    # ← YOUR API KEYS GO HERE (gitignored)
├── .env.example            # Template to copy from
├── config.py               # Loads from .env
├── src/
│   └── ses_agents.py       # Uses API keys from config
└── frontend/
    └── app.js              # Calls backend API (no keys)
```

---

## 🐛 Troubleshooting

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### "No module named 'openai'"
```bash
pip install openai
```

### "API key not found"
1. Check `.env` file exists in project root
2. Verify no extra spaces: `OPENAI_API_KEY=sk-xxx` (not `= sk-xxx`)
3. Restart your terminal/IDE after creating `.env`

### "Invalid API key"
1. Check key is copied correctly (no extra characters)
2. Verify key is active on OpenAI dashboard
3. Check billing is enabled

### "Rate limit exceeded"
1. Check your OpenAI usage dashboard
2. Add billing/increase limits
3. Implement retry logic with exponential backoff

---

## 💰 Cost Management

### OpenAI Pricing (as of 2024)
- **GPT-4o**: ~$2.50 per 1M input tokens
- **GPT-3.5-turbo**: ~$0.50 per 1M input tokens

### Tips to Save Money:
- Use `gpt-3.5-turbo` for development
- Set `OPENAI_MAX_TOKENS` to limit response length
- Implement caching for repeated queries
- Set monthly spending limits on OpenAI dashboard

---

## 🔄 Alternative: Using Free/Local Models

### Ollama (Free, runs locally)
```bash
# Install Ollama
# Visit: https://ollama.com/

# Run a model
ollama run llama2

# Update config to use local model
OPENAI_API_KEY=ollama
OPENAI_MODEL=llama2
```

---

## ✅ Checklist

- [ ] Installed `python-dotenv` and `openai`
- [ ] Created `.env` from `.env.example`
- [ ] Added OpenAI API key to `.env`
- [ ] Verified `.env` is in `.gitignore`
- [ ] Tested configuration with test commands
- [ ] Set spending limits on OpenAI dashboard
- [ ] Never committed API keys to Git

---

## 📞 Need Help?

- OpenAI Documentation: https://platform.openai.com/docs
- Check API status: https://status.openai.com/
- Bite-Piper Issues: Create an issue in your repository

**Remember**: Keep your API keys secret and rotate them regularly! 🔐
