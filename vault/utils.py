import os
from datetime import datetime

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024
        i += 1
    
    return f"{size:.2f} {size_names[i]}"


def get_file_icon(filename):
    """Get emoji icon based on file extension"""
    ext = os.path.splitext(filename)[1].lower()
    
    icon_map = {
        '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.bmp': '🖼️', '.svg': '🖼️',
        '.pdf': '📄', '.doc': '📄', '.docx': '📄', '.txt': '📄', '.rtf': '📄',
        '.mp4': '🎬', '.avi': '🎬', '.mov': '🎬', '.mkv': '🎬', '.wmv': '🎬',
        '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵', '.aac': '🎵', '.ogg': '🎵',
        '.zip': '📦', '.rar': '📦', '.7z': '📦', '.tar': '📦', '.gz': '📦',
        '.xls': '📊', '.xlsx': '📊', '.csv': '📊',
        '.ppt': '📽️', '.pptx': '📽️',
        '.exe': '⚙️', '.msi': '⚙️',
        '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨', '.json': '📋',
    }
    
    return icon_map.get(ext, '📁')


def format_date(date_obj):
    """Format datetime object to readable string"""
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%b %d, %Y at %I:%M %p")
    return "Unknown date"

