---
title: GeoLocator DP
background: /assets/home.png
permalink: /
description: Data exchange format for geolocator data
---

**GeoLocator Data Package** (GeoLocator DP) defines a data exchange format for geolocator data. By using a common structure across projects, GeoLocator DP makes data easier to share, compare, and reuse, ultimately supporting bird migration research, conservation, and public outreach.

{:.alert .alert-primary style="padding-left: 32px;"}
**Ready to publish your GeoLocator Data Package?** Follow the step-by-step practical guide in the [GeoLocator Data Package chapter of the GeoPressureManual](https://geopressure.org/GeoPressureManual/geolocator-create.html) to create, curate, and share your package with confidence.

## Data Package Structure

A GeoLocator Data Package follows the more general [Data Package](https://datapackage.org/) and is organized into three components: (1) the core resources containing raw geolocator data, (2) optional but highly recommended trajectory resources generated with [GeoPressureR](https://geopressure.org/GeoPressureManual/), and (3) a minimal local manifest.

### 1. Core Resources

The core GeoLocator DP resources consist of raw geolocator data and deployment information. These `resources` can be generated without running trajectory analyses.

| File                                                                           | Description                                                                                           |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| [`tags.csv`](https://geopressure.org/GeoLocator-DP/core/tags/)                 | Table of devices used in the study. We assume that a `tag` is only used once on a single animal.      |
| [`measurements.csv`](https://geopressure.org/GeoLocator-DP/core/measurements/) | Table with the raw measurements of all sensors (e.g., light, pressure, ...) for all tags.             |
| [`observations.csv`](https://geopressure.org/GeoLocator-DP/core/observations/) | Table of bird-level field observations, including equipment, retrieval, and observations of control birds without tags. |

### 2. GeoPressureR Resources

The GeoPressureR extension consists of optional trajectory data generated through the [GeoPressureR workflow analysis](https://geopressure.org/GeoPressureManual/geopressuretemplate-workflow.html).

| File                                                                                    | Description                                                                                                                   |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [`staps.csv`](https://geopressure.org/GeoLocator-DP/geopressurer/staps)                 | Table of the stationary periods of all tags.                                                                                  |
| [`paths.csv`](https://geopressure.org/GeoLocator-DP/geopressurer/paths)                 | Table of the trajectory of all tags, typically most likely path or simulation paths.                                          |
| [`edges.csv`](https://geopressure.org/GeoLocator-DP/geopressurer/edges)                 | Table containing the flight information of the edges associated with the paths.                                               |
| [`twilights.csv`](https://geopressure.org/GeoLocator-DP/geopressurer/twilights)         | Table of the twilights estimated from light data for all tags.                                                                |
| [`pressurepaths.csv`](https://geopressure.org/GeoLocator-DP/geopressurer/pressurepaths) | Table of pressure-based paths.                                                                                                |
| `params.json`                                                                           | List of [parameters](https://geopressure.org/GeoPressureR/reference/param_create.html) used to run the GeoPressureR workflow. |

### 3. Local Manifest

Following the [Data Package standard](https://datapackage.org/standard/data-package/), each GeoLocator DP contains a [`datapackage.json`](https://github.com/GeoPressure/GeoLocator-DP/blob/main/example/datapackage.json) file with: (1) a machine-readable index of all data [`resources`](https://datapackage.org/standard/data-resource/), (2) a package-level [`$schema`](https://datapackage.org/standard/data-package/#dollar-schema) pointing to the GeoLocator DP profile version. Since v1.0, the local manifest stays intentionally minimal, while metadata are managed in Zenodo. The [GeoLocator DP profile](https://github.com/GeoPressure/GeoLocator-DP/blob/main/geolocator-dp-profile.json) defines the manifest requirements.

## How to contribute?

If you have multi-sensor geolocator data and would like to contribute a GeoLocator Data Package, follow the workflow below.

1. [`create_geopressuretemplate()`](https://geopressure.org/GeoLocatoR/reference/create_geopressuretemplate.html): Set up your local GeoPressureTemplate project folder [[guide](https://geopressure.org/GeoPressureManual/geopressuretemplate-intro.html)].
2. [`geopressuretemplate()`](https://geopressure.org/GeoPressureR/reference/geopressuretemplate.html): Run trajectory analyses in your GeoPressureTemplate project [[guide](https://geopressure.org/GeoPressureManual/geopressuretemplate-workflow.html)].
3. [`read_geopressuretemplate()`](https://geopressure.org/GeoLocatoR/reference/read_geopressuretemplate.html): Build your GeoLocator Data Package from the template outputs [[guide](https://geopressure.org/GeoPressureManual/geolocator-create.html)].
4. Draft the record on [`Zenodo`](https://zenodo.org/) with metadata, reserve the DOI, and select the GeoLocator-DP community (without publishing yet) [[guide](https://help.zenodo.org/docs/share/submit-to-community/)].
5. [`validate_gldp()`](https://geopressure.org/GeoLocatoR/reference/validate_gldp.html) and [`plot()`](https://geopressure.org/GeoLocatoR/reference/plot.geolocatordp.html): Validate the package and resolve issues until all checks pass [[guide](https://geopressure.org/GeoPressureManual/geolocator-intro.html)].
6. Submit for curation and publish the record [[guide](https://help.zenodo.org/docs/share/submit-to-community/)].

<img src="{{ '/assets/user_steps.svg' | relative_url }}" alt="Contribution workflow from setup to publication" style="width: 100%; max-width: 820px; display: block; margin: 0 auto 1rem auto;" />

<div class="alert alert-info" style="padding-left: 32px;" markdown="1">

Why use Zenodo?

1. long-term hosting, DOI assignment, and versioned records,
2. a simple and reliable way to manage metadata through web forms,
3. community curation through the [GeoLocator DP Zenodo community](https://zenodo.org/communities/geolocator-dp/).

</div>

{:.alert .alert-danger style="padding-left: 32px;"}
For the metadata checklist, validation policy, and visual quality checks before release, see the [Curation page]({{ '/curation/' | relative_url }}).

## Resources

<table>
    <tr>
        <td>
            <a href="https://geopressure.org/GeoLocatoR/"><img src="assets/logo_geolocator.png" width="100px" alt="GeoLocatoR logo"/></a>
        </td>
        <td>
            The <a href="https://geopressure.org/GeoLocatoR/">GeoLocatoR</a> R package is designed to handle GeoLocator DP: creating a DP, adding resources, writing a DP, and reading a DP. It is essentially an extension of the <a href="https://docs.ropensci.org/frictionless/">frictionless</a> package for geolocator data.
        </td>
    </tr>
    <tr style="border-top-width: 1px;">
        <td>
            <a href="https://geopressure.org/GeoPressureManual/geolocator-intro.html"><img src="assets/cover_geopressuremanual.png" width="100px" alt="GeoPressureManual logo"/></a>
        </td>
        <td>
            The <a href="https://geopressure.org/GeoPressureManual/geolocator-intro.html">Geolocator Manual</a> R book has a dedicated part on the use of the GeoLocator Data Package. This is a great place to start learning more about how to use it with your GeoPressureTemplate project.
        </td>
    </tr>
    <tr>
        <td><a href="https://geopressure.org/GeoPressureR/"><img src="assets/logo_geopressurer.png" width="100px" alt="GeoPressureR logo"/></a></td>
        <td>
            <a href="https://geopressure.org/GeoPressureR/">GeoPressureR</a> is the main package to analyze geolocator data. Once a GeoLocator Data Package is created, GeoPressureR is our recommended software to read the data into R and analyze the data.
        </td>
    </tr>
      <tr style="border-top-width: 1px;">
        <td>
            <a href="https://zenodo.org/communities/geolocator-dp/"><img src="assets/logo.png" width="100px" alt="GeoLocator DP logo"/> </a>
        </td>
        <td>
            You'll be able to find all GeoLocator Data Packages in the <a href="https://zenodo.org/communities/geolocator-dp/">GeoLocator Data Package Zenodo Community</a>. Once you've published your data package, make sure to <a href="https://help.zenodo.org/docs/share/submit-to-community/">submit it to the community</a>.
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://geopressure.org/GeoLocatorExplorer/"><img src="assets/logo_geolocatorexplorer.svg" width="100px" alt="GeoLocatorExplorer logo"/> </a>
        </td>
        <td>
            Explore the most likely trajectories of all existing data packages on a 3D map with <a href="https://geopressure.org/GeoLocatorExplorer/">GeoLocatorExplorer</a>.
        </td>
    </tr>
</table>

## How to Cite

> Nussbaumer, R., Desmet, P. & Geolocator Development Team (2024). GeoLocator Data Package. Zenodo. <https://doi.org/10.5281/zenodo.14258411>
