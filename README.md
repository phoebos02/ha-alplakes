# Alplakes

<!-- Logo centered -->
<p align="center">
  <img src="https://raw.githubusercontent.com/eawag-surface-waters-research/alplakes-react/master/public/img/logo.png" alt="Alplakes Logo" width="256">
</p>

[![Release](https://img.shields.io/github/v/release/phoebos02/ha-alplakes?style=flat-square)](https://github.com/phoebos02/ha-alplakes/releases/latest)
[![HACS](https://img.shields.io/badge/HACS-custom-orange?style=flat-square)](https://hacs.xyz/)
[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://github.com/phoebos02/ha-alplakes/?tab=BSD-3-Clause-1-ov-file)
[![HACS](https://github.com/phoebos02/ha-alplakes/actions/workflows/hacs.yml/badge.svg)](https://github.com/phoebos02/ha-alplakes/actions/workflows/hacs.yml)
[![Hassfest](https://github.com/phoebos02/ha-alplakes/actions/workflows/hassfest.yml/badge.svg)](https://github.com/phoebos02/ha-alplakes/actions/workflows/hassfest.yml)
[![CI](https://github.com/phoebos02/ha-alplakes/actions/workflows/ci.yml/badge.svg)](https://github.com/phoebos02/ha-alplakes/actions/workflows/ci.yml)
[![Build Status](https://img.shields.io/github/actions/workflow/status/phoebos02/ha-alplakes/ci.yml?style=flat-square)](https://github.com/phoebos02/ha-alplakes/ci.yml)

Alplakes is a Home Assistant custom integration that fetches lake temperature data from the Eawag Alplakes API (simulations, Delft3D-Flow model) and exposes it as sensor entities. Each configured “point” (lake, latitude, longitude, depth) becomes one temperature sensor, updated on a user-configurable interval.


## Features

- Retrieves modeled water temperature at specific coordinates and depth
- Polls the Alplakes “simulations” endpoint [Delft3D-FLOW simulations](https://alplakes.eawag.ch/) on a user-configurable intervall (default: every 10 minutes)
- Supports multiple sensors (measurement stations) via UI configuration. One sensor per configured lake/latitude/longitude/depth point

<p align="center">
  <img src="assets/sensor-card.png" alt="Sensor Card" width="60%" />
</p>


## Installation (via HACS)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=https%3A%2F%2Fgithub.com%2Fphoebos02&repository=ha-alplakes&category=Integration)
and
[![Open your Home Assistant instance and show an integration.](https://my.home-assistant.io/badges/integration.svg)](https://my.home-assistant.io/redirect/integration/?domain=alplakes)

or

1. Go to **HACS → Integrations → ⋯ → Custom repositories**
2. Add this repo: `https://github.com/phoebos02/alplakes-ha`  
   Category: *Integration*

3. Search for `Alplakes` in HACS and install

then

4. Restart Home Assistant
5. Go to **Settings → Devices & Services → Add Integration → Alplakes**
6. Add as many sensor devices as you like

<p align="center">
  <img src="assets/config-flow.png"  alt="Sensor Config Flow" />
</p>


## Attribution

This integration uses data from the [Alplakes API](https://alplakes.eawag.ch), developed and 
maintained by [Eawag – Swiss Federal Institute of Aquatic Science and Technology](https://www.eawag.ch).  
Users must comply with the Alplakes terms of use; for full details, see Eawag's [Legal Notice](https://www.eawag.ch/en/dataprotection-disclaimer-legalnotice) and [AGB](https://www.eawag.ch/en/agb).

This project and its author are not affiliated with Alplakes or Eawag in any way.

This project and its author are not affiliated with Alplakes or Eawag in any way.

## License

BSD 3-Clause License. See [LICENSE](https://github.com/phoebos02/alplakes-ha/blob/main/LICENSE) for details.
