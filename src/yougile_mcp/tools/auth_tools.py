"""
MCP tools for YouGile authentication and setup.
Handles initial authentication, API key management, and company selection.
"""

from typing import List, Dict, Any
from mcp.server.fastmcp import Context
from ...core import AuthManager, YouGileClient, models, auth_manager
from ...api import auth as auth_api
from ...utils.validation import validate_email, validate_uuid
from ...utils.formatting import format_error_message, format_success_message


async def get_companies_tool(login: str, password: str, ctx: Context) -> List[models.Company]:
    """
    Get list of companies available to user.
    
    Args:
        login: User email address
        password: User password  
        ctx: MCP context for logging and progress
        
    Returns:
        List of Company objects with id and title
    """
    try:
        await ctx.info("Fetching companies from YouGile...")
        
        # Validate inputs
        email = validate_email(login)
        
        # Create temporary client for authentication
        temp_auth_manager = AuthManager()
        async with YouGileClient(temp_auth_manager) as client:
            # Note: This call doesn't require API key, uses login/password
            companies_data = await auth_api.get_companies(client, email, password)
            
            await ctx.debug(f"Found {len(companies_data)} companies")
            
            # Convert to structured output
            companies = [
                models.Company(
                    id=company.get("id", ""),
                    title=company.get("title", "Unknown Company"),
                    timestamp=company.get("timestamp"),
                    deleted=company.get("deleted", False)
                )
                for company in companies_data
            ]
            
            await ctx.info(f"Successfully retrieved {len(companies)} companies")
            return companies
            
    except Exception as e:
        await ctx.error(f"Failed to get companies: {str(e)}")
        raise


async def create_api_key_tool(
    login: str, 
    password: str, 
    company_id: str, 
    ctx: Context
) -> models.ApiKey:
    """
    Create API key for accessing YouGile API.
    
    Args:
        login: User email address
        password: User password
        company_id: ID of company to create key for
        ctx: MCP context for logging and progress
        
    Returns:
        ApiKey object with key value and company_id
    """
    try:
        await ctx.info(f"Creating API key for company {company_id[:8]}...")
        
        # Validate inputs
        email = validate_email(login)
        company_uuid = validate_uuid(company_id, "company_id")
        
        # Create temporary client for authentication
        temp_auth_manager = AuthManager()
        async with YouGileClient(temp_auth_manager) as client:
            key_value = await auth_api.create_api_key(client, email, password, company_uuid)
            
            if not key_value:
                raise ValueError("No API key returned from server")
            
            # Save credentials to global auth manager for subsequent requests
            auth_manager.set_credentials(key_value, company_uuid)
            
            api_key = models.ApiKey(
                key=key_value,
                company_id=company_uuid
            )
            
            await ctx.info("API key created successfully")
            await ctx.debug(f"Key starts with: {key_value[:10]}...")
            
            return api_key
            
    except Exception as e:
        await ctx.error(f"Failed to create API key: {str(e)}")
        raise


async def setup_authentication_tool(
    login: str,
    password: str,
    company_id: str = None,
    ctx: Context = None
) -> models.ApiKey:
    """
    Complete authentication setup - get companies and create API key in one step.
    
    Args:
        login: User email address
        password: User password
        company_id: Optional company ID. If not provided, will use first available company
        ctx: MCP context for logging and progress
        
    Returns:
        ApiKey object with key value and company_id
    """
    try:
        await ctx.info("🔑 Setting up YouGile authentication...")
        
        # Step 1: Get available companies
        await ctx.info("Step 1: Fetching available companies...")
        companies = await get_companies_tool(login, password, ctx)
        
        if not companies:
            raise ValueError("No companies available for this user")
        
        # Step 2: Select company
        if company_id:
            # Use provided company ID
            company_uuid = validate_uuid(company_id, "company_id")
            selected_company = next((c for c in companies if c.id == company_uuid), None)
            if not selected_company:
                available_ids = [c.id for c in companies]
                raise ValueError(f"Company {company_id} not found. Available: {available_ids}")
        else:
            # Use first available company
            selected_company = companies[0]
            company_uuid = selected_company.id
            await ctx.info(f"Using first available company: {selected_company.title}")
        
        await ctx.info(f"Selected company: {selected_company.title} ({company_uuid})")
        
        # Step 3: Create API key
        await ctx.info("Step 2: Creating API key...")
        api_key = await create_api_key_tool(login, password, company_uuid, ctx)
        
        await ctx.info("✅ Authentication setup completed successfully!")
        await ctx.info(f"Company: {selected_company.title}")
        await ctx.info("You can now use all YouGile MCP tools")
        
        return api_key
        
    except Exception as e:
        await ctx.error(f"Failed to setup authentication: {str(e)}")
        raise


async def list_api_keys_tool(
    login: str,
    password: str,
    company_id: str = None,
    ctx: Context = None
) -> List[Dict[str, Any]]:
    """Get list of existing API keys for the user."""
    try:
        await ctx.info("📋 Fetching API keys...")
        
        # Validate inputs
        email = validate_email(login)
        if company_id:
            company_id = validate_uuid(company_id, "company_id")
        
        # Create temporary client for authentication
        temp_auth_manager = AuthManager()
        async with YouGileClient(temp_auth_manager) as client:
            keys_data = await auth_api.get_api_keys(client, email, password, company_id)
            
        await ctx.info(f"✅ Found {len(keys_data)} API keys")
        
        # Add key preview (first 10 chars + "...")
        for key_info in keys_data:
            if 'key' in key_info:
                key_info['key_preview'] = key_info['key'][:10] + "..."
        
        return keys_data
        
    except Exception as e:
        await ctx.error(f"Failed to get API keys: {str(e)}")
        raise


async def delete_api_key_tool(api_key: str, ctx: Context) -> Dict[str, Any]:
    """Delete an API key."""
    try:
        await ctx.info(f"🗑️ Deleting API key: {api_key[:10]}...")
        
        # Create temporary client for this operation
        temp_auth_manager = AuthManager()
        async with YouGileClient(temp_auth_manager) as client:
            await auth_api.delete_api_key(client, api_key)
            
        await ctx.info("✅ API key deleted successfully")
        return {"success": True, "message": "API key deleted", "key_preview": api_key[:10] + "..."}
        
    except Exception as e:
        await ctx.error(f"Failed to delete API key: {str(e)}")
        raise