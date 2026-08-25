# 🎯 TimesJobs Scraper - AI-Ready Job Data Extractor

[![Apify](https://img.shields.io/badge/Apify-Actor-00D4FF?style=for-the-badge&logo=apify)](https://apify.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AI Ready](https://img.shields.io/badge/AI-Ready-10B981?style=for-the-badge&logo=openai)](https://www.anthropic.com)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-7C3AED?style=for-the-badge)](https://modelcontextprotocol.io)

> 🚀 **Extract job listings from TimesJobs.com** with full structured data - perfect for ChatGPT, Claude, AI agents, and MCP integrations!

---

## ✨ Why This Scraper?

TimesJobs.com is one of India's largest job portals with **millions of job listings** across all industries. This actor provides:

- 🎯 **AI-Optimized Output** - Clean JSON ready for GPT-4, Claude, and other LLMs
- 🔄 **MCP Protocol Support** - Seamless integration with Model Context Protocol agents
- 📊 **Rich Data Fields** - Job title, company, salary, skills, location, experience, and more
- ⚡ **Fast & Reliable** - Handles pagination, anti-bot measures, and errors gracefully
- 🌐 **Proxy Support** - Built-in Apify proxy rotation for stable scraping
- 💰 **Cost-Effective** - Only $0.005 per result + $0.05 per run

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| **🔍 Smart Search** | Search by keywords, location, experience level |
| **📦 Structured Data** | Consistent JSON schema for every job listing |
| **🤖 AI-First Design** | Optimized for ChatGPT, Claude, and MCP agents |
| **🌐 Proxy Support** | Residential proxies included for reliability |
| **⚡ Fast Extraction** | Scrapes 50+ jobs in under 1 minute |
| **📊 Rich Metadata** | Company, salary, skills, posted date, and more |
| **🔄 Pagination** | Automatically handles multiple pages |
| **🛡️ Error Handling** | Robust parsing with graceful degradation |

---

## 📊 Output Schema

Each job listing contains the following fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `jobTitle` | string | Job position title | "Senior Python Developer" |
| `companyName` | string | Hiring company name | "Tech Solutions India" |
| `location` | string | Job location | "Bangalore, Karnataka" |
| `experience` | string | Required experience | "3-5 Years" |
| `salary` | string | Salary range | "₹8-12 Lakhs P.A." |
| `skills` | string | Required skills | "Python, Django, AWS, Docker" |
| `jobDescription` | string | Full job description | "We are looking for..." |
| `postedDate` | string | When job was posted | "2 days ago" |
| `jobLink` | string | Direct job URL | "https://www.timesjobs.com/..." |

### 📄 Example Output

```json
{
  "jobTitle": "Senior Python Developer",
  "companyName": "Tech Mahindra",
  "location": "Bangalore, Pune",
  "experience": "4-7 Years",
  "salary": "₹10-15 Lakhs P.A.",
  "skills": "Python, Django, Flask, REST APIs, AWS, Docker, Kubernetes",
  "jobDescription": "Looking for experienced Python developer to join our cloud team...",
  "postedDate": "Posted 3 days ago",
  "jobLink": "https://www.timesjobs.com/job-detail/python-developer-xyz-123"
}
```

---

## 🚀 Quick Start

### 1️⃣ **Basic Usage**

```javascript
// Using Apify SDK
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'YOUR_APIFY_TOKEN',
});

const run = await client.actor('YOUR_USERNAME/timesjobs-scraper').call({
    searchKeywords: 'Data Scientist',
    searchLocation: 'Mumbai',
    maxResults: 100
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### 2️⃣ **Python Integration**

```python
from apify_client import ApifyClient

client = ApifyClient('YOUR_APIFY_TOKEN')

run = client.actor('YOUR_USERNAME/timesjobs-scraper').call(
    run_input={
        'searchKeywords': 'Machine Learning Engineer',
        'searchLocation': 'Hyderabad',
        'maxResults': 50
    }
)

items = client.dataset(run['defaultDatasetId']).list_items().items
print(items)
```

### 3️⃣ **Direct API Call**

```bash
curl -X POST https://api.apify.com/v2/acts/YOUR_USERNAME~timesjobs-scraper/runs \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_APIFY_TOKEN' \
  -d '{
    "searchKeywords": "DevOps Engineer",
    "searchLocation": "Delhi NCR",
    "maxResults": 75
  }'
```

---

## 🤖 AI Integration

### ChatGPT / GPT-4

Perfect for building job search assistants:

```javascript
// Fetch jobs and pass to GPT-4
const jobs = await fetchJobsFromApify();
const response = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [{
    role: "user",
    content: `Analyze these job listings and suggest the best matches for a candidate with 5 years Python experience: ${JSON.stringify(jobs)}`
  }]
});
```

### Claude / Anthropic API

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_KEY")
jobs = fetch_jobs_from_apify()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{
        "role": "user",
        "content": f"Compare these job offers and create a recommendation report: {jobs}"
    }]
)
```

### MCP (Model Context Protocol)

This actor is fully compatible with MCP servers:

```json
{
  "mcpServers": {
    "timesjobs": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server-apify"],
      "env": {
        "APIFY_API_TOKEN": "YOUR_TOKEN",
        "ACTOR_ID": "YOUR_USERNAME/timesjobs-scraper"
      }
    }
  }
}
```

---

## 📋 Input Configuration

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `searchKeywords` | string | ✅ Yes | - | Job keywords (e.g., "Python Developer") |
| `searchLocation` | string | ❌ No | "" | Job location (e.g., "Bangalore") |
| `maxResults` | integer | ❌ No | 50 | Max number of jobs to scrape (1-1000) |
| `experienceLevel` | enum | ❌ No | "" | Filter: "", "0-2", "2-5", "5-10", "10+" |
| `proxyConfig` | object | ❌ No | Residential | Apify proxy configuration |

### 🎯 Input Examples

#### Basic Search
```json
{
  "searchKeywords": "Python Developer"
}
```

#### Advanced Search
```json
{
  "searchKeywords": "Full Stack Developer",
  "searchLocation": "Remote",
  "maxResults": 100,
  "experienceLevel": "2-5"
}
```

#### With Custom Proxy
```json
{
  "searchKeywords": "Data Engineer",
  "searchLocation": "Bangalore",
  "maxResults": 200,
  "proxyConfig": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  }
}
```

---

## 💡 Use Cases

### 🎓 **For Job Seekers**
- Monitor new job postings matching your skills
- Compare salaries across companies
- Track job market trends in your industry

### 🏢 **For Recruiters**
- Analyze competitor job postings
- Research salary benchmarks
- Identify skill demand patterns

### 🤖 **For AI Developers**
- Build intelligent job matching systems
- Create personalized job recommendation engines
- Train ML models on job market data

### 📊 **For Researchers**
- Study employment trends in India
- Analyze skill requirements by industry
- Track hiring patterns over time

---

## 🔧 Advanced Configuration

### Proxy Settings

The actor uses **Apify Residential Proxies** by default for maximum reliability:

```json
{
  "proxyConfig": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  }
}
```

### Custom Experience Filters

```json
{
  "searchKeywords": "DevOps",
  "experienceLevel": "5-10"
}
```

Options:
- `""` - All experience levels
- `"0-2"` - Entry level (0-2 years)
- `"2-5"` - Mid level (2-5 years)
- `"5-10"` - Senior level (5-10 years)
- `"10+"` - Expert level (10+ years)

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| **Average Run Time** | 30-60 seconds |
| **Jobs Per Run** | 50-200 (configurable) |
| **Success Rate** | 95%+ |
| **Proxy Support** | ✅ Residential |
| **Cost Per Job** | $0.005 |
| **Cost Per Run** | $0.05 + $0.005/result |

---

## 🛠️ Technical Details

### Architecture
- **Language:** Python 3.11
- **Framework:** Apify SDK 2.0
- **Parser:** BeautifulSoup4 + lxml
- **HTTP Client:** httpx (async)
- **Proxy:** Apify Residential Proxies

### Data Quality
- ✅ **Deduplication:** Jobs are unique per run
- ✅ **Validation:** All required fields validated
- ✅ **Cleaning:** Text normalized and whitespace removed
- ✅ **Error Handling:** Graceful degradation on missing fields

### Scalability
- Handles **1000+ jobs** per run
- Async/await for concurrent requests
- Automatic pagination
- Rate limiting protection

---

## 🔍 Troubleshooting

### No Results Returned

**Solution:**
1. Check if your search keywords are too specific
2. Try broader location (e.g., "India" instead of specific city)
3. Remove experience level filter
4. Verify TimesJobs.com is accessible from your location

### Proxy Errors

**Solution:**
1. Ensure your Apify account has proxy access
2. Use RESIDENTIAL proxy group (default)
3. Check proxy configuration in input

### Missing Fields

**Solution:**
- Some jobs don't include all fields (e.g., salary)
- The scraper handles missing data gracefully
- Check `jobLink` to verify source data

---

## 🌟 Best Practices

### 1. **Optimize Search Keywords**
```json
{
  "searchKeywords": "Python Django AWS",  // ✅ Good - specific
  "searchKeywords": "job"                 // ❌ Bad - too generic
}
```

### 2. **Use Realistic maxResults**
```json
{
  "maxResults": 100  // ✅ Good for most use cases
}
```

### 3. **Combine with AI**
```javascript
// Fetch jobs
const jobs = await scrapeJobs();

// Analyze with AI
const insights = await analyzeWithClaude(jobs);
```

---

## 🔄 Integration Examples

### Zapier Webhook
```json
POST https://hooks.zapier.com/YOUR_WEBHOOK
{
  "jobs": [...results from actor...]
}
```

### Google Sheets Export
```javascript
const run = await client.actor('YOUR_USERNAME/timesjobs-scraper').call(input);
await client.dataset(run.defaultDatasetId).exportToGoogleSheets(sheetId);
```

### Slack Notification
```javascript
const jobs = await getDatasetItems(runId);
await postToSlack({
  text: `Found ${jobs.length} new jobs matching your criteria!`,
  attachments: jobs.slice(0, 5).map(job => ({
    title: job.jobTitle,
    text: `${job.companyName} - ${job.location}`,
    color: "good"
  }))
});
```

---

## 📚 Resources

- 📖 [Apify Documentation](https://docs.apify.com)
- 🤖 [OpenAI API](https://platform.openai.com/docs)
- 🧠 [Anthropic Claude](https://docs.anthropic.com)
- 🔗 [MCP Protocol](https://modelcontextprotocol.io)
- 💼 [TimesJobs](https://www.timesjobs.com)

---

## 🆘 Support

- 💬 **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/timesjobs-scraper/issues)
- 📧 **Email:** support@example.com
- 🐛 **Bug Reports:** Use GitHub Issues with detailed reproduction steps
- 💡 **Feature Requests:** Open a discussion in GitHub

---

## 📝 Changelog

### Version 1.0.0 (2025-01-XX)
- ✨ Initial release
- 🎯 Support for keyword and location search
- 📊 9 structured output fields
- 🤖 AI-ready JSON output
- 🔄 MCP protocol compatible
- 🌐 Residential proxy support
- ⚡ Async/await architecture

---

## 🏆 Why Choose This Actor?

| Feature | This Actor | Others |
|---------|------------|--------|
| **AI Integration** | ✅ Optimized for GPT-4, Claude | ❌ Generic output |
| **MCP Support** | ✅ Native support | ❌ Not supported |
| **Data Quality** | ✅ 9 structured fields | ⚠️ Varies |
| **Proxy Included** | ✅ Residential | ⚠️ Sometimes |
| **Documentation** | ✅ Comprehensive | ⚠️ Minimal |
| **Pricing** | ✅ $0.005/result | 💰 Often higher |
| **Maintenance** | ✅ Active | ⚠️ Often abandoned |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

MIT License - feel free to use this actor for personal or commercial projects.

---

## 🌟 Star Us!

If this actor helps you build amazing AI-powered job search tools, please ⭐ star the repository!

---

<div align="center">

**Built with ❤️ for the AI community**

[🚀 Try it now on Apify](https://apify.com) | [📖 Documentation](https://docs.apify.com) | [🤖 AI Examples](https://github.com)

</div>

---

## 🎯 Quick Command Reference

```bash
# Install Apify CLI
npm install -g apify-cli

# Clone this actor
apify pull YOUR_USERNAME/timesjobs-scraper

# Run locally
apify run

# Push to Apify
apify push
```

---

## 💻 Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/timesjobs-scraper.git
cd timesjobs-scraper

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export APIFY_TOKEN=your_token_here

# Run locally
python -m src.main
```

---

## 🔐 Security

- ✅ No credentials stored in code
- ✅ Secure proxy rotation
- ✅ Rate limiting protection
- ✅ HTTPS-only connections
- ✅ Input validation

---

## 🎨 Customization

Want to customize the scraper? Key files:

- `src/main.py` - Main scraping logic
- `.actor/input_schema.json` - Input configuration
- `.actor/actor.json` - Actor metadata
- `requirements.txt` - Python dependencies

---

## 📊 Example Workflow

```mermaid
graph LR
    A[User Input] --> B[TimesJobs Scraper]
    B --> C[Raw HTML]
    C --> D[Parsed Data]
    D --> E[Apify Dataset]
    E --> F[AI Agent]
    F --> G[Insights]
```

---

## 🎓 Learning Resources

New to web scraping or Apify? Check out:

- [Apify Academy](https://docs.apify.com/academy)
- [Web Scraping Best Practices](https://blog.apify.com)
- [Python BeautifulSoup Tutorial](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

<div align="center">

### 🚀 Ready to extract job data at scale?

[**Start Scraping Now →**](https://console.apify.com)

</div>
