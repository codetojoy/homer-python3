#!/bin/bash

# Homer Enhanced Installation Script
# This script generates your homepage and optionally sets it as your browser homepage

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_NAME="homer.py"
LINKS_FILE="links.txt"
OUTPUT_FILE="index.html"
BACKUP_DIR="$HOME/.homer_backups"

# Functions
print_header() {
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${NC}                    ${CYAN}🏠 Homer Enhanced Setup${NC}                    ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo
}

print_step() {
    echo -e "${BLUE}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${CYAN}ℹ️${NC}  $1"
}

check_python() {
    print_step "Checking Python installation..."
    
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Found $PYTHON_VERSION"
        return 0
    else
        print_error "Python 3 is required but not found!"
        print_info "Please install Python 3: https://python.org/downloads/"
        return 1
    fi
}

check_links_file() {
    print_step "Checking for links file..."
    
    if [[ -f "$LINKS_FILE" ]]; then
        print_success "Found $LINKS_FILE"
        return 0
    else
        print_warning "$LINKS_FILE not found. Creating example file..."
        create_example_links_file
        return 0
    fi
}

create_example_links_file() {
    cat > "$LINKS_FILE" << 'EOF'
# Homer Enhanced Links File
# Format: Group names on their own line, followed by links
# Links format: Name, URL, Optional Description

🚀 Quick Start
Google, https://google.com, Search the web
GitHub, https://github.com, Code repositories
Stack Overflow, https://stackoverflow.com, Programming Q&A

📧 Communication
Gmail, https://gmail.com, Email service
Slack, https://slack.com, Team communication
Discord, https://discord.com, Chat and communities

🔧 Development Tools  
VS Code, https://code.visualstudio.com, Code editor
Docker Hub, https://hub.docker.com, Container registry
NPM, https://npmjs.com, Node package manager

📰 News & Information
Hacker News, https://news.ycombinator.com, Tech news
Reddit, https://reddit.com, Social news
BBC News, https://bbc.com/news, World news

🎵 Entertainment
YouTube, https://youtube.com, Video platform
Spotify, https://spotify.com, Music streaming
Netflix, https://netflix.com, Movies and shows
EOF

    print_success "Created example $LINKS_FILE with sample links"
    print_info "Edit $LINKS_FILE to customize your links"
}

generate_homepage() {
    print_step "Generating homepage..."
    
    if [[ -f "$SCRIPT_NAME" ]]; then
        python3 "$SCRIPT_NAME" "$@"
        if [[ $? -eq 0 ]]; then
            print_success "Homepage generated successfully!"
            return 0
        else
            print_error "Failed to generate homepage"
            return 1
        fi
    else
        print_error "$SCRIPT_NAME not found!"
        return 1
    fi
}

get_homepage_path() {
    local current_dir=$(pwd)
    echo "file://$current_dir/$OUTPUT_FILE"
}

backup_browser_settings() {
    local browser=$1
    print_step "Creating backup of $browser settings..."
    
    mkdir -p "$BACKUP_DIR"
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    
    case $browser in
        "chrome")
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                local prefs_dir="$HOME/Library/Application Support/Google/Chrome/Default"
                if [[ -f "$prefs_dir/Preferences" ]]; then
                    cp "$prefs_dir/Preferences" "$BACKUP_DIR/chrome_preferences_$timestamp.json"
                    print_success "Chrome preferences backed up"
                fi
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                # Linux
                local prefs_dir="$HOME/.config/google-chrome/Default"
                if [[ -f "$prefs_dir/Preferences" ]]; then
                    cp "$prefs_dir/Preferences" "$BACKUP_DIR/chrome_preferences_$timestamp.json"
                    print_success "Chrome preferences backed up"
                fi
            fi
            ;;
        "firefox")
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                local ff_dir="$HOME/Library/Application Support/Firefox/Profiles"
                if [[ -d "$ff_dir" ]]; then
                    local profile_dir=$(find "$ff_dir" -name "*.default*" | head -n 1)
                    if [[ -f "$profile_dir/prefs.js" ]]; then
                        cp "$profile_dir/prefs.js" "$BACKUP_DIR/firefox_prefs_$timestamp.js"
                        print_success "Firefox preferences backed up"
                    fi
                fi
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                # Linux
                local ff_dir="$HOME/.mozilla/firefox"
                if [[ -d "$ff_dir" ]]; then
                    local profile_dir=$(find "$ff_dir" -name "*.default*" | head -n 1)
                    if [[ -f "$profile_dir/prefs.js" ]]; then
                        cp "$profile_dir/prefs.js" "$BACKUP_DIR/firefox_prefs_$timestamp.js"
                        print_success "Firefox preferences backed up"
                    fi
                fi
            fi
            ;;
        "brave")
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                local prefs_dir="$HOME/Library/Application Support/BraveSoftware/Brave-Browser/Default"
                if [[ -f "$prefs_dir/Preferences" ]]; then
                    cp "$prefs_dir/Preferences" "$BACKUP_DIR/brave_preferences_$timestamp.json"
                    print_success "Brave preferences backed up"
                fi
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                # Linux
                local prefs_dir="$HOME/.config/BraveSoftware/Brave-Browser/Default"
                if [[ -f "$prefs_dir/Preferences" ]]; then
                    cp "$prefs_dir/Preferences" "$BACKUP_DIR/brave_preferences_$timestamp.json"
                    print_success "Brave preferences backed up"
                fi
            fi
            ;;
    esac
}

set_chrome_homepage() {
    local homepage_url=$1
    print_step "Setting Chrome homepage..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        local prefs_file="$HOME/Library/Application Support/Google/Chrome/Default/Preferences"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        local prefs_file="$HOME/.config/google-chrome/Default/Preferences"
    else
        print_warning "Chrome homepage setting not supported on this OS"
        return 1
    fi
    
    if [[ -f "$prefs_file" ]]; then
        # Use Python to modify JSON safely
        python3 -c "
import json
import sys

prefs_file = '$prefs_file'
homepage_url = '$homepage_url'

try:
    with open(prefs_file, 'r') as f:
        prefs = json.load(f)
    
    # Set homepage settings
    if 'homepage' not in prefs:
        prefs['homepage'] = {}
    
    prefs['homepage']['is_new_tab_page'] = False
    prefs['homepage']['use_homepage'] = True
    prefs['homepage']['homepage_url'] = homepage_url
    
    # Set startup settings
    if 'session' not in prefs:
        prefs['session'] = {}
    
    prefs['session']['restore_on_startup'] = 4  # Open specific page
    prefs['session']['startup_urls'] = [homepage_url]
    
    with open(prefs_file, 'w') as f:
        json.dump(prefs, f, indent=2)
    
    print('✅ Chrome homepage set successfully')
except Exception as e:
    print(f'❌ Error setting Chrome homepage: {e}')
    sys.exit(1)
"
        if [[ $? -eq 0 ]]; then
            print_success "Chrome homepage configured"
            return 0
        fi
    else
        print_warning "Chrome preferences file not found"
        return 1
    fi
}

set_firefox_homepage() {
    local homepage_url=$1
    print_step "Setting Firefox homepage..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        local ff_dir="$HOME/Library/Application Support/Firefox/Profiles"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        local ff_dir="$HOME/.mozilla/firefox"
    else
        print_warning "Firefox homepage setting not supported on this OS"
        return 1
    fi
    
    if [[ -d "$ff_dir" ]]; then
        local profile_dir=$(find "$ff_dir" -name "*.default*" | head -n 1)
        local user_js="$profile_dir/user.js"
        
        if [[ -n "$profile_dir" ]]; then
            # Add or update homepage settings in user.js
            echo "// Homer Enhanced Homepage Settings - $(date)" >> "$user_js"
            echo "user_pref(\"browser.startup.homepage\", \"$homepage_url\");" >> "$user_js"
            echo "user_pref(\"browser.startup.page\", 1);" >> "$user_js"
            
            print_success "Firefox homepage configured"
            print_info "Restart Firefox for changes to take effect"
            return 0
        else
            print_warning "Firefox profile directory not found"
            return 1
        fi
    else
        print_warning "Firefox not found"
        return 1
    fi
}

set_brave_homepage() {
    local homepage_url=$1
    print_step "Setting Brave homepage..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        local prefs_file="$HOME/Library/Application Support/BraveSoftware/Brave-Browser/Default/Preferences"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        local prefs_file="$HOME/.config/BraveSoftware/Brave-Browser/Default/Preferences"
    else
        print_warning "Brave homepage setting not supported on this OS"
        return 1
    fi
    
    if [[ -f "$prefs_file" ]]; then
        # Use Python to modify JSON safely (same as Chrome)
        python3 -c "
import json
import sys

prefs_file = '$prefs_file'
homepage_url = '$homepage_url'

try:
    with open(prefs_file, 'r') as f:
        prefs = json.load(f)
    
    # Set homepage settings
    if 'homepage' not in prefs:
        prefs['homepage'] = {}
    
    prefs['homepage']['is_new_tab_page'] = False
    prefs['homepage']['use_homepage'] = True
    prefs['homepage']['homepage_url'] = homepage_url
    
    # Set startup settings
    if 'session' not in prefs:
        prefs['session'] = {}
    
    prefs['session']['restore_on_startup'] = 4  # Open specific page
    prefs['session']['startup_urls'] = [homepage_url]
    
    with open(prefs_file, 'w') as f:
        json.dump(prefs, f, indent=2)
    
    print('✅ Brave homepage set successfully')
except Exception as e:
    print(f'❌ Error setting Brave homepage: {e}')
    sys.exit(1)
"
        if [[ $? -eq 0 ]]; then
            print_success "Brave homepage configured"
            return 0
        fi
    else
        print_warning "Brave preferences file not found"
        return 1
    fi
}

open_in_browser() {
    local file_path=$1
    print_step "Opening homepage in browser..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$file_path"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open "$file_path" >/dev/null 2>&1 &
    else
        print_info "Please open $file_path in your browser"
    fi
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -t, --title TITLE       Set custom page title"
    echo "  -s, --subtitle SUBTITLE Set custom page subtitle"
    echo "  --theme THEME           Set theme (modern, classic, minimal)"
    echo "  --install-chrome        Set as Chrome homepage"
    echo "  --install-firefox       Set as Firefox homepage"
    echo "  --install-brave         Set as Brave homepage"
    echo "  --install-all           Set as homepage for all browsers"
    echo "  --no-backup            Don't backup browser settings"
    echo "  --open                 Open homepage in browser after generation"
    echo
    echo "Examples:"
    echo "  $0                                    # Basic generation"
    echo "  $0 --install-chrome --open           # Set as Chrome homepage and open"
    echo "  $0 -t \"Team Portal\" --install-all   # Custom title, set for all browsers"
}

# Main script
main() {
    print_header
    
    # Parse arguments
    local python_args=()
    local install_chrome=false
    local install_firefox=false
    local install_brave=false
    local no_backup=false
    local open_browser=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            --install-chrome)
                install_chrome=true
                shift
                ;;
            --install-firefox)
                install_firefox=true
                shift
                ;;
            --install-brave)
                install_brave=true
                shift
                ;;
            --install-all)
                install_chrome=true
                install_firefox=true
                install_brave=true
                shift
                ;;
            --no-backup)
                no_backup=true
                shift
                ;;
            --open)
                open_browser=true
                shift
                ;;
            -t|--title)
                python_args+=("$1" "$2")
                shift 2
                ;;
            -s|--subtitle)
                python_args+=("$1" "$2")
                shift 2
                ;;
            --theme)
                python_args+=("$1" "$2")
                shift 2
                ;;
            *)
                python_args+=("$1")
                shift
                ;;
        esac
    done
    
    # Check prerequisites
    check_python || exit 1
    check_links_file
    
    # Generate homepage
    if ! generate_homepage "${python_args[@]}"; then
        exit 1
    fi
    
    local homepage_url=$(get_homepage_path)
    
    # Install as browser homepage if requested
    if [[ "$install_chrome" == true || "$install_firefox" == true || "$install_brave" == true ]]; then
        echo
        print_step "Installing as browser homepage..."
        
        # Create backups unless disabled
        if [[ "$no_backup" != true ]]; then
            [[ "$install_chrome" == true ]] && backup_browser_settings "chrome"
            [[ "$install_firefox" == true ]] && backup_browser_settings "firefox"
            [[ "$install_brave" == true ]] && backup_browser_settings "brave"
        fi
        
        # Set homepage for each requested browser
        [[ "$install_chrome" == true ]] && set_chrome_homepage "$homepage_url"
        [[ "$install_firefox" == true ]] && set_firefox_homepage "$homepage_url"
        [[ "$install_brave" == true ]] && set_brave_homepage "$homepage_url"
        
        echo
        print_info "Browser settings have been updated"
        print_info "You may need to restart your browser for changes to take effect"
        
        if [[ "$no_backup" != true ]]; then
            print_info "Original settings backed up to: $BACKUP_DIR"
        fi
    fi
    
    # Open in browser if requested
    if [[ "$open_browser" == true ]]; then
        echo
        open_in_browser "$homepage_url"
        print_success "Opened homepage in browser"
    fi
    
    echo
    print_success "All done! 🎉"
    print_info "Your homepage: $homepage_url"
    print_info "Edit '$LINKS_FILE' and run this script again to update"
    echo
}

# Run main function with all arguments
main "$@"
