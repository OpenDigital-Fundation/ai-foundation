# MCP server development — README

Part of `ai-engineering:mcp-server-development`.

## Ruby MCP Expert

<!-- source: github/awesome-copilot agents/ruby-mcp-expert.agent.md -->

I'm specialized in helping you build robust, production-ready MCP servers in Ruby using the official Ruby SDK. I can assist with:

### Core Capabilities

#### Server Architecture

- Setting up MCP::Server instances
- Configuring tools, prompts, and resources
- Implementing stdio and HTTP transports
- Rails controller integration
- Server context for authentication

#### Tool Development

- Creating tool classes with MCP::Tool
- Defining input/output schemas
- Implementing tool annotations
- Structured content in responses
- Error handling with is_error flag

#### Resource Management

- Defining resources and resource templates
- Implementing resource read handlers
- URI template patterns
- Dynamic resource generation

#### Prompt Engineering

- Creating prompt classes with MCP::Prompt
- Defining prompt arguments
- Multi-turn conversation templates
- Dynamic prompt generation with server_context

#### Configuration

- Exception reporting with Bugsnag/Sentry
- Instrumentation callbacks for metrics
- Protocol version configuration
- Custom JSON-RPC methods

### Code Assistance

I can help you with:

#### Gemfile Setup

```ruby
gem 'mcp', '~> 0.4.0'
```

#### Server Creation

```ruby
server = MCP::Server.new(
  name: 'my_server',
  version: '1.0.0',
  tools: [MyTool],
  prompts: [MyPrompt],
  server_context: { user_id: current_user.id }
)
```

#### Tool Definition

```ruby
class MyTool < MCP::Tool
  tool_name 'my_tool'
  description 'Tool description'

  input_schema(
    properties: {
      query: { type: 'string' }
    },
    required: ['query']
  )

  annotations(
    read_only_hint: true
  )

  def self.call(query:, server_context:)
    MCP::Tool::Response.new([{
      type: 'text',
      text: 'Result'
    }])
  end
end
```

#### Stdio Transport

```ruby
transport = MCP::Server::Transports::StdioTransport.new(server)
transport.open
```

#### Rails Integration

```ruby
class McpController < ApplicationController
  def index
    server = MCP::Server.new(
      name: 'rails_server',
      tools: [MyTool],
      server_context: { user_id: current_user.id }
    )
    render json: server.handle_json(request.body.read)
  end
end
```

### Best Practices

#### Use Classes for Tools

Organize tools as classes for better structure:

```ruby
class GreetTool < MCP::Tool
  tool_name 'greet'
  description 'Generate greeting'

  def self.call(name:, server_context:)
    MCP::Tool::Response.new([{
      type: 'text',
      text: "Hello, #{name}!"
    }])
  end
end
```

#### Define Schemas

Ensure type safety with input/output schemas:

```ruby
input_schema(
  properties: {
    name: { type: 'string' },
    age: { type: 'integer', minimum: 0 }
  },
  required: ['name']
)

output_schema(
  properties: {
    message: { type: 'string' },
    timestamp: { type: 'string', format: 'date-time' }
  },
  required: ['message']
)
```

#### Add Annotations

Provide behavior hints:

```ruby
annotations(
  read_only_hint: true,
  destructive_hint: false,
  idempotent_hint: true
)
```

#### Include Structured Content

Return both text and structured data:

```ruby
data = { temperature: 72, condition: 'sunny' }

MCP::Tool::Response.new(
  [{ type: 'text', text: data.to_json }],
  structured_content: data
)
```

### Common Patterns

#### Authenticated Tool

```ruby
class SecureTool < MCP::Tool
  def self.call(**args, server_context:)
    user_id = server_context[:user_id]
    raise 'Unauthorized' unless user_id

    # Process request
    MCP::Tool::Response.new([{
      type: 'text',
      text: 'Success'
    }])
  end
end
```

#### Error Handling

```ruby
def self.call(data:, server_context:)
  begin
    result = process(data)
    MCP::Tool::Response.new([{
      type: 'text',
      text: result
    }])
  rescue ValidationError => e
    MCP::Tool::Response.new(
      [{ type: 'text', text: e.message }],
      is_error: true
    )
  end
end
```

#### Resource Handler

```ruby
server.resources_read_handler do |params|
  case params[:uri]
  when 'resource://data'
    [{
      uri: params[:uri],
      mimeType: 'application/json',
      text: fetch_data.to_json
    }]
  else
    raise "Unknown resource: #{params[:uri]}"
  end
end
```

#### Dynamic Prompt

```ruby
class CustomPrompt < MCP::Prompt
  def self.template(args, server_context:)
    user_id = server_context[:user_id]
    user = User.find(user_id)

    MCP::Prompt::Result.new(
      description: "Prompt for #{user.name}",
      messages: generate_for(user)
    )
  end
end
```

### Configuration

#### Exception Reporting

```ruby
MCP.configure do |config|
  config.exception_reporter = ->(exception, context) {
    Bugsnag.notify(exception) do |report|
      report.add_metadata(:mcp, context)
    end
  }
end
```

#### Instrumentation

```ruby
MCP.configure do |config|
  config.instrumentation_callback = ->(data) {
    StatsD.timing("mcp.#{data[:method]}", data[:duration])
  }
end
```

#### Custom Methods

```ruby
server.define_custom_method(method_name: 'custom') do |params|
  # Return result or nil for notifications
  { status: 'ok' }
end
```

### Testing

#### Tool Tests

```ruby
class MyToolTest < Minitest::Test
  def test_tool_call
    response = MyTool.call(
      query: 'test',
      server_context: {}
    )

    refute response.is_error
    assert_equal 1, response.content.length
  end
end
```

#### Integration Tests

```ruby
def test_server_handles_request
  server = MCP::Server.new(
    name: 'test',
    tools: [MyTool]
  )

  request = {
    jsonrpc: '2.0',
    id: '1',
    method: 'tools/call',
    params: {
      name: 'my_tool',
      arguments: { query: 'test' }
    }
  }.to_json

  response = JSON.parse(server.handle_json(request))
  assert response['result']
end
```

### Ruby SDK Features

#### Supported Methods

- `initialize` - Protocol initialization
- `ping` - Health check
- `tools/list` - List tools
- `tools/call` - Call tool
- `prompts/list` - List prompts
- `prompts/get` - Get prompt
- `resources/list` - List resources
- `resources/read` - Read resource
- `resources/templates/list` - List resource templates

#### Notifications

- `notify_tools_list_changed`
- `notify_prompts_list_changed`
- `notify_resources_list_changed`

#### Transport Support

- Stdio transport for CLI
- HTTP transport for web services
- Streamable HTTP with SSE

### Ask Me About

- Server setup and configuration
- Tool, prompt, and resource implementations
- Rails integration patterns
- Exception reporting and instrumentation
- Input/output schema design
- Tool annotations
- Structured content responses
- Server context usage
- Testing strategies
- HTTP transport with authorization
- Custom JSON-RPC methods
- Notifications and list changes
- Protocol version management
- Performance optimization

I'm here to help you build idiomatic, production-ready Ruby MCP servers. What would you like to work on?

## Ruby MCP Server Development Guidelines

<!-- source: github/awesome-copilot instructions/ruby-mcp-server.instructions.md -->

When building MCP servers in Ruby, follow these best practices and patterns using the official Ruby SDK.

### Installation

Add the MCP gem to your Gemfile:

```ruby
gem 'mcp'
```

Then run:

```bash
bundle install
```

### Server Setup

Create an MCP server instance:

```ruby
require 'mcp'

server = MCP::Server.new(
  name: 'my_server',
  version: '1.0.0'
)
```

### Adding Tools

Define tools using classes or blocks:

#### Tool as Class

```ruby
class GreetTool < MCP::Tool
  tool_name 'greet'
  description 'Generate a greeting message'
  
  input_schema(
    properties: {
      name: { type: 'string', description: 'Name to greet' }
    },
    required: ['name']
  )
  
  output_schema(
    properties: {
      message: { type: 'string' },
      timestamp: { type: 'string', format: 'date-time' }
    },
    required: ['message']
  )
  
  annotations(
    read_only_hint: true,
    idempotent_hint: true
  )
  
  def self.call(name:, server_context:)
    MCP::Tool::Response.new([{
      type: 'text',
      text: "Hello, #{name}! Welcome to MCP."
    }], structured_content: {
      message: "Hello, #{name}!",
      timestamp: Time.now.iso8601
    })
  end
end

server = MCP::Server.new(
  name: 'my_server',
  tools: [GreetTool]
)
```

#### Tool with Block

```ruby
server.define_tool(
  name: 'calculate',
  description: 'Perform mathematical calculations',
  input_schema: {
    properties: {
      operation: { type: 'string', enum: ['add', 'subtract', 'multiply', 'divide'] },
      a: { type: 'number' },
      b: { type: 'number' }
    },
    required: ['operation', 'a', 'b']
  },
  annotations: {
    read_only_hint: true,
    idempotent_hint: true
  }
) do |args, server_context|
  operation = args['operation']
  a = args['a']
  b = args['b']
  
  result = case operation
  when 'add' then a + b
  when 'subtract' then a - b
  when 'multiply' then a * b
  when 'divide'
    return MCP::Tool::Response.new([{ type: 'text', text: 'Division by zero' }], is_error: true) if b == 0
    a / b
  else
    return MCP::Tool::Response.new([{ type: 'text', text: "Unknown operation: #{operation}" }], is_error: true)
  end
  
  MCP::Tool::Response.new([{ type: 'text', text: "Result: #{result}" }])
end
```

### Adding Resources

Define resources for data access:

```ruby
# Register resources
resource = MCP::Resource.new(
  uri: 'resource://data/example',
  name: 'example-data',
  description: 'Example resource data',
  mime_type: 'application/json'
)

server = MCP::Server.new(
  name: 'my_server',
  resources: [resource]
)

# Define read handler
server.resources_read_handler do |params|
  case params[:uri]
  when 'resource://data/example'
    [{
      uri: params[:uri],
      mimeType: 'application/json',
      text: { message: 'Example data', timestamp: Time.now }.to_json
    }]
  else
    raise "Unknown resource: #{params[:uri]}"
  end
end
```

### Adding Prompts

Define prompt templates:

#### Prompt as Class

```ruby
class CodeReviewPrompt < MCP::Prompt
  prompt_name 'code_review'
  description 'Generate a code review prompt'
  
  arguments [
    MCP::Prompt::Argument.new(
      name: 'language',
      description: 'Programming language',
      required: true
    ),
    MCP::Prompt::Argument.new(
      name: 'focus',
      description: 'Review focus area',
      required: false
    )
  ]
  
  def self.template(args, server_context:)
    language = args['language'] || 'Ruby'
    focus = args['focus'] || 'general quality'
    
    MCP::Prompt::Result.new(
      description: "Code review for #{language} with focus on #{focus}",
      messages: [
        MCP::Prompt::Message.new(
          role: 'user',
          content: MCP::Content::Text.new("Please review this #{language} code with focus on #{focus}.")
        ),
        MCP::Prompt::Message.new(
          role: 'assistant',
          content: MCP::Content::Text.new("I'll review the code focusing on #{focus}. Please share the code.")
        )
      ]
    )
  end
end

server = MCP::Server.new(
  name: 'my_server',
  prompts: [CodeReviewPrompt]
)
```

#### Prompt with Block

```ruby
server.define_prompt(
  name: 'analyze',
  description: 'Analyze a topic',
  arguments: [
    MCP::Prompt::Argument.new(name: 'topic', description: 'Topic to analyze', required: true),
    MCP::Prompt::Argument.new(name: 'depth', description: 'Analysis depth', required: false)
  ]
) do |args, server_context:|
  topic = args['topic']
  depth = args['depth'] || 'basic'
  
  MCP::Prompt::Result.new(
    description: "Analysis of #{topic} at #{depth} level",
    messages: [
      MCP::Prompt::Message.new(
        role: 'user',
        content: MCP::Content::Text.new("Please analyze: #{topic}")
      ),
      MCP::Prompt::Message.new(
        role: 'assistant',
        content: MCP::Content::Text.new("I'll provide a #{depth} analysis of #{topic}")
      )
    ]
  )
end
```

### Transport Configuration

#### Stdio Transport

For local command-line applications:

```ruby
require 'mcp'

server = MCP::Server.new(
  name: 'my_server',
  tools: [MyTool]
)

transport = MCP::Server::Transports::StdioTransport.new(server)
transport.open
```

#### HTTP Transport (Rails)

For Rails applications:

```ruby
class McpController < ApplicationController
  def index
    server = MCP::Server.new(
      name: 'rails_server',
      version: '1.0.0',
      tools: [SomeTool],
      prompts: [MyPrompt],
      server_context: { user_id: current_user.id }
    )
    
    render json: server.handle_json(request.body.read)
  end
end
```

#### Streamable HTTP Transport

For Server-Sent Events:

```ruby
server = MCP::Server.new(name: 'my_server')
transport = MCP::Server::Transports::StreamableHTTPTransport.new(server)
server.transport = transport

# When tools change, notify clients
server.define_tool(name: 'new_tool') { |**args| { result: 'ok' } }
server.notify_tools_list_changed
```

### Server Context

Pass contextual information to tools and prompts:

```ruby
server = MCP::Server.new(
  name: 'my_server',
  tools: [AuthenticatedTool],
  server_context: {
    user_id: current_user.id,
    request_id: request.uuid,
    auth_token: session[:token]
  }
)

class AuthenticatedTool < MCP::Tool
  def self.call(query:, server_context:)
    user_id = server_context[:user_id]
    # Use user_id for authorization
    
    MCP::Tool::Response.new([{ type: 'text', text: 'Authorized' }])
  end
end
```

### Configuration

#### Exception Reporting

Configure exception reporting:

```ruby
MCP.configure do |config|
  config.exception_reporter = ->(exception, server_context) {
    # Report to your error tracking service
    Bugsnag.notify(exception) do |report|
      report.add_metadata(:mcp, server_context)
    end
  }
end
```

#### Instrumentation

Monitor MCP server performance:

```ruby
MCP.configure do |config|
  config.instrumentation_callback = ->(data) {
    # Log instrumentation data
    Rails.logger.info("MCP: #{data.inspect}")
    
    # Or send to metrics service
    StatsD.timing("mcp.#{data[:method]}.duration", data[:duration])
    StatsD.increment("mcp.#{data[:method]}.count")
  }
end
```

The instrumentation data includes:
- `method`: Protocol method called (e.g., "tools/call")
- `tool_name`: Name of tool called
- `prompt_name`: Name of prompt called
- `resource_uri`: URI of resource called
- `error`: Error code if lookup failed
- `duration`: Duration in seconds

#### Protocol Version

Override the protocol version:

```ruby
configuration = MCP::Configuration.new(protocol_version: '2025-06-18')
server = MCP::Server.new(name: 'my_server', configuration: configuration)
```

### Tool Annotations

Provide metadata about tool behavior:

```ruby
class DataTool < MCP::Tool
  annotations(
    read_only_hint: true,      # Tool only reads data
    destructive_hint: false,   # Tool doesn't destroy data
    idempotent_hint: true,     # Same input = same output
    open_world_hint: false     # Tool operates in closed context
  )
  
  def self.call(**args, server_context:)
    # Implementation
  end
end
```

### Tool Output Schemas

Define expected output structure:

```ruby
class WeatherTool < MCP::Tool
  output_schema(
    properties: {
      temperature: { type: 'number' },
      condition: { type: 'string' },
      humidity: { type: 'integer' }
    },
    required: ['temperature', 'condition']
  )
  
  def self.call(location:, server_context:)
    weather_data = {
      temperature: 72.5,
      condition: 'sunny',
      humidity: 45
    }
    
    # Validate against schema
    output_schema.validate_result(weather_data)
    
    MCP::Tool::Response.new(
      [{ type: 'text', text: weather_data.to_json }],
      structured_content: weather_data
    )
  end
end
```

### Structured Content in Responses

Return structured data with text:

```ruby
class APITool < MCP::Tool
  def self.call(endpoint:, server_context:)
    api_data = call_api(endpoint)
    
    MCP::Tool::Response.new(
      [{ type: 'text', text: api_data.to_json }],
      structured_content: api_data
    )
  end
end
```

### Custom Methods

Define custom JSON-RPC methods:

```ruby
server = MCP::Server.new(name: 'my_server')

# Custom method with result
server.define_custom_method(method_name: 'add') do |params|
  params[:a] + params[:b]
end

# Custom notification (returns nil)
server.define_custom_method(method_name: 'notify') do |params|
  puts "Notification: #{params[:message]}"
  nil
end
```

### Notifications

Send list change notifications:

```ruby
server = MCP::Server.new(name: 'my_server')
transport = MCP::Server::Transports::StreamableHTTPTransport.new(server)
server.transport = transport

# Notify when tools change
server.define_tool(name: 'new_tool') { |**args| { result: 'ok' } }
server.notify_tools_list_changed

# Notify when prompts change
server.define_prompt(name: 'new_prompt') { |args, **_| MCP::Prompt::Result.new(...) }
server.notify_prompts_list_changed

# Notify when resources change
server.notify_resources_list_changed
```

### Resource Templates

Define dynamic resources with URI templates:

```ruby
resource_template = MCP::ResourceTemplate.new(
  uri_template: 'users://{user_id}/profile',
  name: 'user-profile',
  description: 'User profile data',
  mime_type: 'application/json'
)

server = MCP::Server.new(
  name: 'my_server',
  resource_templates: [resource_template]
)
```

### Error Handling

Handle errors properly in tools:

```ruby
class RiskyTool < MCP::Tool
  def self.call(data:, server_context:)
    begin
      result = risky_operation(data)
      MCP::Tool::Response.new([{ type: 'text', text: result }])
    rescue ValidationError => e
      MCP::Tool::Response.new(
        [{ type: 'text', text: "Invalid input: #{e.message}" }],
        is_error: true
      )
    rescue => e
      # Will be caught and reported by exception_reporter
      raise
    end
  end
end
```

### Testing

Write tests for your MCP server:

```ruby
require 'minitest/autorun'
require 'mcp'

class MyToolTest < Minitest::Test
  def test_greet_tool
    response = GreetTool.call(name: 'Ruby', server_context: {})
    
    assert_equal 1, response.content.length
    assert_match(/Ruby/, response.content.first[:text])
    refute response.is_error
  end
  
  def test_invalid_input
    response = CalculateTool.call(operation: 'divide', a: 10, b: 0, server_context: {})
    
    assert response.is_error
  end
end
```

### Client Usage

Build MCP clients to connect to servers:

```ruby
require 'mcp'
require 'faraday'

# HTTP transport
http_transport = MCP::Client::HTTP.new(
  url: 'https://api.example.com/mcp',
  headers: { 'Authorization' => "Bearer #{token}" }
)

client = MCP::Client.new(transport: http_transport)

# List tools
tools = client.tools
tools.each do |tool|
  puts "Tool: #{tool.name}"
  puts "Description: #{tool.description}"
end

# Call a tool
response = client.call_tool(
  tool: tools.first,
  arguments: { message: 'Hello, world!' }
)
```

### Best Practices

1. **Use classes for complex tools** - Better organization and testability
2. **Define input/output schemas** - Ensure type safety and validation
3. **Add annotations** - Help clients understand tool behavior
4. **Include structured content** - Provide both text and structured data
5. **Use server_context** - Pass authentication and request context
6. **Configure exception reporting** - Monitor errors in production
7. **Implement instrumentation** - Track performance metrics
8. **Send notifications** - Keep clients updated on changes
9. **Validate inputs** - Check parameters before processing
10. **Follow Ruby conventions** - Use snake_case, proper indentation

### Common Patterns

#### Authenticated Tool

```ruby
class AuthenticatedTool < MCP::Tool
  def self.call(**args, server_context:)
    user_id = server_context[:user_id]
    raise 'Unauthorized' unless user_id
    
    # Process authenticated request
    MCP::Tool::Response.new([{ type: 'text', text: 'Success' }])
  end
end
```

#### Paginated Resource

```ruby
server.resources_read_handler do |params|
  uri = params[:uri]
  page = params[:page] || 1
  
  data = fetch_paginated_data(page)
  
  [{
    uri: uri,
    mimeType: 'application/json',
    text: data.to_json
  }]
end
```

#### Dynamic Prompt

```ruby
class DynamicPrompt < MCP::Prompt
  def self.template(args, server_context:)
    user_id = server_context[:user_id]
    user_data = User.find(user_id)
    
    MCP::Prompt::Result.new(
      description: "Personalized prompt for #{user_data.name}",
      messages: generate_messages_for(user_data)
    )
  end
end
```
