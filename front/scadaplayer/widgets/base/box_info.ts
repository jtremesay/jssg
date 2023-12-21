import { Size } from "./size";
import { Widget } from "./widget";

export class BoxInfo extends Widget {
    labels: string[]
    values: string[]

    constructor(labels: string[]) {
        super()
        this.labels = labels
        this.values = labels.map(() => "")
    }

    draw(ctx: CanvasRenderingContext2D, size: Size): void {
        ctx.save()
        ctx.translate(0, 20)
        this.labels.forEach((label, i) => {
            ctx.font = "12px monospace"
            ctx.textAlign = "left"
            ctx.fillStyle = "white"
            ctx.fillText(label.toUpperCase() + ":", 10, i * 15, size.width)
            ctx.textAlign = "right"
            ctx.fillText(this.values[i], size.width - 10, i * 15, size.width)
        })
        ctx.restore()
    }
}