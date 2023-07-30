import { Drawer } from "./drawer";


/**
 * @brief Redispatch of drawer commands
 * @implements Drawer
 */
export class DrawerMultiplexer implements Drawer {
    drawers: Drawer[];

    constructor() {
        this.drawers = []
    }


    // Implements Drawer
    clear() {
        for (let drawer of this.drawers) {
            drawer.clear();
        }
    }

    draw_floor() {
        for (let drawer of this.drawers) {
            drawer.draw_floor();
        }
    }

    draw_ceil() {
        for (let drawer of this.drawers) {
            drawer.draw_ceil();
        }
    }

    draw_wall(column: number, height: number, color: string) {
        for (let drawer of this.drawers) {
            drawer.draw_wall(column, height, color);
        }
    }
}