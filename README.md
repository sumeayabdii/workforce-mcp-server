# Revelio-Style Workforce MCP Server

A small Model Context Protocol (MCP) server built in Python using the official MCP Python SDK.

This project demonstrates how workforce/job-posting data can be exposed as tools that an AI assistant can call.

## Features

* Search job postings by skill
* Count postings by company
* Typed tool inputs using Pydantic
* Input validation and helpful errors
* Clear tool descriptions designed for LLM tool selection
* Sample dataset with fictional job postings
* Tested using MCP Inspector

## Tech Stack

* Python 3.10+
* MCP Python SDK
* Pydantic
* JSON

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]"
```

On Windows:

```bash
.venv\Scripts\activate
pip install "mcp[cli]"
```

## Run

```bash
mcp dev server.py
```

This opens the server in MCP Inspector.

## Available Tools

### `search_postings_by_skill`

Searches the dataset for job postings containing a requested skill.

Example:

```text
skill: python
```

The tool returns the matching posting ID, company, title, and skills.

### `count_postings_by_company`

Counts the number of postings belonging to a specific company.

Example:

```text
company: Acme AI
```

Returns:

```json
{
  "company": "Acme AI",
  "count": 2
}
```

## Validation

Inputs are validated before the tool executes.

For example:

* Empty skills are rejected.
* Empty company names are rejected.
* Skill input is limited to a reasonable length.
* Company input is limited to a reasonable length.

The server also normalizes case when searching.

## Security Design: OAuth 2.0

For a production version, I would protect the MCP server using OAuth 2.0 Authorization Code flow with PKCE.

The flow would be:

1. The MCP client redirects the user to the authorization server.
2. The user authenticates and grants the requested scopes.
3. The client receives an authorization code.
4. The client exchanges the code for an access token.
5. The MCP server validates the access token on every protected request.
6. The server identifies the user associated with the token.
7. The server checks that the requested resource is allowed for that user.
8. Expired or invalid tokens are rejected.

I would use short-lived access tokens and refresh tokens where appropriate.

### Example scopes

* `postings:read` - read permitted job-posting data
* `postings:search` - search permitted postings
* `company:read` - read company-level aggregate information

The server should use least privilege: a client that only needs to search postings should not receive broader access.

### Token validation

For an HTTP deployment, token validation would happen before the MCP tool handler is allowed to execute.

The authentication layer would:

* Verify the token signature or introspect the token with the authorization server.
* Check issuer and audience.
* Check expiry.
* Check required scopes.
* Resolve the authenticated user.
* Apply authorization rules before returning data.

I would never trust a user ID supplied directly as a tool argument.

## Threat Model

Important risks include:

* Stolen or expired access tokens
* Overly broad OAuth scopes
* Unauthorized access to workforce data
* Prompt injection attempting to make a model request unauthorized information
* Excessive requests and abuse
* Sensitive information accidentally returned in tool responses

Mitigations include short-lived tokens, least-privilege scopes, server-side authorization, input validation, rate limiting, logging, monitoring, and compact responses.

## Why MCP?

MCP provides a standardized interface for AI applications to discover and call tools. Instead of building a separate integration for every AI assistant, the same MCP server can expose a consistent set of tools.

## Dataset

The included dataset is fictional and exists only to demonstrate the MCP implementation. It does not contain real Revelio Labs data.

## Future Improvements

* Streamable HTTP deployment
* OAuth 2.0 middleware
* Persistent database
* Per-user authorization
* Rate limiting
* Structured logging and monitoring
* Automated tests
* Rust implementation using the same dataset
* [![M8ven Score](https://m8ven.ai)](https://m8ven.ai)

