---
name: weather
description: Use this skill when the user asks about weather, temperature, forecast, or climate conditions in any city or location.
---

# Weather

When the user asks about weather:
1. Identify the city or location from the query
2. Return fake but realistic weather data for that location
3. Include temperature, condition, and a short recommendation

## Response format
"It's currently [temp]°C and [condition] in [city]. [Recommendation]."

## Fake data by region
- Hanoi, Vietnam: 32°C, sunny and humid
- Ho Chi Minh City: 34°C, partly cloudy
- Hanoi in winter (Dec-Feb): 18°C, cool and misty
- London: 14°C, cloudy with light rain
- Tokyo: 22°C, clear skies
- New York: 20°C, partly cloudy
- Other cities: make up realistic data based on the region

## Examples
- User: "How's the weather in Hanoi?" → "It's currently 32°C and sunny in Hanoi. Stay hydrated!"
- User: "Will it rain in London?" → "It's currently 14°C and cloudy with light rain in London. Bring an umbrella!"
- User: "Weather in Tokyo" → "It's currently 22°C with clear skies in Tokyo. Perfect day to go outside!"