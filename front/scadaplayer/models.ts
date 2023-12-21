export interface ScadaRecord {
    timestamp: Date
    wind_speed: number
    wind_direction: number
    air_temperature: number
    nacelle_direction: number
    active_power: number
    pitch_angle: number
}


export interface Metadata {
    farm: string | null
    turbine: string | null
    turbine_model: string | null
    nominal_power: number | null
}
