import { ScadaRecord } from "./models"

export function parse_scada(scada: string): ScadaRecord[] {
    let lines = scada.split("\n")

    // Parse headers
    let lut: Record<string, number> = {}
    lines[0].split(",").forEach((value, i) => {
        lut[value] = i
    })
    lines.splice(0, 1)

    return lines.map((value) => value.trim()).filter((value) => value.length).map((line) => {
        let values = line.split(",")

        return {
            timestamp: new Date(values[lut["timestamp"]]),
            wind_speed: Number.parseFloat(values[lut["wind_speed"]]),
            wind_direction: Number.parseFloat(values[lut["wind_direction"]]),
            air_temperature: Number.parseFloat(values[lut["air_temperature"]]),
            nacelle_direction: Number.parseFloat(values[lut["nacelle_direction"]]),
            active_power: Number.parseFloat(values[lut["active_power"]]),
            pitch_angle: Number.parseFloat(values[lut["pitch_angle"]]),
        }
    })
}
