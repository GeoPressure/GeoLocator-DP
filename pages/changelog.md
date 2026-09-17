---
title: Changelog
permalink: /changelog/
---

GeoLocator DP is versioned with Git tags. A data package declares the version it
follows through the package-level
[`$schema`](https://datapackage.org/standard/data-package/#dollar-schema):

```json
{
  "$schema": "https://raw.githubusercontent.com/GeoPressure/GeoLocator-DP/v1.1/geolocator-dp-profile.json"
}
```

[`GeoLocatoR`](https://geopressure.com/GeoLocatoR/) upgrades a package from any
earlier version when it reads one, so an archived package never needs to be
rewritten by hand.

This page collects the [GitHub
releases](https://github.com/GeoPressure/GeoLocator-DP/releases) in one place.

## v1.1

### Resources

- Move the GeoLocator DP table schema URL from `resource.$schema` to
  `resource.schema`. In the Data Package standard, `$schema` is the profile of
  the resource *descriptor* while
  [`schema`](https://datapackage.org/standard/data-resource/#schema) is the
  [Table Schema](https://datapackage.org/standard/table-schema/) describing the
  columns. `schema` accepts either a versioned table schema URL or an inline
  descriptor.
- Require `type` on tabular resources, which must be `table`. It replaces the
  Data Package v1 `profile: "tabular-data-resource"`.
- `$schema` remains optional and, when present, must be
  `https://datapackage.org/profiles/2.0/dataresource.json`.

### Table schemas

- Write [`fieldsMatch`](https://datapackage.org/standard/table-schema/#fieldsMatch)
  as a string rather than an array, as the standard requires. The array form
  came from an error in the published Table Schema profile
  ([frictionlessdata/datapackage#965](https://github.com/frictionlessdata/datapackage/issues/965)),
  fixed in Data Package v2.1.
- Write [`primaryKey`](https://datapackage.org/standard/table-schema/#primaryKey)
  and [`foreignKeys`](https://datapackage.org/standard/table-schema/#foreignKeys)
  fields as arrays of strings, the Data Package v2 spelling.
- Remove the `unique` constraint on `tags.tag_id`, which duplicated the primary
  key.

### Profile

- Select the resource schema with `if`/`then` on the resource `name` rather
  than `oneOf`. The accepted descriptors are unchanged, but a validation error
  now names the property at fault instead of reporting that the whole resource
  matched none of the branches.

### Repository

- Show `primaryKey`, `foreignKeys`, `missingValues` and `fieldsMatch` on each
  table page, and link SKOS terms by identifier rather than by URL.
- Fix a broken SKOS link on `observations.datetime`, and restore `_data`
  symlink for the measurements schema so the website renders the schema the
  standard ships.
- Add `example/datapackage.json` and `example/measurements.csv`.
- Validate the example package, and the spelling of `fieldsMatch` and of the
  keys, in `tests/validate_profile_and_schemas.py`.
- Add this changelog page.

## v1.0

*8 April 2026 — [release](https://github.com/GeoPressure/GeoLocator-DP/releases/tag/v1.0)*

### Major

- Remove all metadata from `datapackage.json`, which becomes a minimal local
  manifest containing only the schema and the list of
  [resources](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/4f2e644503b6f7db7539d78469175ef5f7e69324).
- Rename sensor `pitch` into `mean_acceleration_z`. See
  [#24](https://github.com/GeoPressure/GeoLocator-DP/issues/24).
- Remove `paths.ind`, `paths.interp`, `staps.include`, `edges.s` and `edges.t`
  ([1](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/8ef7ad8cf9e48e82d8396f535536fb8e5b9c119f),
  [2](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/418f7c926fdff4af0a1c5e48d57a50f8a61c95d2)).
- [Drop support for non-deployed tags](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/795ccc4cdd0bf575b39378ca3e63c61247ac2b8e).
- [Review and fix errors in `primaryKey` and `foreignKeys`](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/355585f44e27d36c12e9d55f92a2bd6e0b4008fb).

### Minor

- [Add pattern to `$schema`](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/1f48ca9754f11ffb417158c9e4ea816f3053e4b0).
- [Enforce CSV (or zipped CSV) for the resources](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/acbfbf1cc6372adf9d243f86bc26e013a7f0d59e).
- [Allow for additional resources](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/73ee1cff50e5f817defcc04e39ff665cccaf3746).
- [Update `validate-profile-and-schemas.yml`](https://github.com/GeoPressure/GeoLocator-DP/commit/e5104b4e6dcbe9a2009d71bba5184c5daacc9166).

### Website

- [Update website with curation and overview page](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/b056fe28f37402a5cad76e2c9f5252bf5f7e578a).
- [Add icon to alert](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/c478512f6c50a0580accd7d2e03e2eeb401b1947).
- [Add image background cover for GeoPressureR resources](https://github.com/GeoPressure/GeoLocator-DP/pull/32/commits/dd7782878941883f71fde28a9575eb96e7b5f9d2).
- [Update all URLs to geopressure.org](https://github.com/GeoPressure/GeoLocator-DP/commit/0732e4d257705625a10ee585cced8d5affa40d09).

### Not implemented

- No major changes to `edges.csv`, see
  [#31](https://github.com/GeoPressure/GeoLocator-DP/issues/31).

[Full changelog](https://github.com/GeoPressure/GeoLocator-DP/compare/v0.6...v1.0)

## v0.6

*9 March 2026 — [release](https://github.com/GeoPressure/GeoLocator-DP/releases/tag/v0.6)*

Rather minor edits in preparation for v1.0.

- [Remove `ind` from `pressurepaths`](https://github.com/GeoPressure/GeoLocator-DP/commit/c278695d094ea40e13fea6458a078a7711ea0d1a).

[Full changelog](https://github.com/GeoPressure/GeoLocator-DP/compare/v0.5...v0.6)

## v0.5

*30 January 2026 — [release](https://github.com/GeoPressure/GeoLocator-DP/releases/tag/v0.5)*

- [**Major** fix of missing `type` for `edges`](https://github.com/GeoPressure/GeoLocator-DP/pull/27/commits/60251cd0117856fc7302ce9d3d0abfab81ad0893).
- [Update schema descriptions and reorder `stap_id` in `paths`](https://github.com/GeoPressure/GeoLocator-DP/pull/27/commits/d61bda88f8a733649839c6a781225f50df074c43).
- [Add `Other` to the `identifierType` enum list](https://github.com/GeoPressure/GeoLocator-DP/pull/27/commits/86b3bc39b245edec6e4f6be42bfcbdc6254afdf4).

[Full changelog](https://github.com/GeoPressure/GeoLocator-DP/compare/v0.4...v0.5)

## v0.4

*21 January 2026 — [release](https://github.com/GeoPressure/GeoLocator-DP/releases/tag/v0.4)*

- [Add `datapackage_id` field to the `tags` schema](https://github.com/GeoPressure/GeoLocator-DP/commit/a85af2d8ad9f16297fb5cbb07a448d1c3aab24b2).
- [Allow string or list of string for the `taxonomicName` and `contributorRole` definitions](https://github.com/GeoPressure/GeoLocator-DP/commit/cd9e5144fa756be5c2ec3bf460dd93f93bdca2e0).
- [Make `lat` and `lon` not required, to allow for cases where `include=FALSE`](https://github.com/GeoPressure/GeoLocator-DP/commit/4056a3f4a6d7164b218ec51b8b23b50f3c2a72c8).

[Full changelog](https://github.com/GeoPressure/GeoLocator-DP/compare/v0.3...v0.4)

## v0.3

*1 October 2025 — [release](https://github.com/GeoPressure/GeoLocator-DP/releases/tag/v0.3)*

### Data Package definition

- Fix example and validation of `schema` in `geolocator-dp-profile.json`
  ([1](https://github.com/GeoPressure/GeoLocator-DP/commit/5bbafa9c478375398f98637d2733fd1fc3ec1952),
  [2](https://github.com/GeoPressure/GeoLocator-DP/commit/e2fcef4a1e3653d079d6ddcafacca6a25eef0313)).
- [Remove `embargo` from the required fields list](https://github.com/GeoPressure/GeoLocator-DP/commit/c489984a3c4928d28f52615d2032a17c93d0909e).
- [Update version pattern](https://github.com/GeoPressure/GeoLocator-DP/commit/25b9af8614b045a7c0b8efd1ab266bf9cae727eb).

### Minor

- [Fix tests](https://github.com/GeoPressure/GeoLocator-DP/commit/7f22ddd447c6f992b8f3a2c0fcf79cd123dce896).
- [Fix SKOS links](https://github.com/GeoPressure/GeoLocator-DP/commit/f984d660f50c3930556451aa97c4dc9be8418fbd).
- [Review text with Copilot](https://github.com/GeoPressure/GeoLocator-DP/commit/3ce0b90a46b883b70fe27a272b7e3f19f4f920bf).
- [Add GeoLocatorExplorer](https://github.com/GeoPressure/GeoLocator-DP/commit/09b25749e71b5c785ab9149ab52bfd30994787e2).

### New contributors

- [@PabloCapilla](https://github.com/PabloCapilla) made their
  [first contribution](https://github.com/GeoPressure/GeoLocator-DP/commit/c0b15b4b010b02f2fa9a16f8d4ff74351988e282).

[Full changelog](https://github.com/GeoPressure/GeoLocator-DP/compare/v0.2...v0.3)

## v0.2

*16 January 2025 — [release](https://github.com/GeoPressure/GeoLocator-DP/releases/tag/v0.2)*

### pressurepaths

- New!

### tags

- [Correct typo for `firwmare`](https://github.com/GeoPressure/GeoLocator-DP/commit/90b65c555720a006aa814e91f04dc85209be7df1).

### observations

- `life_stage` → `age_class`
  ([commit](https://github.com/GeoPressure/GeoLocator-DP/commit/4a6d8bcae5d211822799ad4f09e341687d53d321),
  [#13](https://github.com/GeoPressure/GeoLocator-DP/issues/13)).
- Remove `broken_damage` from `device_status`
  ([#14](https://github.com/GeoPressure/GeoLocator-DP/issues/14)).

### measurements

- Add `wet_count` and `conductivity` sensors
  ([commit](https://github.com/GeoPressure/GeoLocator-DP/commit/6720312c0de3e025f98fd24a19d2d7e8061f238b),
  [#12](https://github.com/GeoPressure/GeoLocator-DP/issues/12)).

### Metadata

- Make `manufacturer` and `model` required
  ([commit](https://github.com/GeoPressure/GeoLocator-DP/commit/7e9e85dd0a43716b6d2a43bf2bc7ce4d4f15e40f),
  [#11](https://github.com/GeoPressure/GeoLocator-DP/issues/11)).
- [Rename `citation` into `bibliographicCitation`](https://github.com/GeoPressure/GeoLocator-DP/commit/477f3899194edf2a31b93a1019d654714084eeb4).
- [Refine `contributors` roles](https://github.com/GeoPressure/GeoLocator-DP/commit/9d7cef6aa214f29dd836619cc45eee94cce66703).
- [Add `spatial` and make `reference_location` optional](https://github.com/GeoPressure/GeoLocator-DP/pull/19/commits/2e91036e6bfb718623b4b784e41abf43541c827d).
- [Add `numberTags`](https://github.com/GeoPressure/GeoLocator-DP/pull/19/commits/8e059382e1157fa9a97962f01a3bf05da600f7f7).
- [Remove `homepage`, `image`, `references` and `name`](https://github.com/GeoPressure/GeoLocator-DP/pull/19/commits/db091f74245c1b521d3dbe2a3665452bf4f70c53).
- [Add `computed` properties](https://github.com/GeoPressure/GeoLocator-DP/pull/19/commits/83bddf87668f29bdaee361e3a4c8c6e0cb71acdf).
- Re-order the properties and improve documentation.

### New contributors

- [@peterdesmet](https://github.com/peterdesmet) made their
  [first contribution](https://github.com/GeoPressure/GeoLocator-DP/pull/17).

[Full changelog](https://github.com/GeoPressure/GeoLocator-DP/compare/v0.1...v0.2)

## v0.1

*2 December 2024 — [release](https://github.com/GeoPressure/GeoLocator-DP/releases/tag/v0.1)*

Initial release.

[Full changelog](https://github.com/GeoPressure/GeoLocator-DP/commits/v0.1)
