import { Widget } from "./widget"
import { DashboardItem } from "./dashboard_item"
import { Size } from "./size"
import { Point } from "./point"
import { Metadata } from "../../models"
import { GRID_SIZE, ITEM_SIZE } from "../../config"
import { Simulation } from "../../simulation"

export class Dashboard extends Widget {
    items: DashboardItem[]
    display_grid: boolean

    constructor() {
        super()
        this.items = []
        this.display_grid = false
    }

    add_item(widget: Widget, size: Size, position: Point): DashboardItem {
        let item = new DashboardItem(position, size, widget)
        this.items.push(item)

        return item
    }

    update(metadata: Metadata, simulation: Simulation) {
        this.items.forEach((item) => {
            item.update(metadata, simulation)
        })
    }

    draw(ctx: CanvasRenderingContext2D, size: Size) {
        super.draw(ctx, size)

        ctx.fillStyle = "black"
        ctx.fillRect(0, 0, size.width, size.height)

        // Draw debug grid
        if (this.display_grid) {
            ctx.beginPath()
            ctx.lineWidth = 1
            ctx.strokeStyle = "white"
            for (let x = 0; x < GRID_SIZE.width; ++x) {
                ctx.moveTo(x * ITEM_SIZE.width, 0)
                ctx.lineTo(x * ITEM_SIZE.width, GRID_SIZE.height * ITEM_SIZE.height)
            }
            for (let y = 0; y < GRID_SIZE.height; ++y) {
                ctx.moveTo(0, y * ITEM_SIZE.height)
                ctx.lineTo(GRID_SIZE.width * ITEM_SIZE.width, y * ITEM_SIZE.height)
            }
            ctx.stroke()
        }

        this.items.forEach((item) => {
            item.draw(ctx, size)
        })
    }
}
