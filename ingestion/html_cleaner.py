#!/usr/bin/env python3
"""HTML cleanup utilities for extracting valuable content from LangGraph documentation pages."""
from bs4 import BeautifulSoup, Tag, NavigableString
from typing import Optional
import re


class LangGraphHTMLCleaner:
    """Extracts and cleans valuable content from LangGraph HTML documentation pages."""
    
    # Selectors for elements to remove (Mintlify documentation structure)
    REMOVE_SELECTORS = [
        'nav',                    # Navigation
        'header',                 # Header with logo/search
        'footer',                 # Footer
        '.sidebar',               # Sidebar navigation
        '[class*="sidebar"]',     # Any sidebar elements
        '[id*="sidebar"]',       # Sidebar by ID
        '[class*="navigation"]',  # Navigation elements
        '[class*="header"]',      # Header elements
        '[id*="header"]',         # Header by ID (but keep header inside content)
        '[class*="footer"]',      # Footer elements
        '[id*="footer"]',         # Footer by ID
        '[class*="search"]',      # Search elements
        '[id*="search"]',         # Search by ID
        'script',                 # All scripts
        'style',                  # All styles
        '[class*="edit"]',        # Edit page links
        '[class*="feedback"]',    # Feedback sections
        '[class*="helpful"]',     # "Was this page helpful?" sections
        '[class*="social"]',      # Social media links
        '[class*="brand"]',       # Branding elements
        '[class*="logo"]',        # Logo elements
        'aside',                   # Sidebar/aside elements
        '[role="navigation"]',    # Navigation by role
        '[role="banner"]',        # Header by role
        '[role="contentinfo"]',   # Footer by role
        '[class*="skip"]',        # Skip links
        '[class*="mintlify"]',    # Mintlify-specific UI elements
        '[id="navbar"]',          # Navbar
        '[id="table-of-contents"]', # Table of contents
        '[id*="toc"]',            # TOC elements
        '[class*="breadcrumb"]',  # Breadcrumbs
        '[id="page-context-menu"]', # Page context menu
        '[id="content-side-layout"]', # Side layout (TOC sidebar)
        '[id="content-container"]',  # Container (but we want inner content)
    ]
    
    # Selectors for main content area (Mintlify/Next.js structure)
    CONTENT_SELECTORS = [
        '#content',                    # Primary content ID (docs.langchain.com)
        '#content-area',               # Alternative content area
        '[id="content"]',              # Explicit ID selector
        'main',                        # Main element
        '[role="main"]',               # Main by role
        'article',                     # Article element
        '[class*="mdx-content"]',      # MDX content (docs.langchain.com)
        '[class*="prose"]',            # Prose content
        '[class*="documentation"]',    # Documentation class
        '[class*="docs-content"]',     # Docs content class
    ]
    
    def __init__(self):
        """Initialize the HTML cleaner."""
        pass
    
    def clean_html(self, html_content: str, url: str = "") -> str:
        """
        Clean HTML content and extract valuable documentation content.
        
        Args:
            html_content: Raw HTML content
            url: Source URL (for debugging)
            
        Returns:
            Cleaned HTML string ready for markdown conversion
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find and extract main content FIRST (before removing elements)
        main_content = self._extract_main_content(soup)
        
        if main_content is None:
            # Fallback: try to find any article or main-like content
            main_content = soup.find('body')
            if main_content:
                # Remove unwanted elements from body, but preserve content area
                self._remove_unwanted_elements(main_content)
        
        if main_content is None:
            # Last resort: return cleaned body
            return self._clean_fallback(soup)
        
        # Clean up the main content (remove unwanted elements within content)
        self._clean_content(main_content)
        
        # Convert to string
        return str(main_content)
    
    def _remove_unwanted_elements(self, soup: BeautifulSoup | Tag):
        """Remove unwanted elements from the soup."""
        # Create a set of elements to remove (to avoid removing same element twice)
        elements_to_remove = set()
        
        for selector in self.REMOVE_SELECTORS:
            for element in soup.select(selector):
                # Don't remove if it's inside a content area we want to keep
                if element.find_parent('div', id='content'):
                    # Only remove if it's a header/breadcrumb/etc inside content
                    if element.name in ['header', 'nav'] or 'breadcrumb' in str(element.get('class', [])).lower():
                        elements_to_remove.add(element)
                else:
                    elements_to_remove.add(element)
        
        # Remove all collected elements
        for element in elements_to_remove:
            element.decompose()
    
    def _extract_main_content(self, soup: BeautifulSoup) -> Optional[Tag]:
        """Extract the main content area from the HTML."""
        # Try each selector in order of preference
        for selector in self.CONTENT_SELECTORS:
            element = soup.select_one(selector)
            if element:
                # Verify it has actual content (not just empty div)
                text = element.get_text(strip=True)
                if len(text) > 50:  # Has substantial content
                    return element
        
        # Fallback: look for div with id="content" or class containing "content"
        content_div = soup.find('div', id='content')
        if content_div:
            text = content_div.get_text(strip=True)
            if len(text) > 50:
                return content_div
        
        return None
    
    def _clean_content(self, content: Tag):
        """Clean up content elements."""
        # Remove header elements within content (page title, breadcrumbs, etc.)
        header_in_content = content.find('header', id='header')
        if header_in_content:
            header_in_content.decompose()
        
        # Remove page context menus
        for menu in content.find_all(id='page-context-menu'):
            menu.decompose()
        
        # Remove breadcrumbs
        for breadcrumb in content.find_all(class_=lambda x: x and 'breadcrumb' in x.lower()):
            breadcrumb.decompose()
        
        # Remove empty elements
        for element in content.find_all():
            # Remove elements with only whitespace
            if isinstance(element, Tag):
                text = element.get_text(strip=True)
                if not text and not element.find_all(['pre', 'code', 'img']):
                    element.decompose()
                    continue
                
                # Clean up attributes (keep only essential ones)
                self._clean_attributes(element)
                
                # Fix relative URLs to absolute (if needed)
                self._fix_urls(element)
    
    def _clean_attributes(self, element: Tag):
        """Remove unnecessary attributes, keep only essential ones."""
        essential_attrs = ['href', 'src', 'alt', 'title', 'id', 'class']
        attrs_to_remove = []
        
        for attr in element.attrs:
            if attr not in essential_attrs:
                attrs_to_remove.append(attr)
            elif attr == 'class':
                # Keep class but clean it (remove UI-related classes)
                classes = element.get('class', [])
                if isinstance(classes, list):
                    # Remove UI-related classes
                    cleaned_classes = [
                        c for c in classes 
                        if not any(ui_term in c.lower() for ui_term in [
                            'mintlify', 'sidebar', 'nav', 'header', 'footer',
                            'search', 'brand', 'logo', 'social', 'edit', 'feedback'
                        ])
                    ]
                    if cleaned_classes:
                        element['class'] = cleaned_classes
                    else:
                        attrs_to_remove.append('class')
        
        for attr in attrs_to_remove:
            del element[attr]
    
    def _fix_urls(self, element: Tag):
        """Convert relative URLs to absolute if needed."""
        for tag_name, attr_name in [('a', 'href'), ('img', 'src'), ('link', 'href')]:
            for tag in element.find_all(tag_name):
                url = tag.get(attr_name)
                if url and url.startswith('/'):
                    # Keep relative URLs as-is for now
                    # They can be resolved later if needed
                    pass
    
    def _clean_fallback(self, soup: BeautifulSoup) -> str:
        """Fallback cleaning method when main content can't be found."""
        body = soup.find('body')
        if body:
            self._remove_unwanted_elements(body)
            self._clean_content(body)
            return str(body)
        return str(soup)
    
    def html_to_markdown(self, html_content: str, url: str = "") -> str:
        """
        Convert cleaned HTML to markdown.
        
        Args:
            html_content: Cleaned HTML content
            url: Source URL (for reference)
            
        Returns:
            Markdown string
        """
        try:
            import html2text
        except ImportError:
            raise ImportError(
                "html2text is required for HTML to markdown conversion. "
                "Install it with: pip install html2text"
            )
        
        # Clean HTML first
        cleaned_html = self.clean_html(html_content, url)
        
        # Configure html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        h.body_width = 0  # Don't wrap lines
        h.unicode_snob = True  # Use unicode
        h.skip_internal_links = False
        h.inline_links = True  # Use inline link format
        h.escape_snob = True  # Escape special characters
        
        # Convert to markdown
        markdown = h.handle(cleaned_html)
        
        # Post-process markdown
        markdown = self._post_process_markdown(markdown, url)
        
        return markdown
    
    def _post_process_markdown(self, markdown: str, url: str = "") -> str:
        """Post-process markdown to clean up common issues."""
        lines = markdown.split('\n')
        cleaned_lines = []
        skip_empty = False
        
        for line in lines:
            # Remove excessive empty lines (max 2 consecutive)
            if not line.strip():
                if skip_empty:
                    continue
                skip_empty = True
                cleaned_lines.append('')
            else:
                skip_empty = False
                # Clean up common artifacts
                line = re.sub(r'^\s*\[Skip to main content\]\([^\)]+\)\s*$', '', line)
                line = re.sub(r'^\s*Copy page\s*$', '', line)
                line = re.sub(r'^\s*Powered by Mintlify.*$', '', line)
                
                # Fix empty headings (e.g., "## " or "### ")
                line = re.sub(r'^#+\s+$', '', line)
                
                # Fix anchor-only lines (e.g., "[​](#core-components)")
                line = re.sub(r'^\s*\[​\]\(#[^\)]+\)\s*$', '', line)
                
                # Fix escaped parentheses in code (html2text sometimes over-escapes)
                # But keep them in regular text where they might be intentional
                # Only fix in code blocks context
                if line.strip() and not line.strip().startswith('```'):
                    # Unescape parentheses that are clearly in code context
                    line = re.sub(r'\\\(', '(', line)
                    line = re.sub(r'\\\)', ')', line)
                
                # Remove lines that are just anchor links
                if re.match(r'^\s*\[.*\]\(#.*\)\s*$', line):
                    continue
                
                if line.strip():  # Only add non-empty lines
                    cleaned_lines.append(line)
        
        # Join and clean up
        result = '\n'.join(cleaned_lines)
        
        # Remove leading/trailing whitespace
        result = result.strip()
        
        # Add source URL as comment at the top if provided
        if url:
            result = f"<!-- Source: {url} -->\n\n{result}"
        
        return result


def clean_langgraph_html(html_content: str, url: str = "") -> str:
    """
    Convenience function to clean LangGraph HTML and convert to markdown.
    
    Args:
        html_content: Raw HTML content
        url: Source URL (optional, for reference)
        
    Returns:
        Cleaned markdown string
    """
    cleaner = LangGraphHTMLCleaner()
    return cleaner.html_to_markdown(html_content, url)

