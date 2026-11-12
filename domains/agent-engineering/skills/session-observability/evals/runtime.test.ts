import { describe, expect, test, mock } from 'bun:test'
import { costOf, kindsOf, ledgerOf, spendsOf, usdOf } from '../assets/session-lens/hooks/digest/cost'
import { scan, tally, emptyRun } from '../assets/session-lens/hooks/digest/record'
import { usesOf } from '../assets/session-lens/hooks/digest/uses'
import { effortStudyOf } from '../assets/session-lens/hooks/digest/effort'
import { resolve, dirname } from 'node:path'
import { readdirSync, readFileSync, existsSync } from 'node:fs'

// Synthetic data only. The host interface is a stub; no Claude process, network or personal records.
// Bun inserts this renderer import for test-time TSX loading; the Claude host has its own renderer.
mock.module('react/jsx-dev-runtime', () => ({ jsxDEV: () => null, Fragment: 'synthetic-fragment' }))
mock.module('react/jsx-runtime', () => ({ jsx: () => null, jsxs: () => null, Fragment: 'synthetic-fragment' }))
mock.module('claude-code', () => ({
  atom: (_key: unknown, initial: unknown) => ({ initial }),
  read: async () => { throw new Error('synthetic observer failure') },
  update: async () => { throw new Error('synthetic observer failure') },
}))

describe('usage arithmetic on synthetic records', () => {
  test('cache write durations are disjoint and sum to total writes', () => {
    expect(kindsOf({ i: 4, o: 2, cr: 3, cw: 10, c1: 6 })).toEqual({ i: 4, o: 2, cr: 3, w5: 4, w1: 6 })
    expect(kindsOf({ i: 0, o: 0, cr: 0, cw: 10, c1: 20 }).w5).toBe(0)
  })
  test('dated standard Fable 5.2 rate cannot inherit Fable 5', () => {
    expect(usdOf({ md: 'claude-fable-5-2', i: 1_000_000, o: 0, cr: 0, cw: 0 })).toBe(8)
    expect(usdOf({ md: 'claude-mythos-5-2', i: 0, o: 1_000_000, cr: 0, cw: 0 })).toBe(40)
  })
  test('Sonnet 5.5 cache reads use its own dated rate', () => {
    expect(costOf({ md: 'claude-sonnet-5-5', i: 0, o: 0, cr: 1_000_000, cw: 0 })?.cr).toBeCloseTo(0.1)
  })
  test('unknown minor/provider models remain unpriced, dated known IDs work', () => {
    for (const md of ['claude-fable-5-9', 'claude-sonnet-5-6', 'unlisted-model'])
      expect(usdOf({ md, i: 100, o: 100, cr: 0, cw: 0 })).toBeUndefined()
    expect(usdOf({ md: 'claude-sonnet-4-20250514', i: 1_000_000, o: 0, cr: 0, cw: 0 })).toBe(3)
  })
  test('cumulative process readings use deltas instead of summing snapshots', () => {
    const spends = spendsOf([{ start: 0, at: 10, usd: 2 }, { start: 0, at: 20, usd: 5 }])
    expect(spends.map(s => s.usd)).toEqual([2, 3])
    expect(ledgerOf(spends, []).total).toBe(5)
  })
  test('separate measurement coverage and an estimated unmeasured request', () => {
    const result = ledgerOf([{ start: 0, end: 10, usd: 2 }], [{ ts: 5, usd: 1, md: 'a' }, { ts: 20, usd: 1, md: 'a' }])
    expect(result.snapped).toBe(2); expect(result.estimated).toBe(1.5)
    expect(result.pm).toBe(0.5); expect(result.isFull).toBe(false)
  })
  test('repeated assistant fragments count one request and one call per use ID', () => {
    const row = { t: 'assistant' as const, id: 'same-request', ts: '2026-11-12T00:00:00Z', md: 'unlisted-model', u: { i: 12, o: 4, cr: 0, cw: 0 }, c: [{ k: 'use', id: 'same-use', name: 'Bash', n: 4 }] }
    const result = scan([row, row])
    expect(result.steps).toHaveLength(1);expect(result.uses.size).toBe(1)
    expect(result.calls[0]?.tools).toBe(1);expect(result.chat.toolCount).toBe(1)
  })
  test('Skill/tool/MCP rows preserve identifiers and distinct categories', () => {
    const calls = new Map([
      ['s', { k: 'use', name: 'Skill', sk: 'education:learn', n: 8 }],
      ['b', { k: 'use', name: 'Bash', n: 12 }],
      ['m', { k: 'use', name: 'mcp__server__lookup', n: 16 }],
    ])
    const t = tally(calls, new Map())
    expect(t.skills).toEqual({ 'education:learn': 1 });expect(t.mcp.server?.tools.lookup?.calls).toBe(1)
    const rows=usesOf('main', { ...emptyRun(), tools: t.tools, skills: { 'education:learn': { count: 1, tokens: 0 } } }, true, { known: {}, listed: [], who: {}, kids: [], log: [], since: '' })
    expect(rows.skillRows[0]?.name).toBe('education:learn');expect(rows.skillRows[0]?.back).toBeUndefined()
    expect(rows.skillRows[0]?.scope).toBe('?')
  })
  test('small effort samples do not produce a confident comparison', () => {
    const result = effortStudyOf([{ model: 'synthetic', effort: 'low', calls: 1, steps: 1 }, { model: 'synthetic', effort: 'high', calls: 10, steps: 1 }])
    expect(result[0]?.verdict).toBe('few')
  })
})

describe('optional native package integrity', () => {
  const root = resolve(import.meta.dir, '../assets/session-lens')
  test('every local module import resolves and transpiles without loading the host', () => {
    let count=0
    const walk=(folder: string): string[] => readdirSync(folder,{withFileTypes:true}).flatMap(x=>x.isDirectory()?walk(resolve(folder,x.name)):[resolve(folder,x.name)])
    for(const file of walk(root).filter(f=>/\.tsx?$/.test(f)&&!f.endsWith('.d.ts'))){
      const trans=new Bun.Transpiler({loader:file.endsWith('.tsx')?'tsx':'ts'})
      const text=readFileSync(file,'utf8');trans.transformSync(text)
      for(const imp of trans.scanImports(text)){
        if(imp.path.startsWith('.')){
          const base=resolve(dirname(file),imp.path)
          expect([base,base+'.ts',base+'.tsx',base+'.d.ts',resolve(base,'index.ts'),resolve(base,'index.d.ts')].some(existsSync)).toBe(true)
        }else if(imp.path === 'react' || imp.path.startsWith('react/jsx')){
          // Compiler-generated import in this test, not a dependency in the vendored source.
          expect(file.endsWith('.tsx')).toBe(true)
          expect(/from ['\"]react/.test(text)).toBe(false)
        }else expect(imp.path).toBe('claude-code')
      }
      count++
    }
    expect(count).toBeGreaterThan(40)
  })
  test('disabled actions cannot call model, settings helper or transcript copier', async () => {
    const { report, askAutocompactTuning } = await import('../assets/session-lens/hooks/refresh')
    const { linkSession } = await import('../assets/session-lens/hooks/record/transcript')
    const { writeTuning, readTuning } = await import('../assets/session-lens/hooks/record/autocompact')
    const messages: string[]=[]
    const host={ui:{toast:(m:string)=>messages.push(m)}} as never
    await report(host);await askAutocompactTuning(host)
    await expect(linkSession(host)).rejects.toThrow('disabled')
    await expect(writeTuning(host,[],()=>{})).rejects.toThrow('not changed')
    await expect(readTuning(host,false,()=>{})).rejects.toThrow('disabled')
    expect(messages).toHaveLength(2)
  })
  test('observer state failure preserves exactly one downstream call and original error', async () => {
    const { register } = await import('../assets/session-lens/hooks/register')
    const hooks: {event:string,fn:Function}[]=[]
    register(((event:string, ...args:unknown[])=>{hooks.push({event,fn:args.at(-1) as Function});return {catch:()=>{throw new Error('observer must not retry next')}}}) as never)
    for(const event of ['command.run','turn.start','turn.complete','skill.prompt']){
      const h=hooks.find(x=>x.event===event && (event!=='command.run'||x.fn.length===3))!
      let calls=0;const downstream=new Error('synthetic downstream failure')
      await expect(h.fn({}, {command:'other',origin:{kind:'human'},text:'',source:'synthetic',skill:'test'}, async()=>{calls++;throw downstream})).rejects.toBe(downstream)
      expect(calls).toBe(1)
    }
  })
})
