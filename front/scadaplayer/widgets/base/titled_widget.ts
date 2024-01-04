import { TITLE_HEIGHT } from "../../config";
import { Metadata } from "../../models";
import { Simulation } from "../../simulation";
import { Size } from "./size";
import { Widget } from "./widget";

export class TitledWidget extends Widget {
    label: string
    widget: Widget

    constructor(label: string, widget: Widget) {
        super()
        this.label = label
        this.widget = widget
    }

    update(metadata: Metadata, simulation: Simulation): void {
        this.widget.update(metadata, simulation)
    }

    draw(ctx: CanvasRenderingContext2D, size: Size): void {
        ctx.save()

        // Title
        ctx.font = "bold 12px monospace";
        ctx.textAlign = "center"
        ctx.fillStyle = "white"
        ctx.fillText(this.label.toUpperCase(), size.width / 2, 15, size.width)

        // Inner widget
        ctx.translate(0, TITLE_HEIGHT)
        this.widget.draw(
            ctx,
            new Size(size.width, size.height - TITLE_HEIGHT)
        )

        // Border
        ctx.beginPath()
        ctx.lineWidth = 1
        ctx.strokeStyle = "white"
        ctx.moveTo(0, 0)
        ctx.lineTo(size.width, 0)
        ctx.stroke()

        ctx.restore()
    }
}
