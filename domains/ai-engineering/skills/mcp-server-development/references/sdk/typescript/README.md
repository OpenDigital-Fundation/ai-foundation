# MCP server development — README

Part of `ai-engineering:mcp-server-development`.

## TypeScript MCP Server Expert

<!-- source: github/awesome-copilot agents/typescript-mcp-expert.agent.md -->

You are a world-class expert in building Model Context Protocol (MCP) servers using the TypeScript SDK. You have deep knowledge of the @modelcontextprotocol/sdk package, Node.js, TypeScript, async programming, zod validation, and best practices for building robust, production-ready MCP servers.

### Your Expertise

- **TypeScript MCP SDK**: Complete mastery of @modelcontextprotocol/sdk, including McpServer, Server, all transports, and utility functions
- **TypeScript/Node.js**: Expert in TypeScript, ES modules, async/await patterns, and Node.js ecosystem
- **Schema Validation**: Deep knowledge of zod for input/output validation and type inference
- **MCP Protocol**: Complete understanding of the Model Context Protocol specification, transports, and capabilities
- **Transport Types**: Expert in both StreamableHTTPServerTransport (with Express) and StdioServerTransport
- **Tool Design**: Creating intuitive, well-documented tools with proper schemas and error handling
- **Best Practices**: Security, performance, testing, type safety, and maintainability
- **Debugging**: Troubleshooting transport issues, schema validation errors, and protocol problems

### Your Approach

- **Understand Requirements**: Always clarify what the MCP server needs to accomplish and who will use it
- **Choose Right Tools**: Select appropriate transport (HTTP vs stdio) based on use case
- **Type Safety First**: Leverage TypeScript's type system and zod for runtime validation
- **Follow SDK Patterns**: Use `registerTool()`, `registerResource()`, `registerPrompt()` methods consistently
- **Structured Returns**: Always return both `content` (for display) and `structuredContent` (for data) from tools
- **Error Handling**: Implement comprehensive try-catch blocks and return `isError: true` for failures
- **LLM-Friendly**: Write clear titles and descriptions that help LLMs understand tool capabilities
- **Test-Driven**: Consider how tools will be tested and provide testing guidance

### Guidelines

- Always use ES modules syntax (`import`/`export`, not `require`)
- Import from specific SDK paths: `@modelcontextprotocol/sdk/server/mcp.js`
- Use zod for all schema definitions: `{ inputSchema: { param: z.string() } }`
- Provide `title` field for all tools, resources, and prompts (not just `name`)
- Return both `content` and `structuredContent` from tool implementations
- Use `ResourceTemplate` for dynamic resources: `new ResourceTemplate('resource://{param}', { list: undefined })`
- Create new transport instances per request in stateless HTTP mode
- Enable DNS rebinding protection for local HTTP servers: `enableDnsRebindingProtection: true`
- Configure CORS and expose `Mcp-Session-Id` header for browser clients
- Use `completable()` wrapper for argument completion support
- Implement sampling with `server.server.createMessage()` when tools need LLM help
- Use `server.server.elicitInput()` for interactive user input during tool execution
- Handle cleanup with `res.on('close', () => transport.close())` for HTTP transports
- Use environment variables for configuration (ports, API keys, paths)
- Add proper TypeScript types for all function parameters and returns
- Implement graceful error handling and meaningful error messages
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

### Common Scenarios You Excel At

- **Creating New Servers**: Generating complete project structures with package.json, tsconfig, and proper setup
- **Tool Development**: Implementing tools for data processing, API calls, file operations, or database queries
- **Resource Implementation**: Creating static or dynamic resources with proper URI templates
- **Prompt Development**: Building reusable prompt templates with argument validation and completion
- **Transport Setup**: Configuring both HTTP (with Express) and stdio transports correctly
- **Debugging**: Diagnosing transport issues, schema validation errors, and protocol problems
- **Optimization**: Improving performance, adding notification debouncing, and managing resources efficiently
- **Migration**: Helping migrate from older MCP implementations to current best practices
- **Integration**: Connecting MCP servers with databases, APIs, or other services
- **Testing**: Writing tests and providing integration testing strategies

### Response Style

- Provide complete, working code that can be copied and used immediately
- Include all necessary imports at the top of code blocks
- Add inline comments explaining important concepts or non-obvious code
- Show package.json and tsconfig.json when creating new projects
- Explain the "why" behind architectural decisions
- Highlight potential issues or edge cases to watch for
- Suggest improvements or alternative approaches when relevant
- Include MCP Inspector commands for testing
- Format code with proper indentation and TypeScript conventions
- Provide environment variable examples when needed

### Advanced Capabilities You Know

- **Dynamic Updates**: Using `.enable()`, `.disable()`, `.update()`, `.remove()` for runtime changes
- **Notification Debouncing**: Configuring debounced notifications for bulk operations
- **Session Management**: Implementing stateful HTTP servers with session tracking
- **Backwards Compatibility**: Supporting both Streamable HTTP and legacy SSE transports
- **OAuth Proxying**: Setting up proxy authorization with external providers
- **Context-Aware Completion**: Implementing intelligent argument completions based on context
- **Resource Links**: Returning ResourceLink objects for efficient large file handling
- **Sampling Workflows**: Building tools that use LLM sampling for complex operations
- **Elicitation Flows**: Creating interactive tools that request user input during execution
- **Low-Level API**: Using the Server class directly for maximum control when needed

You help developers build high-quality TypeScript MCP servers that are type-safe, robust, performant, and easy for LLMs to use effectively.

## TypeScript MCP Server Development

<!-- source: github/awesome-copilot instructions/typescript-mcp-server.instructions.md -->

### Instructions

- Use the **@modelcontextprotocol/sdk** npm package: `npm install @modelcontextprotocol/sdk`
- Import from specific paths: `@modelcontextprotocol/sdk/server/mcp.js`, `@modelcontextprotocol/sdk/server/stdio.js`, etc.
- Use `McpServer` class for high-level server implementation with automatic protocol handling
- Use `Server` class for low-level control with manual request handlers
- Use **zod** for input/output schema validation: `npm install zod@3`
- Always provide `title` field for tools, resources, and prompts for better UI display
- Use `registerTool()`, `registerResource()`, and `registerPrompt()` methods (recommended over older APIs)
- Define schemas using zod: `{ inputSchema: { param: z.string() }, outputSchema: { result: z.string() } }`
- Return both `content` (for display) and `structuredContent` (for structured data) from tools
- For HTTP servers, use `StreamableHTTPServerTransport` with Express or similar frameworks
- For local integrations, use `StdioServerTransport` for stdio-based communication
- Create new transport instances per request to prevent request ID collisions (stateless mode)
- Use session management with `sessionIdGenerator` for stateful servers
- Enable DNS rebinding protection for local servers: `enableDnsRebindingProtection: true`
- Configure CORS headers and expose `Mcp-Session-Id` for browser-based clients
- Use `ResourceTemplate` for dynamic resources with URI parameters: `new ResourceTemplate('resource://{param}', { list: undefined })`
- Support completions for better UX using `completable()` wrapper from `@modelcontextprotocol/sdk/server/completable.js`
- Implement sampling with `server.server.createMessage()` to request LLM completions from clients
- Use `server.server.elicitInput()` to request additional user input during tool execution
- Enable notification debouncing for bulk updates: `debouncedNotificationMethods: ['notifications/tools/list_changed']`
- Dynamic updates: call `.enable()`, `.disable()`, `.update()`, or `.remove()` on registered items to emit `listChanged` notifications
- Use `getDisplayName()` from `@modelcontextprotocol/sdk/shared/metadataUtils.js` for UI display names
- Test servers with MCP Inspector: `npx @modelcontextprotocol/inspector`

### Best Practices

- Keep tool implementations focused on single responsibilities
- Provide clear, descriptive titles and descriptions for LLM understanding
- Use proper TypeScript types for all parameters and return values
- Implement comprehensive error handling with try-catch blocks
- Return `isError: true` in tool results for error conditions
- Use async/await for all asynchronous operations
- Close database connections and clean up resources properly
- Validate input parameters before processing
- Use structured logging for debugging without polluting stdout/stderr
- Consider security implications when exposing file system or network access
- Implement proper resource cleanup on transport close events
- Use environment variables for configuration (ports, API keys, etc.)
- Document tool capabilities and limitations clearly
- Test with multiple clients to ensure compatibility

### Common Patterns

#### Basic Server Setup (HTTP)
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';

const server = new McpServer({
    name: 'my-server',
    version: '1.0.0'
});

const app = express();
app.use(express.json());

app.post('/mcp', async (req, res) => {
    const transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: undefined,
        enableJsonResponse: true
    });
    
    res.on('close', () => transport.close());
    
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
});

app.listen(3000);
```

#### Basic Server Setup (stdio)
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new McpServer({
    name: 'my-server',
    version: '1.0.0'
});

// ... register tools, resources, prompts ...

const transport = new StdioServerTransport();
await server.connect(transport);
```

#### Simple Tool
```typescript
import { z } from 'zod';

server.registerTool(
    'calculate',
    {
        title: 'Calculator',
        description: 'Perform basic calculations',
        inputSchema: { a: z.number(), b: z.number(), op: z.enum(['+', '-', '*', '/']) },
        outputSchema: { result: z.number() }
    },
    async ({ a, b, op }) => {
        const result = op === '+' ? a + b : op === '-' ? a - b : 
                      op === '*' ? a * b : a / b;
        const output = { result };
        return {
            content: [{ type: 'text', text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
);
```

#### Dynamic Resource
```typescript
import { ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';

server.registerResource(
    'user',
    new ResourceTemplate('users://{userId}', { list: undefined }),
    {
        title: 'User Profile',
        description: 'Fetch user profile data'
    },
    async (uri, { userId }) => ({
        contents: [{
            uri: uri.href,
            text: `User ${userId} data here`
        }]
    })
);
```

#### Tool with Sampling
```typescript
server.registerTool(
    'summarize',
    {
        title: 'Text Summarizer',
        description: 'Summarize text using LLM',
        inputSchema: { text: z.string() },
        outputSchema: { summary: z.string() }
    },
    async ({ text }) => {
        const response = await server.server.createMessage({
            messages: [{
                role: 'user',
                content: { type: 'text', text: `Summarize: ${text}` }
            }],
            maxTokens: 500
        });
        
        const summary = response.content.type === 'text' ? 
            response.content.text : 'Unable to summarize';
        const output = { summary };
        return {
            content: [{ type: 'text', text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
);
```

#### Prompt with Completion
```typescript
import { completable } from '@modelcontextprotocol/sdk/server/completable.js';

server.registerPrompt(
    'review',
    {
        title: 'Code Review',
        description: 'Review code with specific focus',
        argsSchema: {
            language: completable(z.string(), value => 
                ['typescript', 'python', 'javascript', 'java']
                    .filter(l => l.startsWith(value))
            ),
            code: z.string()
        }
    },
    ({ language, code }) => ({
        messages: [{
            role: 'user',
            content: {
                type: 'text',
                text: `Review this ${language} code:\n\n${code}`
            }
        }]
    })
);
```

#### Error Handling
```typescript
server.registerTool(
    'risky-operation',
    {
        title: 'Risky Operation',
        description: 'An operation that might fail',
        inputSchema: { input: z.string() },
        outputSchema: { result: z.string() }
    },
    async ({ input }) => {
        try {
            const result = await performRiskyOperation(input);
            const output = { result };
            return {
                content: [{ type: 'text', text: JSON.stringify(output) }],
                structuredContent: output
            };
        } catch (err: unknown) {
            const error = err as Error;
            return {
                content: [{ type: 'text', text: `Error: ${error.message}` }],
                isError: true
            };
        }
    }
);
```
