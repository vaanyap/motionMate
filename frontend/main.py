import os
import sys
import importlib
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDesktopWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer, QFileSystemWatcher

class MotionMimicApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        print("🚀 Starting MotionMateApp...")
        
        self.init_ui()
        self.start_simple_watcher()
        
    def init_ui(self):
        """Initialize UI components"""
        print("🔄 Initializing UI...")
        
        # Clear existing widgets first
        while self.count() > 0:
            widget = self.widget(0)
            self.removeWidget(widget)
            widget.deleteLater()
        
        try:
            # Import and create pages - make sure these imports are correct
            from pages.home import HomePage
            from pages.game_page import GamePage
            from pages.configuration_page import ConfigurationPage  # Make sure this matches your file name

            self.home_page = HomePage(self)
            self.game_page = GamePage(self)
            self.configuration_page = ConfigurationPage(self)


            # Add them in order and print debug info
            print(f"Adding HomePage at index: {self.count()}")
            self.addWidget(self.home_page)
            
            print(f"Adding ConfigurationPage at index: {self.count()}")
            self.addWidget(self.configuration_page)

            print(f"Adding GamePage at index: {self.count()}")
            self.addWidget(self.game_page)
            
            
            print(f"Total pages after loading: {self.count()}")

            # Get screen dimensions
            screen = QDesktopWidget().screenGeometry()
            screen_width = screen.width()
            screen_height = screen.height()
            
            # Set window to fullscreen or maximized
            self.showMaximized()
            
            # Load and apply background image
            self.apply_background(screen_width, screen_height)
            
            self.setWindowTitle("MotionMate")
            print("✅ UI initialized successfully!")
            
        except Exception as e:
            print(f"❌ UI initialization failed: {e}")
            import traceback
            traceback.print_exc()

    def start_simple_watcher(self):
        """Use QFileSystemWatcher (built into PyQt) - no threading issues!"""
        self.watcher = QFileSystemWatcher()
        self.last_reload_time = 0
        
        # Add all Python files to watch
        python_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py') and '__pycache__' not in root:
                    full_path = os.path.abspath(os.path.join(root, file))
                    python_files.append(full_path)
        
        if python_files:
            self.watcher.addPaths(python_files)
            self.watcher.fileChanged.connect(self.on_file_changed)
            print(f"✅ Watching {len(python_files)} files for changes")
            print("💡 Modify any .py file and save to see auto-reload!")
        else:
            print("❌ No Python files found to watch")

    def on_file_changed(self, file_path):
        """Handle file changes - this runs in the main thread"""
        import time
        current_time = time.time()
        
        # Debounce - prevent multiple rapid reloads
        if current_time - self.last_reload_time < 2:
            return
            
        self.last_reload_time = current_time
        
        if file_path.endswith('.py') and '__pycache__' not in file_path:
            print(f"🔄 Change detected: {os.path.basename(file_path)}")
            # Use singleShot to reload after a short delay
            QTimer.singleShot(500, self.hot_reload)

    def apply_background(self, width, height):
        """Apply background image scaled to the given dimensions"""
        img_path = os.path.join(os.path.dirname(__file__), 'background.png')
        images_path = os.path.join(os.path.dirname(__file__), 'images', 'background.png')
        
        if os.path.exists(images_path):
            img_path = images_path
        
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print(f"⚠️  Could not load background image at {img_path}")
            print(f"📁 File exists: {os.path.exists(img_path)}")
            # Fallback to a solid color if image not found
            self.setStyleSheet("QStackedWidget { background-color: #2C3E50; }")
            return
        
        # Scale the image to fit the screen while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        
        # Apply via palette for better control
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def hot_reload(self):
        """Hot reload the application"""
        try:
            print("🔥 Hot reloading application...")
            
            # Clear current widgets
            while self.count() > 0:
                widget = self.widget(0)
                self.removeWidget(widget)
                widget.deleteLater()
            
            # Force Python to reload modules by clearing them from sys.modules
            modules_to_clear = []
            for module_name in list(sys.modules.keys()):
                if module_name.startswith('pages'):
                    modules_to_clear.append(module_name)
            
            for module_name in modules_to_clear:
                del sys.modules[module_name]
            
            print(f"🧹 Cleared {len(modules_to_clear)} modules from cache")
            
            # Re-import and reload
            from pages import home, game_page
            importlib.reload(home)
            importlib.reload(game_page)
            
            # Re-initialize UI
            self.init_ui()
            
            print("✅ Hot reload completed!")
            
        except Exception as e:
            print(f"❌ Hot reload failed: {e}")
            import traceback
            traceback.print_exc()

    def keyPressEvent(self, event):
        """Handle key presses for fullscreen toggle"""
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif event.key() == Qt.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
        elif event.key() == Qt.Key_R and event.modifiers() == Qt.ControlModifier:
            # Manual reload with Ctrl+R
            self.hot_reload()
        else:
            super().keyPressEvent(event)
            
    def closeEvent(self, event):
        """Cleanup on close"""
        print("🛑 Shutting down...")
        if hasattr(self, 'watcher'):
            self.watcher.fileChanged.disconnect()
        event.accept()

if __name__ == "__main__":
    print("🎬 Starting MotionMate with auto-reload...")
    app = QApplication([])
    window = MotionMimicApp()
    sys.exit(app.exec_())