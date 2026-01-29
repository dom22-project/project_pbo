#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Configuration from .env
"""

from config import Config

print("\n" + "="*70)
print("📋 Configuration Loaded from .env")
print("="*70)

print("\n🔐 MySQL Database Settings:")
print(f"   Host: {Config.MYSQL_HOST}")
print(f"   Port: {Config.MYSQL_PORT}")
print(f"   User: {Config.MYSQL_USER}")
print(f"   Password: {'(empty)' if not Config.MYSQL_PASSWORD else '***'}")
print(f"   Database: {Config.MYSQL_DATABASE}")

print(f"\n🌐 Connection URI:")
print(f"   {Config.SQLALCHEMY_DATABASE_URI}")

print(f"\n⚙️  Pool Settings:")
print(f"   Pool Size: {Config.SQLALCHEMY_ENGINE_OPTIONS['pool_size']}")
print(f"   Pool Recycle: {Config.SQLALCHEMY_ENGINE_OPTIONS['pool_recycle']} seconds")
print(f"   Connect Timeout: {Config.SQLALCHEMY_ENGINE_OPTIONS['connect_args']['connect_timeout']} seconds")

print(f"\n📊 Application Settings:")
print(f"   Batch Size: {Config.BATCH_SIZE}")
print(f"   Import Timeout: {Config.IMPORT_TIMEOUT} seconds")
print(f"   Query Timeout: {Config.QUERY_TIMEOUT} seconds")
print(f"   Items Per Page: {Config.ITEMS_PER_PAGE}")

print(f"\n🏥 Hospital Info:")
print(f"   Name: {Config.HOSPITAL_NAME}")
print(f"   Address: {Config.HOSPITAL_ADDRESS}")
print(f"   City: {Config.HOSPITAL_CITY}")
print(f"   Phone: {Config.HOSPITAL_PHONE}")

print(f"\n📁 Upload Settings:")
print(f"   Max Upload: {int(Config.MAX_CONTENT_LENGTH / (1024*1024))} MB")
print(f"   Upload Folder: {Config.UPLOAD_FOLDER}")

print(f"\n" + "="*70)
print("✅ Configuration loaded successfully from .env!")
print("="*70 + "\n")
