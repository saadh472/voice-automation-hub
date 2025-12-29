@echo off
echo ========================================
echo   PUSH TO GITHUB
echo ========================================
echo.
echo IMPORTANT: You need to create the repository on GitHub first!
echo.
echo 1. Go to: https://github.com/new
echo 2. Repository name: voice-automation-hub
echo 3. Choose Public or Private
echo 4. DO NOT check "Initialize with README"
echo 5. Click "Create repository"
echo.
echo ========================================
echo.
echo Also, you need a Personal Access Token:
echo.
echo 1. Go to: https://github.com/settings/tokens
echo 2. Click "Generate new token (classic)"
echo 3. Check "repo" scope
echo 4. Generate and copy the token
echo.
echo ========================================
echo.
pause
echo.
echo Pushing to GitHub...
echo When prompted:
echo   Username: saadh472
echo   Password: Paste your Personal Access Token
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   SUCCESS! 
    echo ========================================
    echo.
    echo Your repository is now live at:
    echo https://github.com/saadh472/voice-automation-hub
    echo.
) else (
    echo.
    echo ========================================
    echo   ERROR
    echo ========================================
    echo.
    echo Please check:
    echo 1. Repository created on GitHub
    echo 2. Personal Access Token is correct
    echo 3. Token has "repo" scope
    echo.
    echo See GITHUB_SETUP.md for detailed instructions
    echo.
)
pause

