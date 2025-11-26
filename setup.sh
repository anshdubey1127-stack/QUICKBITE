#!/bin/bash
# QuickBite Setup Script
# Run this script to set up MongoDB and start the server
# Usage: bash setup.sh

set -e

echo "🚀 QuickBite MongoDB Setup Script"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check if Node.js is installed
echo -e "${BLUE}Step 1: Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Node.js not found. Please install Node.js from https://nodejs.org${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js $(node -v) found${NC}"

# Step 2: Check if MongoDB is installed
echo -e "\n${BLUE}Step 2: Checking MongoDB...${NC}"
if ! command -v mongod &> /dev/null; then
    echo -e "${YELLOW}MongoDB not found. Installing MongoDB Community Edition...${NC}"
    if command -v brew &> /dev/null; then
        brew tap mongodb/brew
        brew install mongodb-community
        echo -e "${GREEN}✓ MongoDB installed${NC}"
    else
        echo -e "${YELLOW}Please install MongoDB from https://www.mongodb.com/try/download/community${NC}"
    fi
fi

# Step 3: Install npm dependencies
echo -e "\n${BLUE}Step 3: Installing npm dependencies...${NC}"
if [ ! -d "node_modules" ]; then
    npm install
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

# Step 4: Check MongoDB is running
echo -e "\n${BLUE}Step 4: Starting MongoDB...${NC}"
if ! pgrep -x "mongod" > /dev/null; then
    echo "Starting MongoDB service..."
    if command -v brew &> /dev/null; then
        brew services start mongodb-community 2>/dev/null || true
    fi
    sleep 2
fi

if pgrep -x "mongod" > /dev/null; then
    echo -e "${GREEN}✓ MongoDB is running${NC}"
else
    echo -e "${YELLOW}⚠ MongoDB may not be running. Try: brew services start mongodb-community${NC}"
fi

# Step 5: Seed database (optional)
echo -e "\n${BLUE}Step 5: Database setup${NC}"
echo "Do you want to seed initial data? (y/n)"
read -r SEED_DB
if [ "$SEED_DB" = "y" ] || [ "$SEED_DB" = "Y" ]; then
    echo "Seeding database..."
    node seed.js
    echo -e "${GREEN}✓ Database seeded${NC}"
else
    echo -e "${GREEN}✓ Skipping database seed${NC}"
fi

# Step 6: Start the server
echo -e "\n${BLUE}Step 6: Starting QuickBite Server...${NC}"
echo -e "${GREEN}✓ Server starting on http://localhost:5000${NC}"
echo -e "${GREEN}✓ API Health Check: http://localhost:5000/api/health${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop the server${NC}\n"

npm run dev
