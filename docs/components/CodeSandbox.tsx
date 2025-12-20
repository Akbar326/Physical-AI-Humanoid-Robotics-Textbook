import React, { useState } from 'react';
import clsx from 'clsx';

interface CodeSandboxProps {
  language: string;
  code: string;
  title?: string;
  description?: string;
  showLineNumbers?: boolean;
}

/**
 * CodeSandbox Component
 * Provides an interactive code example with copy/download functionality
 */
const CodeSandbox: React.FC<CodeSandboxProps> = ({
  language,
  code,
  title,
  description,
  showLineNumbers = false
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `code-example.${getFileExtension(language)}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getFileExtension = (lang: string): string => {
    const extensions: Record<string, string> = {
      python: 'py',
      bash: 'sh',
      javascript: 'js',
      typescript: 'ts',
      yaml: 'yaml',
      json: 'json',
      xml: 'xml',
      cpp: 'cpp',
      c: 'c',
      'c++': 'cpp',
      'c#': 'cs',
      java: 'java',
      html: 'html',
      css: 'css',
    };
    return extensions[lang.toLowerCase()] || 'txt';
  };

  const codeClasses = clsx(
    'code-sandbox',
    'margin-bottom--md',
    'border-radius--md',
    'code-block'
  );

  return (
    <div className={codeClasses}>
      {title && (
        <div className="code-sandbox__header padding--sm">
          <h5 className="code-sandbox__title margin-bottom--none">{title}</h5>
          {description && (
            <p className="code-sandbox__description margin-bottom--none text--small">
              {description}
            </p>
          )}
        </div>
      )}
      <div className="code-sandbox__body">
        <pre className={`language-${language}`}>
          <code className={showLineNumbers ? 'code-block-lines' : ''}>
            {code}
          </code>
        </pre>
      </div>
      <div className="code-sandbox__footer padding--sm button-group button-group--block">
        <button
          className="button button--sm button--outline button--primary"
          onClick={handleCopy}
        >
          {copied ? '✓ Copied!' : 'Copy Code'}
        </button>
        <button
          className="button button--sm button--outline button--secondary"
          onClick={handleDownload}
        >
          Download
        </button>
      </div>
    </div>
  );
};

export default CodeSandbox;