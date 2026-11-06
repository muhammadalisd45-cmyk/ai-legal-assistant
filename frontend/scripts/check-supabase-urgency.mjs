import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const migration = await readFile(
  resolve(root, "supabase/migrations/004_fix_case_urgency_constraint.sql"),
  "utf8"
);

test("urgency migration replaces the existing constraint", () => {
  assert.match(migration, /drop constraint if exists cases_urgency_check/i);
  assert.match(migration, /add constraint cases_urgency_check/i);
});

test("urgency migration allows all five application values", () => {
  for (const value of ["low", "medium", "high", "critical", "unknown"]) {
    assert.ok(
      migration.includes(`'${value}'`),
      `Missing urgency value: ${value}`
    );
  }
});

test("urgency migration preserves nullable urgency values", () => {
  assert.match(migration, /urgency is null/i);
});
