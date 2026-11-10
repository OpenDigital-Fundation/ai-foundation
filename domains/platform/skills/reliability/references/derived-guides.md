# Reliability and observability — derived guides

Part of `platform:reliability`.

## Performance Optimizer

<!-- source: davila7/claude-code-templates cli-tool/components/skills/productivity/performance-optimizer/SKILL.md#common-optimizations -->

### Common Optimizations

#### Database Queries

**Problem: N+1 Queries**
```javascript
// Bad: N+1 queries
const users = await db.users.find();
for (const user of users) {
  user.posts = await db.posts.find({ userId: user.id }); // N queries
}

// Good: Single query with JOIN
const users = await db.users.find()
  .populate('posts'); // 1 query
```

**Problem: Missing Index**
```sql
-- Check slow query
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- Shows: Seq Scan (bad)

-- Add index
CREATE INDEX idx_users_email ON users(email);

-- Check again
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- Shows: Index Scan (good)
```

**Problem: SELECT ***
```javascript
// Bad: Fetches all columns
const users = await db.query('SELECT * FROM users');

// Good: Only needed columns
const users = await db.query('SELECT id, name, email FROM users');
```

**Problem: No Pagination**
```javascript
// Bad: Returns all records
const users = await db.users.find();

// Good: Paginated
const users = await db.users.find()
  .limit(20)
  .skip((page - 1) * 20);
```

#### API Performance

**Problem: No Caching**
```javascript
// Bad: Hits database every time
app.get('/api/stats', async (req, res) => {
  const stats = await db.stats.calculate(); // Slow
  res.json(stats);
});

// Good: Cache for 5 minutes
const cache = new Map();
app.get('/api/stats', async (req, res) => {
  const cached = cache.get('stats');
  if (cached && Date.now() - cached.time < 300000) {
    return res.json(cached.data);
  }
  
  const stats = await db.stats.calculate();
  cache.set('stats', { data: stats, time: Date.now() });
  res.json(stats);
});
```

**Problem: Sequential Operations**
```javascript
// Bad: Sequential (slow)
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);
// Total: 300ms + 200ms + 150ms = 650ms

// Good: Parallel (fast)
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);
// Total: max(300ms, 200ms, 150ms) = 300ms
```

**Problem: Large Payloads**
```javascript
// Bad: Returns everything
res.json(users); // 5MB response

// Good: Only needed fields
res.json(users.map(u => ({
  id: u.id,
  name: u.name,
  email: u.email
}))); // 500KB response
```

#### Frontend Performance

**Problem: Unnecessary Re-renders**
```javascript
// Bad: Re-renders on every parent update
function UserList({ users }) {
  return users.map(user => <UserCard user={user} />);
}

// Good: Memoized
const UserCard = React.memo(({ user }) => {
  return <div>{user.name}</div>;
});
```

**Problem: Large Bundle**
```javascript
// Bad: Imports entire library
import _ from 'lodash'; // 70KB

// Good: Import only what you need
import debounce from 'lodash/debounce'; // 2KB
```

**Problem: No Code Splitting**
```javascript
// Bad: Everything in one bundle
import HeavyComponent from './HeavyComponent';

// Good: Lazy load
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));
```

**Problem: Unoptimized Images**
```html
<!-- Bad: Large image -->
<img src="photo.jpg" /> <!-- 5MB -->

<!-- Good: Optimized and responsive -->
<img 
  src="photo-small.webp" 
  srcset="photo-small.webp 400w, photo-large.webp 800w"
  loading="lazy"
  width="400"
  height="300"
/> <!-- 50KB -->
```

#### Algorithm Optimization

**Problem: Inefficient Algorithm**
```javascript
// Bad: O(n²) - nested loops
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) duplicates.push(arr[i]);
    }
  }
  return duplicates;
}

// Good: O(n) - single pass with Set
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of arr) {
    if (seen.has(item)) duplicates.add(item);
    seen.add(item);
  }
  return Array.from(duplicates);
}
```

**Problem: Repeated Calculations**
```javascript
// Bad: Calculates every time
function getTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
// Called 100 times in render

// Good: Memoized
const getTotal = useMemo(() => {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}, [items]);
```

#### Memory Optimization

**Problem: Memory Leak**
```javascript
// Bad: Event listener not cleaned up
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  // Memory leak!
}, []);

// Good: Cleanup
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

**Problem: Large Data in Memory**
```javascript
// Bad: Loads entire file into memory
const data = fs.readFileSync('huge-file.txt'); // 1GB

// Good: Stream it
const stream = fs.createReadStream('huge-file.txt');
stream.on('data', chunk => process(chunk));
```

## Core Web Vitals optimization

<!-- source: davila7/claude-code-templates cli-tool/components/skills/development/core-web-vitals/SKILL.md#inp-interaction-to-next-paint,cls-cumulative-layout-shift -->

### INP: Interaction to Next Paint

INP measures responsiveness across ALL interactions (clicks, taps, key presses) during a page visit. It reports the worst interaction (at 98th percentile for high-traffic pages).

#### INP breakdown

Total INP = **Input Delay** + **Processing Time** + **Presentation Delay**

| Phase | Target | Optimization |
|-------|--------|--------------|
| Input Delay | < 50ms | Reduce main thread blocking |
| Processing | < 100ms | Optimize event handlers |
| Presentation | < 50ms | Minimize rendering work |

#### Common INP issues

**1. Long tasks blocking main thread**
```javascript
// ❌ Long synchronous task
function processLargeArray(items) {
  items.forEach(item => expensiveOperation(item));
}

// ✅ Break into chunks with yielding
async function processLargeArray(items) {
  const CHUNK_SIZE = 100;
  for (let i = 0; i < items.length; i += CHUNK_SIZE) {
    const chunk = items.slice(i, i + CHUNK_SIZE);
    chunk.forEach(item => expensiveOperation(item));
    
    // Yield to main thread
    await new Promise(r => setTimeout(r, 0));
    // Or use scheduler.yield() when available
  }
}
```

**2. Heavy event handlers**
```javascript
// ❌ All work in handler
button.addEventListener('click', () => {
  // Heavy computation
  const result = calculateComplexThing();
  // DOM updates
  updateUI(result);
  // Analytics
  trackEvent('click');
});

// ✅ Prioritize visual feedback
button.addEventListener('click', () => {
  // Immediate visual feedback
  button.classList.add('loading');
  
  // Defer non-critical work
  requestAnimationFrame(() => {
    const result = calculateComplexThing();
    updateUI(result);
  });
  
  // Use requestIdleCallback for analytics
  requestIdleCallback(() => trackEvent('click'));
});
```

**3. Third-party scripts**
```javascript
// ❌ Eagerly loaded, blocks interactions
<script src="https://heavy-widget.com/widget.js"></script>

// ✅ Lazy loaded on interaction or visibility
const loadWidget = () => {
  import('https://heavy-widget.com/widget.js')
    .then(widget => widget.init());
};
button.addEventListener('click', loadWidget, { once: true });
```

**4. Excessive re-renders (React/Vue)**
```javascript
// ❌ Re-renders entire tree
function App() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <Counter count={count} />
      <ExpensiveComponent /> {/* Re-renders on every count change */}
    </div>
  );
}

// ✅ Memoized expensive components
const MemoizedExpensive = React.memo(ExpensiveComponent);

function App() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <Counter count={count} />
      <MemoizedExpensive />
    </div>
  );
}
```

#### INP optimization checklist

```markdown
- [ ] No tasks > 50ms on main thread
- [ ] Event handlers complete quickly (< 100ms)
- [ ] Visual feedback provided immediately
- [ ] Heavy work deferred with requestIdleCallback
- [ ] Third-party scripts don't block interactions
- [ ] Debounced input handlers where appropriate
- [ ] Web Workers for CPU-intensive operations
```

#### INP debugging
```javascript
// Identify slow interactions
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 200) {
      console.warn('Slow interaction:', {
        type: entry.name,
        duration: entry.duration,
        processingStart: entry.processingStart,
        processingEnd: entry.processingEnd,
        target: entry.target
      });
    }
  }
}).observe({ type: 'event', buffered: true, durationThreshold: 16 });
```

---

### CLS: Cumulative Layout Shift

CLS measures unexpected layout shifts. A shift occurs when a visible element changes position between frames without user interaction.

**CLS Formula:** `impact fraction × distance fraction`

#### Common CLS causes

**1. Images without dimensions**
```html
<!-- ❌ Causes layout shift when loaded -->
<img src="photo.jpg" alt="Photo">

<!-- ✅ Space reserved -->
<img src="photo.jpg" alt="Photo" width="800" height="600">

<!-- ✅ Or use aspect-ratio -->
<img src="photo.jpg" alt="Photo" style="aspect-ratio: 4/3; width: 100%;">
```

**2. Ads, embeds, and iframes**
```html
<!-- ❌ Unknown size until loaded -->
<iframe src="https://ad-network.com/ad"></iframe>

<!-- ✅ Reserve space with min-height -->
<div style="min-height: 250px;">
  <iframe src="https://ad-network.com/ad" height="250"></iframe>
</div>

<!-- ✅ Or use aspect-ratio container -->
<div style="aspect-ratio: 16/9;">
  <iframe src="https://youtube.com/embed/..." 
          style="width: 100%; height: 100%;"></iframe>
</div>
```

**3. Dynamically injected content**
```javascript
// ❌ Inserts content above viewport
notifications.prepend(newNotification);

// ✅ Insert below viewport or use transform
const insertBelow = viewport.bottom < newNotification.top;
if (insertBelow) {
  notifications.prepend(newNotification);
} else {
  // Animate in without shifting
  newNotification.style.transform = 'translateY(-100%)';
  notifications.prepend(newNotification);
  requestAnimationFrame(() => {
    newNotification.style.transform = '';
  });
}
```

**4. Web fonts causing FOUT**
```css
/* ❌ Font swap shifts text */
@font-face {
  font-family: 'Custom';
  src: url('custom.woff2') format('woff2');
}

/* ✅ Optional font (no shift if slow) */
@font-face {
  font-family: 'Custom';
  src: url('custom.woff2') format('woff2');
  font-display: optional;
}

/* ✅ Or match fallback metrics */
@font-face {
  font-family: 'Custom';
  src: url('custom.woff2') format('woff2');
  font-display: swap;
  size-adjust: 105%; /* Match fallback size */
  ascent-override: 95%;
  descent-override: 20%;
}
```

**5. Animations triggering layout**
```css
/* ❌ Animates layout properties */
.animate {
  transition: height 0.3s, width 0.3s;
}

/* ✅ Use transform instead */
.animate {
  transition: transform 0.3s;
}
.animate.expanded {
  transform: scale(1.2);
}
```

#### CLS optimization checklist

```markdown
- [ ] All images have width/height or aspect-ratio
- [ ] All videos/embeds have reserved space
- [ ] Ads have min-height containers
- [ ] Fonts use font-display: optional or matched metrics
- [ ] Dynamic content inserted below viewport
- [ ] Animations use transform/opacity only
- [ ] No content injected above existing content
```

#### CLS debugging
```javascript
// Track layout shifts
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) {
      console.log('Layout shift:', entry.value);
      entry.sources?.forEach(source => {
        console.log('  Shifted element:', source.node);
        console.log('  Previous rect:', source.previousRect);
        console.log('  Current rect:', source.currentRect);
      });
    }
  }
}).observe({ type: 'layout-shift', buffered: true });
```

---

## react-performance-optimizer

<!-- source: davila7/claude-code-templates cli-tool/components/agents/web-tools/react-performance-optimizer.md#advanced-react-performance-patterns -->

### Advanced React Performance Patterns

#### Concurrent React Features
```typescript
// React 18 Concurrent Features
import { startTransition, useDeferredValue, useTransition } from 'react';

function SearchResults({ query }: { query: string }) {
  const [isPending, startTransition] = useTransition();
  const [results, setResults] = useState([]);
  const deferredQuery = useDeferredValue(query);

  // Heavy search operation with transition
  const searchHandler = (newQuery: string) => {
    startTransition(() => {
      // This won't block the UI
      setResults(performExpensiveSearch(newQuery));
    });
  };

  return (
    <div>
      <SearchInput onChange={searchHandler} />
      {isPending && <SearchSpinner />}
      <ResultsList 
        results={results} 
        query={deferredQuery} // Uses deferred value
      />
    </div>
  );
}
```

#### Advanced Memoization Strategies
```typescript
// Deep comparison memoization
import { memo, useMemo } from 'react';
import { isEqual } from 'lodash';

const ExpensiveComponent = memo(({ data, config }) => {
  // Memoize expensive computations
  const processedData = useMemo(() => {
    return data
      .filter(item => item.active)
      .map(item => processComplexCalculation(item, config))
      .sort((a, b) => b.priority - a.priority);
  }, [data, config]);

  const chartConfig = useMemo(() => ({
    responsive: true,
    plugins: {
      legend: { display: config.showLegend },
      tooltip: { enabled: config.showTooltips }
    }
  }), [config.showLegend, config.showTooltips]);

  return <Chart data={processedData} options={chartConfig} />;
}, (prevProps, nextProps) => {
  // Custom comparison function for complex objects
  return isEqual(prevProps.data, nextProps.data) && 
         isEqual(prevProps.config, nextProps.config);
});
```

#### Virtualization for Large Lists
```typescript
// React Window for performance
import { FixedSizeList as List } from 'react-window';

const VirtualizedList = ({ items }: { items: any[] }) => {
  const Row = ({ index, style }: { index: number; style: any }) => (
    <div style={style}>
      <ItemComponent item={items[index]} />
    </div>
  );

  return (
    <List
      height={400}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </List>
  );
};

// Intersection Observer for infinite scrolling
const useInfiniteScroll = (callback: () => void) => {
  const observer = useRef<IntersectionObserver>();
  
  const lastElementRef = useCallback((node: HTMLDivElement) => {
    if (observer.current) observer.current.disconnect();
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) callback();
    });
    if (node) observer.current.observe(node);
  }, [callback]);

  return lastElementRef;
};
```

## Monitoring Expert

<!-- source: Jeffallan/claude-skills skills/monitoring-expert/SKILL.md#quick-start-examples -->

### Quick-Start Examples

#### Structured Logging (Node.js / Pino)
```js
import pino from 'pino';

const logger = pino({ level: 'info' });

// Good — structured fields, includes correlation ID
logger.info({ requestId: req.id, userId: req.user.id, durationMs: elapsed }, 'order.created');

// Bad — string interpolation, no correlation
console.log(`Order created for user ${userId}`);
```

#### Prometheus Metrics (Node.js)
```js
import { Counter, Histogram, register } from 'prom-client';

const httpRequests = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status'],
});

const httpDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request latency',
  labelNames: ['method', 'route'],
  buckets: [0.05, 0.1, 0.3, 0.5, 1, 2, 5],
});

// Instrument a route
app.use((req, res, next) => {
  const end = httpDuration.startTimer({ method: req.method, route: req.path });
  res.on('finish', () => {
    httpRequests.inc({ method: req.method, route: req.path, status: res.statusCode });
    end();
  });
  next();
});

// Expose scrape endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

#### OpenTelemetry Tracing (Node.js)
```js
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { trace } from '@opentelemetry/api';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({ url: 'http://jaeger:4318/v1/traces' }),
});
sdk.start();

// Manual span around a critical operation
const tracer = trace.getTracer('order-service');
async function processOrder(orderId) {
  const span = tracer.startSpan('order.process');
  span.setAttribute('order.id', orderId);
  try {
    const result = await db.saveOrder(orderId);
    span.setStatus({ code: SpanStatusCode.OK });
    return result;
  } catch (err) {
    span.recordException(err);
    span.setStatus({ code: SpanStatusCode.ERROR });
    throw err;
  } finally {
    span.end();
  }
}
```

#### Prometheus Alerting Rule
```yaml
groups:
  - name: api.rules
    rules:
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m])
          / rate(http_requests_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 5% on {{ $labels.route }}"
```

#### k6 Load Test
```js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // ramp up
    { duration: '5m', target: 50 },   // sustained load
    { duration: '1m', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95th percentile < 500 ms
    http_req_failed:   ['rate<0.01'],  // error rate < 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/orders');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```
