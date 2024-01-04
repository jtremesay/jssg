import { ITEM_SIZE } from "../../config"
import { Metadata } from "../../models"
import { Simulation } from "../../simulation"
import { Point } from "./point"
import { Size } from "./size"
import { Widget } from "./widget"

export class DashboardItem extends Widget {
    position: Point
    size: Size
    widget: Widget

    constructor(position: Point, size: Size, widget: Widget) {
        super()
        this.position = position
        this.size = size
        this.widget = widget
    }

    update(metadata: Metadata, simulation: Simulation) {
        this.widget.update(metadata, simulation)
    }


    draw(ctx: CanvasRenderingContext2D, _size: Size) {
        ctx.save()
        ctx.translate(
            this.position.x * ITEM_SIZE.width,
            this.position.y * ITEM_SIZE.height,
        )

        let size = new Size(
            this.size.width * ITEM_SIZE.width,
            this.size.height * ITEM_SIZE.height,
        )

        // Draw the inner widget
        this.widget.draw(ctx, size)

        // Draw the border
        ctx.beginPath()
        ctx.lineWidth = 1
        ctx.strokeStyle = "white"
        ctx.moveTo(0, 0)
        ctx.lineTo(size.width, 0)
        ctx.lineTo(size.width, size.height)
        ctx.lineTo(0, size.height)
        ctx.lineTo(0, 0)
        ctx.stroke()

        ctx.restore()
    }
}
