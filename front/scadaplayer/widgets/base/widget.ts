import { Metadata } from "../../models"
import { Simulation } from "../../simulation"
import { Size } from "./size"

export class Widget {
    constructor() {
    }

    update(_metadata: Metadata, _simulation: Simulation) { }

    draw(ctx: CanvasRenderingContext2D, size: Size) {
        // Debug background
        ctx.fillStyle = "magenta"
        ctx.fillRect(0, 0, size.width, size.height)
    }
}
