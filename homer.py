#!/usr/bin/env python3
"""
Homer Enhanced - A Beautiful Homepage Generator

This script parses a links.txt file and generates a beautiful, modern HTML homepage
with organized link groups. Perfect for personal use, team onboarding, or company
link portals.

Author: Enhanced by GitHub Copilot based on original by codetojoy
License: Apache-2.0
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Config:
    """Configuration class for Homer Enhanced with all file paths and settings."""
    
    input_file: str = 'links.txt'
    output_file: str = 'index.html'
    template_dir: str = 'templates'
    title: str = 'My Homepage'
    subtitle: str = 'Quick Access to Your Favorite Links'
    theme: str = 'modern'  # Options: modern, classic, minimal
    
    @property
    def main_template_file(self) -> str:
        return os.path.join(self.template_dir, f'{self.theme}_main.template.html')
    
    @property
    def homer_template_file(self) -> str:
        return os.path.join(self.template_dir, f'{self.theme}_homer.template.html')
    
    @property
    def link_group_template_file(self) -> str:
        return os.path.join(self.template_dir, f'{self.theme}_link_group.template.html')
    
    @property
    def link_template_file(self) -> str:
        return os.path.join(self.template_dir, f'{self.theme}_link.template.html')


class Token(NamedTuple):
    """Represents a template token and its replacement value."""
    token: str
    new_value: str


def stamp_template(template_file: str, tokens: List[Token]) -> str:
    """
    Process a template file by replacing tokens with their values.
    
    Args:
        template_file: Path to the template file
        tokens: List of Token objects containing replacements
        
    Returns:
        Processed template content as string
        
    Raises:
        FileNotFoundError: If template file doesn't exist
        IOError: If template file cannot be read
    """
    try:
        with open(template_file, 'r', encoding='utf-8') as file:
            content = file.read()

        for token in tokens:
            content = content.replace(token.token, token.new_value)
            
        return content

    except FileNotFoundError:
        print(f"Error: Template file '{template_file}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading template file '{template_file}': {e}")
        sys.exit(1)


class Link:
    """Represents a single link with name and URL."""
    
    def __init__(self, name: str, url: str, description: str = ""):
        """
        Initialize a Link object.
        
        Args:
            name: Display name for the link
            url: Target URL
            description: Optional description for the link
        """
        self.name = name.strip()
        self.url = url.strip()
        self.description = description.strip()
        
        # Add protocol if missing
        if self.url and not self.url.startswith(('http://', 'https://', 'ftp://', 'mailto:')):
            self.url = f'https://{self.url}'
    
    def to_string(self, config: Config) -> str:
        """
        Convert link to HTML using template.
        
        Args:
            config: Configuration object
            
        Returns:
            HTML representation of the link
        """
        template_file = config.link_template_file
        tokens = [
            Token("@URL", self.url),
            Token("@NAME", self.name),
            Token("@DESCRIPTION", self.description)
        ]
        return stamp_template(template_file, tokens)
    
    def __repr__(self) -> str:
        return f"Link(name='{self.name}', url='{self.url}')"


class LinkGroup:
    """Represents a group of related links."""
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize a LinkGroup object.
        
        Args:
            name: Display name for the group
            description: Optional description for the group
        """
        self.name = name.strip()
        self.description = description.strip()
        self.links: List[Link] = []
    
    def add_link(self, link: Link) -> None:
        """
        Add a link to this group.
        
        Args:
            link: Link object to add
        """
        self.links.append(link)
    
    def to_string(self, config: Config) -> str:
        """
        Convert link group to HTML using template.
        
        Args:
            config: Configuration object
            
        Returns:
            HTML representation of the link group
        """
        template_file = config.link_group_template_file
        
        links_content = ""
        for link in self.links:
            links_content += link.to_string(config)
        
        tokens = [
            Token("@NAME", self.name),
            Token("@DESCRIPTION", self.description),
            Token("@LINKS", links_content),
            Token("@LINK_COUNT", str(len(self.links)))
        ]
        return stamp_template(template_file, tokens)
    
    def __repr__(self) -> str:
        return f"LinkGroup(name='{self.name}', links={len(self.links)})"


class HomerModel:
    """Main model containing all link groups and metadata."""
    
    def __init__(self):
        """Initialize the Homer model."""
        self.current_link_group: Optional[LinkGroup] = None
        self.link_groups: List[LinkGroup] = []
        self.created_at = datetime.now()
    
    def add_link_group(self, name: str, description: str = "") -> None:
        """
        Add a new link group.
        
        Args:
            name: Name of the group
            description: Optional description
        """
        link_group = LinkGroup(name, description)
        self.link_groups.append(link_group)
        self.current_link_group = link_group
    
    def add_link(self, name: str, url: str, description: str = "") -> None:
        """
        Add a link to the current group.
        
        Args:
            name: Display name for the link
            url: Target URL
            description: Optional description
            
        Raises:
            ValueError: If no current link group exists
        """
        if self.current_link_group is None:
            raise ValueError("No link group available. Add a group first.")
        
        link = Link(name, url, description)
        self.current_link_group.add_link(link)
    
    def to_string(self, config: Config) -> str:
        """
        Convert the entire model to HTML.
        
        Args:
            config: Configuration object
            
        Returns:
            HTML representation of all link groups
        """
        template_file = config.homer_template_file
        
        link_groups_content = ''
        for link_group in self.link_groups:
            link_groups_content += link_group.to_string(config)
        
        total_links = sum(len(group.links) for group in self.link_groups)
        
        tokens = [
            Token("@LINK_GROUPS", link_groups_content),
            Token("@TOTAL_GROUPS", str(len(self.link_groups))),
            Token("@TOTAL_LINKS", str(total_links)),
            Token("@GENERATED_DATE", self.created_at.strftime("%B %d, %Y at %I:%M %p"))
        ]
        return stamp_template(template_file, tokens)
    
    def get_stats(self) -> dict:
        """
        Get statistics about the model.
        
        Returns:
            Dictionary with stats about groups and links
        """
        total_links = sum(len(group.links) for group in self.link_groups)
        return {
            'groups': len(self.link_groups),
            'total_links': total_links,
            'created_at': self.created_at.isoformat()
        }


class LinkParser:
    """Parses links.txt file and populates HomerModel."""
    
    def __init__(self, config: Config):
        """
        Initialize the parser.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.homer_model = HomerModel()
    
    def process_line(self, line: str, line_number: int = 0) -> None:
        """
        Process a single line from the links file.
        
        Args:
            line: Line content to process
            line_number: Line number for error reporting
        """
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            return
        
        # Parse the line
        parts = [part.strip() for part in line.split(',')]
        
        if len(parts) == 1:
            # This is a group header
            group_name = parts[0]
            self.homer_model.add_link_group(group_name)
            print(f"Added group: {group_name}")
            
        elif len(parts) >= 2:
            # This is a link (name, url, optional description)
            name = parts[0]
            url = parts[1]
            description = parts[2] if len(parts) > 2 else ""
            
            try:
                self.homer_model.add_link(name, url, description)
                print(f"  Added link: {name} -> {url}")
            except ValueError as e:
                print(f"Error on line {line_number}: {e}")
                
        else:
            print(f"Warning: Skipping malformed line {line_number}: {line}")
    
    def process_file(self, file_path: str) -> HomerModel:
        """
        Process the entire links file.
        
        Args:
            file_path: Path to the links file
            
        Returns:
            Populated HomerModel
            
        Raises:
            FileNotFoundError: If links file doesn't exist
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, 1):
                    self.process_line(line, line_number)
                    
        except FileNotFoundError:
            print(f"Error: Links file '{file_path}' not found.")
            print("Please create a links.txt file with your links.")
            sys.exit(1)
        except IOError as e:
            print(f"Error reading links file '{file_path}': {e}")
            sys.exit(1)
        
        return self.homer_model


def write_content(config: Config, homer_model: HomerModel) -> None:
    """
    Write the final HTML content to the output file.
    
    Args:
        config: Configuration object
        homer_model: Populated model with all data
    """
    main_template_file = config.main_template_file
    output_file = config.output_file
    
    # Get model stats for template
    stats = homer_model.get_stats()
    
    tokens = [
        Token("@HOMER_MODEL", homer_model.to_string(config)),
        Token("@TITLE", config.title),
        Token("@SUBTITLE", config.subtitle),
        Token("@TOTAL_GROUPS", str(stats['groups'])),
        Token("@TOTAL_LINKS", str(stats['total_links'])),
        Token("@GENERATED_DATE", datetime.now().strftime("%B %d, %Y at %I:%M %p"))
    ]
    
    content = stamp_template(main_template_file, tokens)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"\n✅ Successfully generated '{output_file}'")
        print(f"📊 Generated {stats['groups']} groups with {stats['total_links']} total links")
        
    except IOError as e:
        print(f"Error writing output file '{output_file}': {e}")
        sys.exit(1)


def setup_templates(config: Config) -> None:
    """
    Ensure template directory exists and create default templates if needed.
    
    Args:
        config: Configuration object
    """
    template_dir = Path(config.template_dir)
    template_dir.mkdir(exist_ok=True)
    print(f"📁 Template directory: {template_dir}")


def main():
    """Main function to orchestrate the homepage generation."""
    parser = argparse.ArgumentParser(
        description="Homer Enhanced - Generate beautiful HTML homepages from link lists",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 homer_enhanced.py                    # Use default settings
  python3 homer_enhanced.py -i my_links.txt   # Use custom input file
  python3 homer_enhanced.py -t "Team Portal"  # Custom title
  python3 homer_enhanced.py --theme minimal   # Use minimal theme
        """
    )
    
    parser.add_argument('-i', '--input', default='links.txt',
                      help='Input links file (default: links.txt)')
    parser.add_argument('-o', '--output', default='index.html',
                      help='Output HTML file (default: index.html)')
    parser.add_argument('-t', '--title', default='My Homepage',
                      help='Page title (default: "My Homepage")')
    parser.add_argument('-s', '--subtitle', default='Quick Access to Your Favorite Links',
                      help='Page subtitle')
    parser.add_argument('--theme', choices=['modern', 'classic', 'minimal'],
                      default='modern', help='Theme to use (default: modern)')
    parser.add_argument('--template-dir', default='templates',
                      help='Template directory (default: templates)')
    parser.add_argument('-v', '--verbose', action='store_true',
                      help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Create configuration
    config = Config(
        input_file=args.input,
        output_file=args.output,
        template_dir=args.template_dir,
        title=args.title,
        subtitle=args.subtitle,
        theme=args.theme
    )
    
    print("🏠 Homer Enhanced - Homepage Generator")
    print("=" * 50)
    print(f"📖 Input file: {config.input_file}")
    print(f"📄 Output file: {config.output_file}")
    print(f"🎨 Theme: {config.theme}")
    print(f"📁 Template directory: {config.template_dir}")
    print()
    
    # Setup templates
    setup_templates(config)
    
    # Parse links file
    print("📋 Processing links...")
    parser = LinkParser(config)
    homer_model = parser.process_file(config.input_file)
    
    # Generate HTML
    print("\n🎨 Generating HTML...")
    write_content(config, homer_model)
    
    print(f"\n🌐 Open {config.output_file} in your browser to view your homepage!")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
