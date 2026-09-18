# GeoLocator DP

GeoLocator DP is a Data Package profile for geolocator data (raw measurements, field observations, and optional GeoPressureR trajectory outputs).

## Documentation

- Website: https://geopressure.org/GeoLocator-DP/
- GeoLocator Manual: https://geopressure.com/GeoPressureManual/geolocator-intro.html
- GeoLocatoR package: https://geopressure.com/GeoLocatoR/

## Repository Contents

- `geolocator-dp-profile.json`: GeoLocator DP package profile
- `*-table-schema.json`: table schemas for core and GeoPressureR resources
- `pages/`: website pages rendered by Jekyll
- `example/`: example CSV resources
- `tests/`: validation tests

## Local Development

This site uses the GitHub Pages Jekyll environment, which currently runs on
Ruby 3.3.4. The project includes a `.ruby-version` file for `chruby` and other
Ruby version managers. Confirm that `ruby --version` reports Ruby 3.3.4 before
installing dependencies.

Install Ruby dependencies:

```bash
bundle install
```

Run the website locally with live reload:

```bash
bundle exec jekyll serve --livereload --incremental
```

Create a production-style build:

```bash
JEKYLL_ENV=production bundle exec jekyll build
```

Run validation tests:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r tests/requirements.txt
python tests/validate_profile_and_schemas.py
```
