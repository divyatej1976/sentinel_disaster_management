/**
 * Weather service using the Open-Meteo Hourly API (free, no API key required).
 * Fetches 7-day hourly forecast and extracts the current hour's values.
 *
 * API docs: https://open-meteo.com/en/docs
 *
 * Parameters used:
 *  temperature_2m         — surface temperature (°C)
 *  apparent_temperature   — feels-like temperature (°C)
 *  relative_humidity_2m   — relative humidity (%)
 *  precipitation          — total precipitation (mm)
 *  rain                   — rainfall component (mm)
 *  showers                — shower component (mm)
 *  snowfall               — snowfall (cm)
 *  cloud_cover            — total cloud cover (%)
 *  surface_pressure       — surface air pressure (hPa)
 *  visibility             — visibility (m)
 *  wind_speed_10m         — wind speed at 10m (km/h)
 *  wind_direction_120m    — wind direction at 120m (°)
 *  temperature_80m        — temperature at 80m for inversion detection (°C)
 */

export interface WeatherData {
  /** 0 = Clear, 1 = Mild, 2 = Humid, 3 = Adverse */
  weatherLevel: 0 | 1 | 2 | 3;
  weatherLabel: string;

  // Core epidemiological inputs
  humidity: number;
  precipitation: number;
  rain: number;
  showers: number;
  snowfall: number;

  // Environmental context
  temperature: number;
  apparentTemperature: number;
  cloudCover: number;
  surfacePressure: number;
  visibility: number;
  windSpeed: number;

  // Metadata
  locationName: string;
  latitude: number;
  longitude: number;

  /** ISO timestamp of the fetched hour */
  observationTime: string;
}

const LEVEL_LABELS: Record<0 | 1 | 2 | 3, string> = {
  0: 'Clear',
  1: 'Mild',
  2: 'Humid',
  3: 'Adverse',
};

/**
 * Maps multiple meteorological parameters to a 4-level epidemiological risk scale.
 *
 * Rationale:
 *  - Humidity > 80%: high vector/pathogen survival rate → Adverse
 *  - Significant precipitation or snowfall: outdoor exposure risk → Adverse
 *  - Low visibility (< 1km): fog, pollution, or heavy rain → Adverse/Humid
 *  - Moderate humidity (60–80%): elevated but not critical → Humid
 *  - Light rain or cloud > 70%: damp conditions → Mild/Humid
 *  - Dry and clear: lowest risk → Clear
 */
function mapToWeatherLevel(
  humidity: number,
  precipitation: number,
  rain: number,
  showers: number,
  snowfall: number,
  cloudCover: number,
  visibility: number,
): 0 | 1 | 2 | 3 {
  const totalWet = precipitation + rain + showers;
  const isHeavyWet = totalWet > 5 || snowfall > 2;
  const isFoggy = visibility < 1000;

  if (humidity > 80 || isHeavyWet || isFoggy) return 3;           // Adverse
  if (humidity > 65 || totalWet > 1 || cloudCover > 80) return 2; // Humid
  if (humidity > 45 || totalWet > 0.1 || cloudCover > 50) return 1; // Mild
  return 0;                                                         // Clear
}

/**
 * Finds the index of the current hour in the hourly time array.
 */
function getCurrentHourIndex(times: string[]): number {
  const now = new Date();
  // Round down to current hour in ISO format matching Open-Meteo output
  const currentHour = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours())
    .toISOString()
    .slice(0, 13); // "2025-04-29T18"

  const idx = times.findIndex((t) => t.startsWith(currentHour));
  return idx >= 0 ? idx : 0;
}

/**
 * Gets the user's GPS coordinates via browser Geolocation API.
 */
function getUserCoordinates(): Promise<GeolocationCoordinates> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by this browser.'));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve(pos.coords),
      (err) => reject(new Error(`Location access denied: ${err.message}`)),
      { timeout: 10_000 }
    );
  });
}

/**
 * Reverse-geocodes coordinates to a human-readable city name (Nominatim, free).
 */
async function reverseGeocode(lat: number, lon: number): Promise<string> {
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`,
      { headers: { 'Accept-Language': 'en' } }
    );
    const data = await res.json();
    const addr = data.address;
    return addr.city || addr.town || addr.village || addr.county || addr.state || `${lat.toFixed(2)}°, ${lon.toFixed(2)}°`;
  } catch {
    return `${lat.toFixed(2)}°N, ${lon.toFixed(2)}°E`;
  }
}

/**
 * Main export: fetches live hourly weather for the user's current location.
 */
export async function fetchLiveWeather(): Promise<WeatherData> {
  // Step 1: Get GPS
  const coords = await getUserCoordinates();
  const { latitude, longitude } = coords;

  // Step 2: Fetch rich hourly data from Open-Meteo
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m,relative_humidity_2m,rain,apparent_temperature,cloud_cover,surface_pressure,visibility,temperature_80m,wind_direction_120m,wind_speed_10m,precipitation,snowfall,showers&past_days=0&forecast_days=7&timezone=auto`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Open-Meteo API error: ${response.status} ${response.statusText}`);
  }
  const data = await response.json();
  const h = data.hourly;

  // Step 3: Find current hour index
  const idx = getCurrentHourIndex(h.time as string[]);

  // Step 4: Extract current-hour values
  const temperature: number       = h.temperature_2m[idx] ?? 0;
  const apparentTemperature: number = h.apparent_temperature[idx] ?? 0;
  const humidity: number          = h.relative_humidity_2m[idx] ?? 0;
  const precipitation: number     = h.precipitation[idx] ?? 0;
  const rain: number              = h.rain[idx] ?? 0;
  const showers: number           = h.showers[idx] ?? 0;
  const snowfall: number          = h.snowfall[idx] ?? 0;
  const cloudCover: number        = h.cloud_cover[idx] ?? 0;
  const surfacePressure: number   = h.surface_pressure[idx] ?? 1013;
  const visibility: number        = h.visibility[idx] ?? 10000;
  const windSpeed: number         = h.wind_speed_10m[idx] ?? 0;
  const observationTime: string   = (h.time as string[])[idx] ?? '';

  // Step 5: Map to 4-level risk scale
  const weatherLevel = mapToWeatherLevel(humidity, precipitation, rain, showers, snowfall, cloudCover, visibility);

  // Step 6: Reverse geocode (concurrent)
  const locationName = await reverseGeocode(latitude, longitude);

  return {
    weatherLevel,
    weatherLabel: LEVEL_LABELS[weatherLevel],
    humidity,
    precipitation,
    rain,
    showers,
    snowfall,
    temperature,
    apparentTemperature,
    cloudCover,
    surfacePressure,
    visibility,
    windSpeed,
    locationName,
    latitude,
    longitude,
    observationTime,
  };
}
