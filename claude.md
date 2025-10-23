# Writing Articles for Horse Energy Blog

This guide explains how to use Claude's subagent workflow to write data-driven articles for the Horse Energy blog and deploy them to horse.energy.

## Overview

Horse Energy is a data-driven blog focusing on economic analysis, democratic institutions, and empirical research. Articles should be:
- **Empirically grounded** with specific data, citations, and sources
- **Analytically rigorous** without sensationalism
- **Well-structured** with clear sections and visualizations
- **Properly cited** with inline superscript citations and a sources section

## Subagent Workflow for Article Creation

### Step 1: Use the Planner Agent

**Purpose:** Create a strategic content plan with angle, outline, and research needs.

```bash
Use Task tool with subagent_type=planner
```

**What to provide:**
- Article topic or thesis
- Key questions to explore
- Available data sources (if any)
- Target audience and style (Horse Energy: data-driven, academic tone)

**What you'll get:**
- Compelling angle/thesis
- Detailed outline with sections
- Key data points to emphasize
- What research the researcher should gather
- Suggested visualizations

### Step 2: Use the Researcher Agent

**Purpose:** Conduct comprehensive literature searches and gather information.

```bash
Use Task tool with subagent_type=researcher
```

**What to provide:**
- The content plan from the planner
- Specific research questions
- Data requirements (statistics, benchmarks, historical comparisons)

**What you'll get:**
- Comprehensive research findings
- Data sources and citations
- Key statistics and figures
- Historical context and comparisons

### Step 3: Use the Writer Agent

**Purpose:** Write comprehensive articles with data visualizations based on plans and research.

```bash
Use Task tool with subagent_type=writer
```

**What to provide:**
- Content plan from planner
- Research findings from researcher
- Template requirements (see below)
- Citation requirements

**What you'll get:**
- Complete HTML article
- Inline citations
- Data visualizations using Plotly.js
- Sources section

## Horse Energy Template Requirements

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Title - Horse Energy</title>
    <style>
        :root {
            --bg: #f5f5f5;
            --fg: #1a1a1a;
            --muted: #666;
        }

        body {
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            background: var(--bg);
            color: var(--fg);
            padding: 2rem 1rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }

        .subtitle {
            font-size: 1.2rem;
            color: var(--muted);
            margin-bottom: 0.5rem;
        }

        .meta {
            color: var(--muted);
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }

        .back-to-blog {
            display: inline-block;
            margin-bottom: 2rem;
            color: #3b82f6;
            text-decoration: none;
            font-weight: 500;
        }

        .back-to-blog:hover {
            text-decoration: underline;
        }

        .key-stat {
            background: #e8f4f8;
            border-left: 4px solid #3b82f6;
            padding: 1rem;
            margin: 1.5rem 0;
        }

        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }

        .comparison-table th,
        .comparison-table td {
            border: 1px solid #ddd;
            padding: 0.75rem;
            text-align: left;
        }

        .comparison-table th {
            background: #f8f9fa;
            font-weight: 600;
        }

        .chart-container {
            margin: 2rem 0;
            padding: 1rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .chart-title {
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--fg);
        }

        sup {
            font-size: 0.7rem;
            color: #3b82f6;
        }
    </style>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>

<a href="index.html" class="back-to-blog">← Back to Horse Energy</a>

<h1>Article Title Here</h1>
<p class="subtitle">A data-driven analysis of [key topic]</p>
<p class="meta">Month Day, 2025 | Data Analysis</p>

<!-- Article content here -->

<h2>Sources & References</h2>

<p style="font-size: 0.9rem; line-height: 1.8; color: var(--muted);">
    <strong>[1]</strong> Source citation with link<br>
    <strong>[2]</strong> Source citation with link<br>
    <!-- etc -->
</p>

</body>
</html>
```

### Key CSS Variables

- **Font:** `system-ui, -apple-system, sans-serif` (NOT Georgia or serif fonts)
- **Background:** `#f5f5f5` (light gray, not white)
- **Text color:** `#1a1a1a` (dark, not pure black)
- **Muted text:** `#666`
- **Accent color:** `#3b82f6` (blue)
- **No container boxes** - content flows naturally on gray background

### Citation Style

Use inline superscript citations:

```html
<p>OpenAI is valued at $157 billion.<sup>[2]</sup> By October 2025,
the company had reached $13 billion in annual recurring revenue.<sup>[11]</sup></p>
```

Include full sources section at end:

```html
<h2>Sources & References</h2>

<p style="font-size: 0.9rem; line-height: 1.8; color: var(--muted);">
    <strong>[1]</strong> Author. "Title" <em>Publication</em> (Date).
    <a href="URL" target="_blank" style="color: #3b82f6;">Link</a><br>
</p>
```

## Deploying to Horse Energy

### Step 1: Create the HTML File

Save your article in the `HorseEnergy/` directory:

```bash
/Users/adnanakil/Documents/Projects/NewProjects/Distribution/HorseEnergy/your_article.html
```

### Step 2: Update the Index

Add entry to `/Users/adnanakil/Documents/Projects/NewProjects/Distribution/HorseEnergy/index.html`:

```html
<article class="post-entry">
    <div class="post-date">Month Day, 2025</div>
    <div class="post-title">
        <a href="your_article.html">Article Title</a>
    </div>
    <p class="post-excerpt">
        Brief description of the article (1-2 sentences)
    </p>
</article>
```

Add this at the TOP of the post list (most recent first).

### Step 3: Commit to Git

```bash
git add HorseEnergy/your_article.html HorseEnergy/index.html
git commit -m "Add [article title] to Horse Energy

- Brief description of article
- Key data points covered
- Sources cited"
```

### Step 4: Push to GitHub

```bash
git push
```

### Step 5: Deploy to Vercel

```bash
vercel --prod --yes
```

The article will be live at `https://horse.energy/HorseEnergy/your_article.html`

## Best Practices

### Data and Citations

1. **Cite everything** - Every claim needs a source
2. **Use specific numbers** - "$16B annual loss" not "massive losses"
3. **Include context** - Compare to historical examples
4. **Link sources** - Provide URLs whenever possible

### Writing Style

1. **Professional tone** - Academic but accessible
2. **No superlatives** - Avoid "most impressive," "revolutionary," etc.
3. **Data-first** - Lead with numbers, not opinions
4. **Steel-man opponents** - Present counter-arguments fairly

### Structure

1. **Clear sections** - Use h2 for main sections, h3 for subsections
2. **Visualizations** - Include charts for key data (using Plotly.js)
3. **Key stats boxes** - Highlight important comparisons
4. **Tables** - Use for side-by-side comparisons

### Article Length

- **Minimum:** 2,000 words with substantive analysis
- **Optimal:** 3,000-5,000 words for comprehensive coverage
- **Maximum:** 8,000 words (only if necessary for depth)

## Example Workflow

```bash
# 1. Plan the article
"I want to write about [topic]. Use the planner agent to create a strategic content plan."

# 2. Gather research
"Use the researcher agent to gather data on [specific questions from plan]."

# 3. Write the article
"Use the writer agent to write a comprehensive article based on the plan and research.
Make sure it matches the Horse Energy template with:
- system-ui font
- light gray background
- inline superscript citations
- comprehensive sources section at end"

# 4. Review and edit
Read through the generated article, check citations, verify data

# 5. Deploy
git add HorseEnergy/article.html HorseEnergy/index.html
git commit -m "Add article"
git push
vercel --prod --yes
```

## Common Mistakes to Avoid

1. **Wrong font** - Don't use Georgia or serif fonts (use system-ui)
2. **Wrong background** - Don't use white containers (use light gray background)
3. **Missing citations** - Every major claim needs a source
4. **Outdated data** - Always check dates (we're in October 2025)
5. **Sensationalist tone** - Stick to data-driven analysis
6. **Missing index update** - Always add new articles to index.html
7. **Wrong section numbers** - Update section numbers if you remove sections

## Vercel Configuration

The site uses a redirect to make the blog index the homepage:

```json
{
  "redirects": [
    {
      "source": "/",
      "destination": "/HorseEnergy/index.html",
      "permanent": false
    }
  ]
}
```

This means `horse.energy` → `horse.energy/HorseEnergy/index.html`

## Repository Structure

```
Distribution/
├── HorseEnergy/
│   ├── index.html              # Blog homepage (list of articles)
│   ├── article1.html           # Individual articles
│   ├── article2.html
│   └── ...
├── index.html                  # Old homepage (not used)
├── vercel.json                 # Redirect configuration
└── claude.md                   # This file
```

## Questions?

If you need to modify the template or have questions about the workflow, refer to existing articles in the `HorseEnergy/` directory as examples. The most recent articles follow the current template standards.
