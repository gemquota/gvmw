// D-044 UNDO / REDO for Chaos Multiplex iterates.
//
// Each entry is a captureGeneration() record (multiplex.js): full particle
// state of every shard plus the run bookkeeping. Entries are large (about
// live particles × 400 B + a few KB per shard: ≈ 20 MB for 20 sims × 2,500),
// so the stack is bounded by bytes as well as by count.

export const UNDO_MAX_STEPS = 20;
/** 256 MB: ≥ 12 steps at 20 sims × 2,500 live particles (≈ 20 MB / step). */
export const UNDO_BYTE_BUDGET = 256 * 1024 * 1024;

export function createGenerationStack({ maxSteps = UNDO_MAX_STEPS, budgetBytes = UNDO_BYTE_BUDGET } = {}) {
  const undo = [];
  const redo = [];
  const bytesOf = (list) => list.reduce((a, g) => a + (g.bytes || 0), 0);
  const trim = () => {
    // Drop the oldest undo steps first; redo entries are dropped next. The
    // newest undo step always stays, whatever its size.
    while (undo.length > maxSteps || (bytesOf(undo) + bytesOf(redo) > budgetBytes && (undo.length > 1 || redo.length))) {
      if (undo.length > 1) undo.shift();
      else if (redo.length) redo.shift();
      else break;
    }
  };
  return {
    /** A new action (iterate / revert): push the pre-action state, clear redo. */
    push(gen) {
      if (!gen) return;
      undo.push(gen);
      redo.length = 0;
      trim();
    },
    /** Step back: `current` (captured now) moves to redo; returns the target. */
    undo(current) {
      if (!undo.length) return null;
      const target = undo.pop();
      if (current) redo.push(current);
      trim();
      return target;
    },
    redo(current) {
      if (!redo.length) return null;
      const target = redo.pop();
      if (current) undo.push(current);
      trim();
      return target;
    },
    clear() { undo.length = 0; redo.length = 0; },
    get canUndo() { return undo.length > 0; },
    get canRedo() { return redo.length > 0; },
    stats() {
      return { undo: undo.length, redo: redo.length, bytes: bytesOf(undo) + bytesOf(redo), budgetBytes, maxSteps };
    },
  };
}
