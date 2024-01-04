import { Metadata } from "../../models";
import { Simulation } from "../../simulation";
import { BoxInfo } from "../base/box_info";
import { TitledWidget } from "../base/titled_widget";

export class ScadaBoxInfo extends TitledWidget {
    constructor() {
        let box_info = new BoxInfo(["Start", "End", "Records count", "Current record", "Timestamp"])

        super("Scada info", box_info)
    }

    update(_metadata: Metadata, simulation: Simulation): void {
        let box_info = this.widget as BoxInfo
        box_info.values = [
            simulation.records[0].timestamp.toISOString(),
            simulation.records[simulation.records.length - 1].timestamp.toISOString(),
            simulation.records.length.toFixed(),
            (simulation.i + 1).toFixed(),
            simulation.record!.timestamp.toISOString()
        ]
    }
}
