# Database design — derived guides

Part of `data:database-design`.

## Example: Event-driven microservices architecture

<!-- source: davila7/claude-code-templates cli-tool/components/agents/database/database-architect.md#architecture-decision-framework,scalability-architecture-patterns -->

### Scalability Architecture Patterns

#### 1. Read Replica Configuration
```sql
-- PostgreSQL read replica setup
-- Master database configuration
-- postgresql.conf
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 32
archive_mode = on
archive_command = 'test ! -f /var/lib/postgresql/archive/%f && cp %p /var/lib/postgresql/archive/%f'

-- Create replication user (set REPLICATION_PASSWORD via environment variable or secrets manager)
CREATE USER replicator REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD '${REPLICATION_PASSWORD}';

-- Read replica configuration
-- recovery.conf
standby_mode = 'on'
-- Set REPLICATION_PASSWORD via environment variable or secrets manager; never hardcode credentials
primary_conninfo = 'host=master.db.example.com port=5432 user=replicator password=${REPLICATION_PASSWORD}'
restore_command = 'cp /var/lib/postgresql/archive/%f %p'
```

#### 2. Horizontal Sharding Strategy
```python
# Application-level sharding implementation

class ShardManager:
    def __init__(self, shard_config):
        self.shards = {}
        for shard_id, config in shard_config.items():
            self.shards[shard_id] = DatabaseConnection(config)
    
    def get_shard_for_customer(self, customer_id):
        """
        Consistent hashing for customer data distribution
        """
        hash_value = hashlib.md5(str(customer_id).encode()).hexdigest()
        shard_number = int(hash_value[:8], 16) % len(self.shards)
        return f"shard_{shard_number}"
    
    async def get_customer_orders(self, customer_id):
        """
        Retrieve customer orders from appropriate shard
        """
        shard_key = self.get_shard_for_customer(customer_id)
        shard_db = self.shards[shard_key]
        
        return await shard_db.fetch_all("""
            SELECT * FROM orders 
            WHERE customer_id = %(customer_id)s 
            ORDER BY created_at DESC
        """, {'customer_id': customer_id})
    
    async def cross_shard_analytics(self, query_template, params):
        """
        Execute analytics queries across all shards
        """
        results = []
        
        # Execute query on all shards in parallel
        tasks = []
        for shard_key, shard_db in self.shards.items():
            task = shard_db.fetch_all(query_template, params)
            tasks.append(task)
        
        shard_results = await asyncio.gather(*tasks)
        
        # Aggregate results from all shards
        for shard_result in shard_results:
            results.extend(shard_result)
        
        return results
```

### Architecture Decision Framework

#### Database Technology Selection Matrix
```python
def recommend_database_technology(requirements):
    """
    Database technology recommendation based on requirements
    """
    recommendations = {
        'relational': {
            'use_cases': ['ACID transactions', 'complex relationships', 'reporting'],
            'technologies': {
                'PostgreSQL': 'Best for complex queries, JSON support, extensions',
                'MySQL': 'High performance, wide ecosystem, simple setup',
                'SQL Server': 'Enterprise features, Windows integration, BI tools'
            }
        },
        'document': {
            'use_cases': ['flexible schema', 'rapid development', 'JSON documents'],
            'technologies': {
                'MongoDB': 'Rich query language, horizontal scaling, aggregation',
                'CouchDB': 'Eventual consistency, offline-first, HTTP API',
                'Amazon DocumentDB': 'Managed MongoDB-compatible, AWS integration'
            }
        },
        'key_value': {
            'use_cases': ['caching', 'session storage', 'real-time features'],
            'technologies': {
                'Redis': 'In-memory, data structures, pub/sub, clustering',
                'Amazon DynamoDB': 'Managed, serverless, predictable performance',
                'Cassandra': 'Wide-column, high availability, linear scalability'
            }
        },
        'search': {
            'use_cases': ['full-text search', 'analytics', 'log analysis'],
            'technologies': {
                'Elasticsearch': 'Full-text search, analytics, REST API',
                'Apache Solr': 'Enterprise search, faceting, highlighting',
                'Amazon CloudSearch': 'Managed search, auto-scaling, simple setup'
            }
        },
        'time_series': {
            'use_cases': ['metrics', 'IoT data', 'monitoring', 'analytics'],
            'technologies': {
                'InfluxDB': 'Purpose-built for time series, SQL-like queries',
                'TimescaleDB': 'PostgreSQL extension, SQL compatibility',
                'Amazon Timestream': 'Managed, serverless, built-in analytics'
            }
        },
        'vector': {
            'use_cases': ['semantic search', 'RAG pipelines', 'embeddings', 'AI agent memory'],
            'technologies': {
                'pgvector': 'PostgreSQL extension, ANN search, zero infrastructure overhead',
                'Pinecone': 'Managed vector DB, real-time upserts, metadata filtering',
                'Qdrant': 'Open-source, payload filtering, on-premise or cloud',
                'Weaviate': 'Hybrid BM25+vector search, GraphQL API, multi-modal'
            }
        },
        'graph': {
            'use_cases': ['fraud detection', 'social networks', 'knowledge graphs', 'recommendation engines'],
            'technologies': {
                'Neo4j': 'Mature Cypher query language, ACID, rich ecosystem',
                'Amazon Neptune': 'Managed, supports Gremlin and SPARQL, AWS integration',
                'ArangoDB': 'Multi-model (graph + document + key-value), AQL'
            }
        },
        'serverless_relational': {
            'use_cases': ['serverless apps', 'branch-per-PR workflows', 'autoscaling to zero', 'edge deployments'],
            'technologies': {
                'Neon': 'Serverless PostgreSQL, database branching, autoscale to zero',
                'PlanetScale': 'Serverless MySQL, schema branching, non-blocking migrations',
                'Turso': 'SQLite at the edge, per-tenant databases, sub-millisecond latency'
            }
        }
    }
    
    # Analyze requirements and return recommendations
    recommended_stack = []
    
    for requirement in requirements:
        for category, info in recommendations.items():
            if requirement in info['use_cases']:
                recommended_stack.append({
                    'category': category,
                    'requirement': requirement,
                    'options': info['technologies']
                })
    
    return recommended_stack
```

## Redis optimization techniques

<!-- source: davila7/claude-code-templates cli-tool/components/agents/database/nosql-specialist.md#performance-optimization-strategies -->

### Performance Optimization Strategies

#### MongoDB Performance Tuning
```javascript
// Performance optimization techniques

// 1. Efficient indexing strategy
db.users.createIndex(
    { "status": 1, "lastLoginDate": -1, "totalSpent": -1 },
    { 
        name: "user_analytics_idx",
        background: true,
        partialFilterExpression: { "status": "active" }
    }
);

// 2. Aggregation pipeline optimization
db.orders.aggregate([
    // Move $match as early as possible
    { $match: { createdAt: { $gte: ISODate("2024-01-01") } } },
    
    // Use $project to reduce document size early
    { $project: { customerId: 1, total: 1, items: 1 } },
    
    // Optimize grouping operations
    { $group: { _id: "$customerId", totalSpent: { $sum: "$total" } } }
], { allowDiskUse: true });

// 3. Connection pooling optimization
const mongoClient = new MongoClient(uri, {
    maxPoolSize: 50,
    minPoolSize: 5,
    maxIdleTimeMS: 30000,
    serverSelectionTimeoutMS: 5000,
    socketTimeoutMS: 45000,
    bufferMaxEntries: 0,
    useNewUrlParser: true,
    useUnifiedTopology: true
});
```

#### Redis Performance Patterns
```python
# Redis optimization techniques

# 1. Pipeline operations to reduce network round trips
pipe = redis_client.pipeline()
for i in range(1000):
    pipe.set(f"key:{i}", f"value:{i}")
    pipe.expire(f"key:{i}", 3600)
pipe.execute()

# 2. Use appropriate data structures
# Instead of individual keys, use hashes for related data
# Bad: Multiple keys
redis_client.set("user:123:name", "John")
redis_client.set("user:123:email", "john@example.com")

# Good: Single hash
redis_client.hmset("user:123", {
    "name": "John",
    "email": "john@example.com"
})

# 3. Memory optimization with compression
import pickle
import zlib

def compress_and_store(key, data, ttl=3600):
    """Store data with compression for memory efficiency"""
    compressed_data = zlib.compress(pickle.dumps(data))
    redis_client.setex(key, ttl, compressed_data)

def retrieve_and_decompress(key):
    """Retrieve and decompress data"""
    compressed_data = redis_client.get(key)
    if compressed_data:
        return pickle.loads(zlib.decompress(compressed_data))
    return None
```
