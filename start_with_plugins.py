#!/usr/bin/env python3
"""
Phishy AI + Ngrok + Email Plugins Deployment Script
Comprehensive deployment solution for easy testing and development
"""
import subprocess
import asyncio
import logging
import time
import signal
import sys
import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any
import argparse
from datetime import datetime

# Add backend to path for imports
sys.path.append(str(Path(__file__).parent / "backend"))

try:
    from ngrok_manager import NgrokManager, update_phishy_tunnel_config
except ImportError:
    print("❌ Error: Could not import ngrok_manager. Make sure backend directory is accessible.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('phishy_deployment.log')
    ]
)
logger = logging.getLogger(__name__)

class PhishyDeployment:
    """Main deployment coordinator for Phishy AI + Ngrok + Plugins"""
    
    def __init__(self, 
                 port: int = 8080,
                 subdomain: Optional[str] = None,
                 auth_token: Optional[str] = None,
                 auto_restart: bool = True):
        self.port = port
        self.subdomain = subdomain
        self.auth_token = auth_token
        self.auto_restart = auto_restart
        
        # Process management
        self.phishy_process = None
        self.ngrok_manager = None
        self.running = False
        
        # Status tracking
        self.deployment_status = {
            "phishy_backend": "stopped",
            "ngrok_tunnel": "stopped",
            "last_updated": None
        }
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        sys.exit(0)
    
    async def start_deployment(self):
        """Start complete deployment"""
        try:
            logger.info("🚀 Starting Phishy AI + Ngrok deployment...")
            
            # Update status
            self.running = True
            self._update_status()
            
            # Step 1: Start Phishy backend
            logger.info("1️⃣ Starting Phishy backend...")
            if not await self._start_phishy_backend():
                raise Exception("Failed to start Phishy backend")
            
            # Step 2: Initialize ngrok manager
            logger.info("2️⃣ Initializing ngrok tunnel...")
            self.ngrok_manager = NgrokManager(
                port=self.port,
                subdomain=self.subdomain,
                auth_token=self.auth_token
            )
            
            # Step 3: Start ngrok tunnel
            if not self.ngrok_manager.start_tunnel():
                raise Exception("Failed to start ngrok tunnel")
            
            # Step 4: Update Phishy configuration with tunnel URL
            logger.info("3️⃣ Configuring Phishy with tunnel URL...")
            await update_phishy_tunnel_config(self.ngrok_manager.public_url)
            
            # Step 5: Wait for backend to load email flagging routes
            await self._wait_for_backend_ready()
            
            # Step 6: Register initial tunnel status
            await self._register_tunnel_with_backend()
            
            # Step 7: Display deployment information
            self._display_deployment_info()
            
            # Step 8: Start monitoring
            if self.auto_restart:
                logger.info("4️⃣ Starting auto-restart monitoring...")
                await self._monitor_services()
            else:
                logger.info("✅ Deployment complete. Press Ctrl+C to stop.")
                await self._wait_for_shutdown()
            
        except Exception as e:
            logger.error(f"❌ Deployment failed: {e}")
            self.shutdown()
            raise
    
    async def _start_phishy_backend(self) -> bool:
        """Start the Phishy backend server"""
        try:
            # Change to backend directory
            backend_dir = Path(__file__).parent / "backend"
            
            # Start backend process
            self.phishy_process = subprocess.Popen(
                [sys.executable, "app.py"],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for backend to start
            max_retries = 30
            for i in range(max_retries):
                try:
                    response = requests.get(f"http://localhost:{self.port}/health", timeout=2)
                    if response.status_code == 200:
                        logger.info(f"✅ Phishy backend started on port {self.port}")
                        self.deployment_status["phishy_backend"] = "running"
                        return True
                except:
                    pass
                
                await asyncio.sleep(1)
            
            logger.error("❌ Phishy backend failed to start within timeout")
            return False
            
        except Exception as e:
            logger.error(f"Error starting Phishy backend: {e}")
            return False
    
    async def _wait_for_backend_ready(self):
        """Wait for backend to fully load all routes including email flagging"""
        max_retries = 20
        for i in range(max_retries):
            try:
                response = requests.get(f"http://localhost:{self.port}/email-flagging/health", timeout=2)
                if response.status_code == 200:
                    logger.info("✅ Email flagging routes loaded")
                    return
            except:
                pass
            
            await asyncio.sleep(1)
        
        logger.warning("⚠️ Email flagging routes may not be fully loaded")
    
    async def _register_tunnel_with_backend(self):
        """Register tunnel URL with backend"""
        try:
            if not self.ngrok_manager or not self.ngrok_manager.public_url:
                return
            
            response = requests.post(
                f"http://localhost:{self.port}/email-flagging/tunnel/update",
                params={
                    "tunnel_url": self.ngrok_manager.public_url,
                    "public_url": self.ngrok_manager.public_url
                },
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Tunnel registered with backend")
                self.deployment_status["ngrok_tunnel"] = "active"
            else:
                logger.warning(f"⚠️ Failed to register tunnel with backend: {response.status_code}")
            
        except Exception as e:
            logger.error(f"Error registering tunnel with backend: {e}")
    
    def _display_deployment_info(self):
        """Display deployment information and setup instructions"""
        if not self.ngrok_manager or not self.ngrok_manager.public_url:
            return
        
        tunnel_url = self.ngrok_manager.public_url
        endpoints = self.ngrok_manager.get_api_endpoints()
        
        print("\n" + "="*60)
        print("🎉 PHISHY AI + NGROK DEPLOYMENT SUCCESSFUL!")
        print("="*60)
        print(f"📍 Public URL: {tunnel_url}")
        print(f"🖥️  Local URL:  http://localhost:{self.port}")
        print(f"📱 Admin UI:   {tunnel_url}")
        print("\n📧 EMAIL PLUGIN ENDPOINTS:")
        print(f"   • Flag Email:  {endpoints['flag_email']}")
        print(f"   • WebSocket:   {endpoints['websocket']}")
        print(f"   • Health:      {endpoints['health']}")
        print(f"   • Setup:       {endpoints['setup']}")
        print("\n🔧 PLUGIN SETUP URLS:")
        for plugin_type in ['outlook', 'gmail', 'thunderbird']:
            print(f"   • {plugin_type.title()}: {tunnel_url}/email-flagging/plugins/setup/{plugin_type}")
        
        print("\n📋 QUICK SETUP:")
        print("1. Open admin dashboard in browser:")
        print(f"   {tunnel_url}")
        print("2. Navigate to 'Email Plugins' section")
        print("3. Choose your email client and follow setup instructions")
        print("4. Use QR code for easy mobile configuration")
        
        print("\n🔍 TESTING:")
        print(f"   curl {endpoints['health']}")
        
        print("\n⚠️  IMPORTANT:")
        print("   • Keep this terminal open to maintain tunnel")
        print("   • Tunnel URL will change if ngrok restarts")
        print("   • Free ngrok tunnels have connection limits")
        print("   • Use Ctrl+C to shutdown gracefully")
        print("="*60 + "\n")
    
    async def _monitor_services(self):
        """Monitor services and auto-restart if needed"""
        logger.info("🔄 Starting service monitoring...")
        
        while self.running:
            try:
                # Check Phishy backend
                backend_healthy = await self._check_backend_health()
                
                # Check ngrok tunnel
                tunnel_healthy = self.ngrok_manager.monitor_tunnel() if self.ngrok_manager else False
                
                # Update status
                self.deployment_status.update({
                    "phishy_backend": "running" if backend_healthy else "error",
                    "ngrok_tunnel": "active" if tunnel_healthy else "error",
                    "last_updated": datetime.now().isoformat()
                })
                
                # Auto-restart if needed
                if not backend_healthy:
                    logger.warning("⚠️ Backend unhealthy, attempting restart...")
                    await self._restart_backend()
                
                if not tunnel_healthy and self.ngrok_manager:
                    logger.warning("⚠️ Tunnel unhealthy, attempting restart...")
                    await self.ngrok_manager.auto_restart_on_failure()
                    if self.ngrok_manager.public_url:
                        await update_phishy_tunnel_config(self.ngrok_manager.public_url)
                        await self._register_tunnel_with_backend()
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(10)
    
    async def _check_backend_health(self) -> bool:
        """Check if backend is healthy"""
        try:
            response = requests.get(f"http://localhost:{self.port}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    async def _restart_backend(self):
        """Restart the backend process"""
        try:
            if self.phishy_process:
                self.phishy_process.terminate()
                try:
                    self.phishy_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.phishy_process.kill()
            
            await asyncio.sleep(2)
            await self._start_phishy_backend()
            await self._wait_for_backend_ready()
            
        except Exception as e:
            logger.error(f"Error restarting backend: {e}")
    
    async def _wait_for_shutdown(self):
        """Wait for shutdown signal"""
        while self.running:
            await asyncio.sleep(1)
    
    def _update_status(self):
        """Update deployment status"""
        self.deployment_status["last_updated"] = datetime.now().isoformat()
        
        # Save status to file
        try:
            status_file = Path("data") / "deployment_status.json"
            status_file.parent.mkdir(exist_ok=True)
            
            with open(status_file, 'w') as f:
                json.dump(self.deployment_status, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving deployment status: {e}")
    
    def shutdown(self):
        """Shutdown all services"""
        logger.info("🛑 Shutting down deployment...")
        
        self.running = False
        
        # Stop ngrok tunnel
        if self.ngrok_manager:
            self.ngrok_manager.stop_tunnel()
            logger.info("✅ Ngrok tunnel stopped")
        
        # Stop Phishy backend
        if self.phishy_process:
            self.phishy_process.terminate()
            try:
                self.phishy_process.wait(timeout=10)
                logger.info("✅ Phishy backend stopped")
            except subprocess.TimeoutExpired:
                self.phishy_process.kill()
                logger.info("✅ Phishy backend killed")
        
        # Update status
        self.deployment_status.update({
            "phishy_backend": "stopped",
            "ngrok_tunnel": "stopped"
        })
        self._update_status()
        
        logger.info("✅ Shutdown complete")

def create_quick_start_script():
    """Create quick start scripts for different platforms"""
    
    # Windows batch script
    windows_script = """@echo off
echo ====================================
echo   Phishy AI + Ngrok Quick Start
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if ngrok is installed
ngrok version >nul 2>&1
if errorlevel 1 (
    echo ERROR: ngrok is not installed or not in PATH
    echo Please install ngrok and try again
    echo Visit: https://ngrok.com/download
    pause
    exit /b 1
)

echo Starting Phishy AI with ngrok...
python start_with_plugins.py --auto-restart

pause
"""
    
    # Linux/Mac shell script
    unix_script = """#!/bin/bash
echo "===================================="
echo "  Phishy AI + Ngrok Quick Start"
echo "===================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "ERROR: ngrok is not installed"
    echo "Please install ngrok and try again"
    echo "Visit: https://ngrok.com/download"
    exit 1
fi

echo "Starting Phishy AI with ngrok..."
python3 start_with_plugins.py --auto-restart
"""
    
    # Write scripts
    Path("quick_start.bat").write_text(windows_script)
    Path("quick_start.sh").write_text(unix_script)
    
    # Make shell script executable
    try:
        os.chmod("quick_start.sh", 0o755)
    except:
        pass
    
    logger.info("✅ Quick start scripts created")

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Phishy AI + Ngrok + Email Plugins Deployment")
    parser.add_argument("--port", type=int, default=8080, help="Backend port (default: 8080)")
    parser.add_argument("--subdomain", type=str, help="Ngrok subdomain (requires auth token)")
    parser.add_argument("--auth-token", type=str, help="Ngrok auth token")
    parser.add_argument("--auto-restart", action="store_true", default=True, help="Enable auto-restart monitoring")
    parser.add_argument("--no-auto-restart", action="store_false", dest="auto_restart", help="Disable auto-restart")
    parser.add_argument("--create-scripts", action="store_true", help="Create quick start scripts and exit")
    
    args = parser.parse_args()
    
    if args.create_scripts:
        create_quick_start_script()
        print("✅ Quick start scripts created!")
        print("   • Windows: quick_start.bat")
        print("   • Linux/Mac: quick_start.sh")
        return
    
    # Validate requirements
    try:
        import requests
        import qrcode
        import psutil
    except ImportError as e:
        print(f"❌ Missing required dependency: {e}")
        print("Install with: pip install requests qrcode[pil] psutil")
        sys.exit(1)
    
    # Create deployment instance
    deployment = PhishyDeployment(
        port=args.port,
        subdomain=args.subdomain,
        auth_token=args.auth_token,
        auto_restart=args.auto_restart
    )
    
    try:
        await deployment.start_deployment()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Deployment error: {e}")
        sys.exit(1)
    finally:
        deployment.shutdown()

if __name__ == "__main__":
    asyncio.run(main())