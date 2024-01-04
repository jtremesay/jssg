import { Metadata } from "../../models";
import { Simulation } from "../../simulation";
import { Gauge } from "../base/gauge";
import { TitledWidget } from "../base/titled_widget";

export class WindSpeedGauge extends TitledWidget {
    constructor() {
        let gauge = new Gauge(0, 25)
        gauge.unit = "m.s⁻¹"
        gauge.precision = 1
        super("Wind speed", gauge)
    }

    update(_metadata: Metadata, simulation: Simulation): void {
        (this.widget as Gauge).value = simulation.record!.wind_speed
    }
}
