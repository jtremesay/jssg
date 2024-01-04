import { Metadata } from "../../models";
import { Simulation } from "../../simulation";
import { Gauge } from "../base/gauge";
import { TitledWidget } from "../base/titled_widget";

export class PitchAngleGauge extends TitledWidget {
    constructor() {
        let gauge = new Gauge(0, 90)
        gauge.unit = "°"
        gauge.precision = 1

        super("Pitch angle", gauge)
    }

    update(_metadata: Metadata, simulation: Simulation): void {
        (this.widget as Gauge).value = simulation.record!.pitch_angle
    }
}
