import { Metadata } from "../../models";
import { Simulation } from "../../simulation";
import { Gauge } from "../base/gauge";
import { TitledWidget } from "../base/titled_widget";

export class ActivePowerGauge extends TitledWidget {
    constructor() {
        let gauge = new Gauge(0, 2000)
        gauge.unit = "kW"
        super("Active power", gauge)
        gauge.short_tick_step = 100
        gauge.long_tick_step = 500
    }

    update(_metadata: Metadata, simulation: Simulation): void {
        (this.widget as Gauge).value = simulation.record!.active_power
    }
}
