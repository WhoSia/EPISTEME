#!/usr/bin/env node
/**
 * EPISTEME P77 W43: inspect real official BIA public API metadata-only
 * accession-level snapshot. No image bytes fetched, no LLM intervention.
 *
 * Usage:
 *   node analysis/p77_w43_bia_api_visibility_census.mjs \
 *     evidence/p77_w43_bia_20261109_four_accessions_metadata_census.json
 *
 * The supplied JSON was saved from official public API responses 2026-11-09.
 * Assertions validate that finite sample, NOT its representativeness.
 */
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

export function audit(data) {
  assert.equal(data.observed_date_KST, "2026-11-09");
  const studies = data.study_results;
  const images = data.image_results;
  const positive = "S-BIAD1410";
  assert.equal(studies[positive].total, 1);
  assert.equal(images[positive].total, 16);
  assert.equal(images[positive].entries.length, 16);
  assert.equal(studies[positive].release_date, "2024-10-30");
  const uuids = new Set();
  let nSource = 0, nConverted = 0, nLinked = 0;
  let nConversionTimestamps = 0;
  for (const image of images[positive].entries) {
    assert.equal(image.accession_id, positive);
    assert(!uuids.has(image.uuid), "duplicate image UUID");
    uuids.add(image.uuid);
    assert(image.original_file_reference_uuid.length > 0);
    assert(image.creation_process_uuid);
    const originals = image.representations.filter(r =>
      r.image_format === ".tiff" && r.object_creator === "bia_image_assignment");
    const derived = image.representations.filter(r =>
      r.image_format === ".ome.zarr" && r.object_creator === "bia_image_conversion");
    assert.equal(originals.length, 1);
    assert.equal(derived.length, 1);
    assert(originals[0].file_uri.startsWith("https://www.ebi.ac.uk/biostudies/files/"));
    assert(derived[0].file_uri.includes(".ome.zarr/"));
    nSource += originals.length; nConverted += derived.length;
    nLinked += Number(originals.length > 0 && derived.length > 0);
    nConversionTimestamps += Number(Boolean(image.converted_at));
  }
  const negative = ["S-BIAD570", "S-BIAD1", "EMPIAR-10014"];
  for (const id of negative) {
    assert.equal(studies[id].total, 1, "study must be visible");
    assert.equal(images[id].total, 0, "image search should have no results");
    assert.equal(images[id].entries.length, 0);
  }
  assert.equal(nSource, 16);
  assert.equal(nConverted, 16);
  assert.equal(nLinked, 16);
  assert.equal(nConversionTimestamps, 0);
  return {
    study_accessions_tested: Object.keys(studies).length,
    accession_with_visible_images: positive,
    image_search_hits_in_positive_accession: 16,
    source_tiff_representations: nSource,
    derived_omezarr_representations: nConverted,
    images_with_both_formats: nLinked,
    study_visible_but_image_search_empty: negative,
    conversion_timestamp_fields_in_saved_metadata: nConversionTimestamps,
    inference: "Conditional on being visible in the API only; NO population conversion rate",
    causal_inference: "NO-GO: no assigned AI converter, actual lab standard choice or independent H0/H1 test"
  };
}

if (process.argv[1] && process.argv[1].endsWith("p77_w43_bia_api_visibility_census.mjs")) {
  assert.equal(process.argv.length, 3, "provide metadata snapshot JSON path");
  const result = audit(JSON.parse(readFileSync(process.argv[2], "utf8")));
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}
