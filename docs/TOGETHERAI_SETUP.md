# 🚀 Setup Guide: TogetherAI Integration

Get AI-powered commit suggestions using any model from TogetherAI!

---

## Quick Setup (3 Steps)

### 1. Get API Key
Visit [https://api.together.xyz/](https://api.together.xyz/) and create an account.
- Sign up (free tier available)
- Generate an API key
- **Set spending limits** (recommended!)

### 2. Choose Your Model
Browse available models at [https://api.together.xyz/models](https://api.together.xyz/models)

**Popular choices**:
- `deepseek-ai/deepseek-coder-33b-instruct` - Great for code
- `Qwen/Qwen2-72B-Instruct` - High quality, versatile
- `meta-llama/Llama-3-70b-chat-hf` - Powerful general model
- `mistralai/Mixtral-8x7B-Instruct-v0.1` - Fast and efficient

**Or use ANY model** - just copy the model ID!

### 3. Run Setup
```bash
commit-checker --setup-ai
```

Follow the prompts:
1. Paste your API key
2. Paste the model ID (e.g., `Qwen/Qwen2-72B-Instruct`)
3. Done!

---

## Usage

### Get AI Suggestions
```bash
# Stage your changes
git add .

# Get suggestions
commit-checker --ai-suggest
```

**Example Output**:
```
🤖 AI Suggestions (using Qwen/Qwen2-72B-Instruct):

1. feat: add user authentication module
2. feat(auth): implement JWT-based user login
3. Add user authentication with JWT tokens

💡 Pick one, modify it, or write your own!
```

### Check AI Status
```bash
commit-checker --ai-status
```

---

## Cost Information

TogetherAI charges per token used. Typical costs:
- **Per suggestion**: $0.001 - $0.01 (depending on model)
- **100 suggestions**: ~$0.10 - $1.00

**Recommendations**:
- ✅ Set spending limits on TogetherAI dashboard
- ✅ Start with smaller/cheaper models
- ✅ Use local models for frequent suggestions
- ✅ Reserve API for complex commits

**Check exact pricing**: [https://www.together.ai/pricing](https://www.together.ai/pricing)

---

## Model Selection Tips

**For commits** (fast, cheap):
- `deepseek-ai/deepseek-coder-6.7b-instruct`
- `meta-llama/Llama-2-7b-chat-hf`

**For quality** (slower, pricier):
- `Qwen/Qwen2-72B-Instruct`
- `meta-llama/Llama-3-70b-chat-hf`

**Balanced**:
- `deepseek-ai/deepseek-coder-33b-instruct`
- `mistralai/Mixtral-8x7B-Instruct-v0.1`

---

## Switching Models

```bash
# Run setup again
commit-checker --setup-ai

# Choose a different model ID
```

Your API key is saved - just update the model!

---

## Security

✅ API keys are **encrypted** and stored at `~/.commit-checker/config.json`
✅ Keys are **never logged** or shown in error messages
✅ **Secure deletion** when uninstalling commit-checker
✅ **No data sent** except your git diff (for suggestions)

---

## Troubleshooting

### "API key invalid"
- Check key at https://api.together.xyz/settings
- Regenerate if needed
- Re-run `--setup-ai`

### "Model not found"
- Verify model ID at https://api.together.xyz/models
- Copy/paste exact ID
- Check for typos

### "Rate limit exceeded"
- You've hit your usage limit
- Wait a few minutes or increase limits on TogetherAI

### "No AI suggestions"
- Make sure you have staged changes: `git add .`
- Check AI status: `commit-checker --ai-status`
- Verify API key setup

---

## FAQ

**Q: Can I use free tier?**
A: Yes! TogetherAI offers free credits for new users.

**Q: How many suggestions per commit?**
A: Typically 3 suggestions per request.

**Q: Can I use multiple models?**
A: Yes, run `--setup-ai` anytime to switch.

**Q: What if I don't want to use API?**
A: Use local models instead! Run `commit-checker --download-models`

**Q: Is my code sent to TogetherAI?**
A: Only the git diff summary (changes, not full files).

---

**Enjoy AI-powered suggestions! 🤖✨**
