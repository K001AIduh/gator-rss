#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const marked = require('marked');

// Create directories if they don't exist
const directories = ['content', 'templates', 'static', 'public'];
directories.forEach((dir) => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

// Clear the public directory
const publicFiles = fs.readdirSync('public');
publicFiles.forEach((file) => {
  const filePath = path.join('public', file);
  if (fs.lstatSync(filePath).isDirectory()) {
    fs.rmSync(filePath, { recursive: true, force: true });
  } else {
    fs.unlinkSync(filePath);
  }
});

// Copy static files to public directory
if (fs.existsSync('static')) {
  const copyStaticFiles = (source, destination) => {
    if (!fs.existsSync(destination)) {
      fs.mkdirSync(destination, { recursive: true });
    }

    const files = fs.readdirSync(source);
    files.forEach((file) => {
      const sourcePath = path.join(source, file);
      const destPath = path.join(destination, file);

      if (fs.lstatSync(sourcePath).isDirectory()) {
        copyStaticFiles(sourcePath, destPath);
      } else {
        fs.copyFileSync(sourcePath, destPath);
      }
    });
  };

  copyStaticFiles('static', 'public');
}

// Read template
let template = '';
if (fs.existsSync(path.join('templates', 'default.html'))) {
  template = fs.readFileSync(path.join('templates', 'default.html'), 'utf8');
} else {
  template = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{title}}</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <header>
    <h1>{{title}}</h1>
  </header>
  <main>
    {{content}}
  </main>
  <footer>
    <p>Built with a simple static site generator</p>
  </footer>
</body>
</html>`;
  fs.mkdirSync('templates', { recursive: true });
  fs.writeFileSync(path.join('templates', 'default.html'), template);
}

// Process markdown files
const processMarkdownFile = (filePath) => {
  const fileContent = fs.readFileSync(filePath, 'utf8');

  // Extract front matter if present (basic implementation)
  let frontMatter = {};
  let markdown = fileContent;

  if (fileContent.startsWith('---')) {
    const endOfFrontMatter = fileContent.indexOf('---', 3);
    if (endOfFrontMatter !== -1) {
      const frontMatterText = fileContent.substring(3, endOfFrontMatter).trim();
      frontMatterText.split('\n').forEach((line) => {
        const [key, value] = line.split(':').map((part) => part.trim());
        if (key && value) {
          frontMatter[key] = value;
        }
      });
      markdown = fileContent.substring(endOfFrontMatter + 3).trim();
    }
  }

  // Convert markdown to HTML
  const content = marked.parse(markdown);

  // Replace template variables
  let html = template;
  html = html.replace('{{title}}', frontMatter.title || 'Untitled');
  html = html.replace('{{title}}', frontMatter.title || 'Untitled'); // Replace title in both places
  html = html.replace('{{content}}', content);

  return {
    frontMatter,
    html,
  };
};

const processDirectory = (sourceDir, targetDir) => {
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  const files = fs.readdirSync(sourceDir);

  files.forEach((file) => {
    const sourcePath = path.join(sourceDir, file);

    if (fs.lstatSync(sourcePath).isDirectory()) {
      const newTargetDir = path.join(targetDir, file);
      processDirectory(sourcePath, newTargetDir);
    } else if (file.endsWith('.md')) {
      const { html } = processMarkdownFile(sourcePath);
      const fileNameWithoutExt = file.replace('.md', '');
      let outputPath;

      if (fileNameWithoutExt === 'index') {
        outputPath = path.join(targetDir, 'index.html');
      } else {
        const newDir = path.join(targetDir, fileNameWithoutExt);
        if (!fs.existsSync(newDir)) {
          fs.mkdirSync(newDir, { recursive: true });
        }
        outputPath = path.join(newDir, 'index.html');
      }

      fs.writeFileSync(outputPath, html);
    }
  });
};

// Process content directory
if (fs.existsSync('content')) {
  processDirectory('content', 'public');
} else {
  // Create example content if content directory is empty
  const exampleContent = `---
title: Welcome to My Static Site
---

# Welcome to My Static Site

This is a simple static site generated with a custom-built static site generator.

## Features

- Markdown support
- HTML templates
- Static file copying

Feel free to edit this content in the \`content\` directory.
`;

  fs.mkdirSync('content', { recursive: true });
  fs.writeFileSync(path.join('content', 'index.md'), exampleContent);
  processDirectory('content', 'public');
}

// Create a basic CSS file if it doesn't exist
const cssDir = path.join('public', 'css');
if (!fs.existsSync(cssDir)) {
  fs.mkdirSync(cssDir, { recursive: true });
}

const cssPath = path.join(cssDir, 'style.css');
if (!fs.existsSync(cssPath)) {
  const css = `body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

header, footer {
  text-align: center;
  margin: 2rem 0;
  padding: 1rem;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

h1, h2, h3 {
  color: #222;
}

a {
  color: #0077cc;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code {
  background-color: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
}

pre {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 3px;
  overflow-x: auto;
}
`;
  fs.writeFileSync(cssPath, css);
}

console.log('Static site generated successfully in the public directory!');
