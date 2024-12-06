from .tracker import SystemTracker

# Initialize tracker when package is imported
_tracker = SystemTracker()

# Export any other functionality you want to provide
__version__ = "20.1.0"