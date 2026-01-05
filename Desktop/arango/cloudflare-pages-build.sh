#!/bin/bash
# Cloudflare Pages build script
# This script is automatically run by Cloudflare Pages during deployment

cd frontend
npm install
npm run build

