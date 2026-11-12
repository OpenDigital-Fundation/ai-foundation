// Modified by OpenDigital: settings mutation and log-scanning helpers are not shipped.
import type { EngineInterface } from 'claude-code'
import type { Tuning, TuningStage } from '../digest/autocompact'
export async function readTuning(_$: EngineInterface, _fresh: boolean, _stage: (s: TuningStage) => void): Promise<Tuning> {
  throw new Error('Autocompact tuning is disabled in this measurement package.')
}
export async function writeTuning(_$: EngineInterface, _args: string[], _stage: (s: TuningStage) => void): Promise<string> {
  throw new Error('Autocompact settings are not changed by this measurement package.')
}
