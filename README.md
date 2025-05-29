# Static Site Generator

A simple static site generator built with Node.js that converts Markdown content into HTML pages.

## Features

- Markdown content support
- HTML templates
- Static asset handling
- Clean and responsive default design

## Getting Started

### Installation

1. Clone this repository
2. Install dependencies:

```bash
npm install
```

### Usage

1. Add your Markdown content to the `content` directory
2. Customize templates in the `templates` directory (optional)
3. Add static files (CSS, images, etc.) to the `static` directory (optional)
4. Build the site:

```bash
npm run build
```

5. The generated site will be in the `public` directory
6. To preview the site locally:

```bash
npm run serve
```

### Content Structure

- Create Markdown files (`.md`) in the `content` directory
- Each file must include front matter at the top:

```markdown
---
title: Page Title
---

# Your content here
```

### File Naming

- Files named `index.md` become `index.html` in their respective directories
- Other files (e.g., `about.md`) become directories with an `index.html` file inside (e.g., `/about/index.html`)

## Project Structure

```
.
├── content/        # Markdown content files
├── templates/      # HTML templates
├── static/         # Static assets (CSS, images, etc.)
├── public/         # Output directory (generated site)
├── main.js         # Main generator script
└── package.json    # Project configuration
```

## Customization

### Templates

Edit the template files in the `templates` directory to customize the HTML structure.

Templates use a simple variable replacement system:

- `{{title}}` - Page title from front matter
- `{{content}}` - Rendered HTML content from the Markdown

### Styling

Edit the CSS files in the `static/css` directory to customize the appearance of your site.
