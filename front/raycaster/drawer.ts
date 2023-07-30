/**
 * @brief An interface for drawing stuff
 */
export interface Drawer {
    /**
     * @brief Clear the canvas
     */
    clear(): void;

    /**
     * @brief Draw the floor
     */
    draw_floor(): void;

    /**
     * @brief Draw the ceil
     */
    draw_ceil(): void;

    /**
     * @brief Draw a vertical wall portion
     * @param column 
     * @param height Height of the wall portion, in pixels
     */
    draw_wall(column: number, height: number, color: string): void;
}
