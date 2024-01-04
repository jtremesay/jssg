import { Metadata } from "../../models";
import { Simulation } from "../../simulation";
import { Gauge } from "../base/gauge";
import { TitledWidget } from "../base/titled_widget";

export class AirTemperatureGauge extends TitledWidget {
    constructor() {
        let gauge = new Gauge(-20, 40)
        gauge.unit = "°C"
        gauge.precision = 1

        super("Air temperature", gauge)
    }

    update(_metadata: Metadata, simulation: Simulation): void {
        (this.widget as Gauge).value = simulation.record!.air_temperature
    }
}
