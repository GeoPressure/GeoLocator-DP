---
title: Curation
background: /assets/curation.jpg
permalink: /curation/
---

## 1. Mandatory Technical Validation

All submitted records must pass the automated validation of [`validate_gldp()`](https://geopressure.com/GeoLocatoR/reference/validate_gldp.html).

## 2. Visual Check

In addition to automated checks, each submission must pass visual and metadata sanity checks. Coverage, ringing, and map plots are inspected to ensure they are biologically plausible and free of obvious artifacts.

Run these checks from the directory containing your package manifest:

```r
pkg <- GeoLocatoR::read_gldp("datapackage.json")
GeoLocatoR::plot(pkg, "coverage")
GeoLocatoR::plot(pkg, "ring")
GeoLocatoR::plot(pkg, "map")
print(pkg)
```

## 3. Metadata Best Practices

### Required

- **Access**: Embargoed records are permitted, but duration must be reasonable and justified, typically until first publication.
- **Description**: Include minimum contextual information such as study species, main study area, project objective, and key processing notes that affect reuse. It's also a good place to invite potential users of the data to get in touch.

### Recommended

- **Title**: Should start with `GeoLocator Data Package: `. The prefix is strongly recommended and expected by the GeoLocator DP community; [`validate_gldp()`](https://geopressure.org/GeoLocatoR/reference/validate_gldp.html) warns when it is missing.
- **Related works**: Link publications that use the data via related identifiers.
- **Software/Repository URL**: Provide a link to the GeoPressureTemplate GitHub repository.
- **Zenodo badge**: Add the Zenodo badge of your repository at the top of the GitHub `README`.
- **Interim files**: Update the `data/interim/<tag_id>.RData` files in your GeoPressureTemplate repository after the final analysis run so they match the published trajectories.
- **Author and roles**: Assign author roles as completely as possible using Zenodo/DataCite role options.

<div class="alert alert-info" style="padding-left: 32px;" markdown="1">

Author role definitions:

- **Contact person**: Person to contact for questions about access, use, citation, or additional information.
- **Project leader**: Person officially designated as head of project (i.e., principal investigator).
- **Data curator**: Person in charge of assembling and standardizing the geolocator data package and metadata for publication.
- **Researcher**: Person involved in analyzing geolocator data or results, often running GeoPressure analyses.
- **Rights holder**: Person or institution owning or managing property rights, including intellectual property rights over the resource.
- **Supervisor**: Designated administrator over the project, including funding acquisition.
- **Data collector**: Person responsible for finding, gathering, or collecting geolocator data (often ringers and field assistants).
- **Other**: Significant contribution not covered by a more specific role (avoid if possible).

</div>
